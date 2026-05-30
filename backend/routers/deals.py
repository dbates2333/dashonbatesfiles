"""
Deals router — CRUD for deals, signal ingestion, justification building, health scoring.
"""
import json
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db, SessionLocal
from models import Deal, DealSignal, Justification, HealthScore, AgentLog

logger = logging.getLogger(__name__)
router = APIRouter()


# ---- Pydantic schemas ----

class DealCreate(BaseModel):
    company: str
    contact_name: str
    contact_title: str
    deal_value: float
    stage: str
    archetype: str
    rep_name: Optional[str] = None


class DealUpdate(BaseModel):
    company: Optional[str] = None
    contact_name: Optional[str] = None
    contact_title: Optional[str] = None
    deal_value: Optional[float] = None
    stage: Optional[str] = None
    archetype: Optional[str] = None
    rep_name: Optional[str] = None


class SignalCreate(BaseModel):
    signal_type: str  # call/email/meeting
    content: str
    timestamp: Optional[datetime] = None


# ---- Helpers ----

def deal_to_dict(deal: Deal, include_health: bool = True) -> dict:
    d = {
        "id": deal.id,
        "company": deal.company,
        "contact_name": deal.contact_name,
        "contact_title": deal.contact_title,
        "deal_value": deal.deal_value,
        "stage": deal.stage,
        "archetype": deal.archetype,
        "rep_name": deal.rep_name,
        "created_at": deal.created_at.isoformat() if deal.created_at else None,
        "updated_at": deal.updated_at.isoformat() if deal.updated_at else None,
    }
    if include_health and deal.health_scores:
        latest = max(deal.health_scores, key=lambda h: h.computed_at)
        d["latest_health"] = {
            "overall_score": latest.overall_score,
            "dimensions": latest.dimensions,
            "risks": latest.risks,
            "gaps": latest.gaps,
            "agent_actions": latest.agent_actions,
            "computed_at": latest.computed_at.isoformat()
        }
    else:
        d["latest_health"] = None
    if deal.justification:
        d["justification_status"] = {
            "completeness_score": deal.justification.completeness_score,
            "agent_status": deal.justification.agent_status,
            "last_updated": deal.justification.last_updated.isoformat() if deal.justification.last_updated else None
        }
    else:
        d["justification_status"] = None
    return d


# ---- Routes ----

@router.get("")
def list_deals(db: Session = Depends(get_db)):
    deals = db.query(Deal).all()
    return [deal_to_dict(d) for d in deals]


@router.get("/{deal_id}")
def get_deal(deal_id: int, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    result = deal_to_dict(deal)

    # Include signals
    result["signals"] = [
        {
            "id": s.id,
            "signal_type": s.signal_type,
            "content": s.content,
            "timestamp": s.timestamp.isoformat() if s.timestamp else None,
            "extracted_insights": s.extracted_insights
        }
        for s in sorted(deal.signals, key=lambda x: x.timestamp or datetime.min, reverse=True)
    ]

    # Include full justification
    if deal.justification:
        j = deal.justification
        result["justification"] = {
            "id": j.id,
            "roi_model": j.roi_model,
            "exec_summary": j.exec_summary,
            "procurement_doc": j.procurement_doc,
            "objection_responses": j.objection_responses,
            "completeness_score": j.completeness_score,
            "agent_status": j.agent_status,
            "last_updated": j.last_updated.isoformat() if j.last_updated else None
        }
    else:
        result["justification"] = None

    # Include all health scores
    if deal.health_scores:
        result["health_scores"] = [
            {
                "id": h.id,
                "overall_score": h.overall_score,
                "dimensions": h.dimensions,
                "risks": h.risks,
                "gaps": h.gaps,
                "agent_actions": h.agent_actions,
                "computed_at": h.computed_at.isoformat()
            }
            for h in sorted(deal.health_scores, key=lambda h: h.computed_at, reverse=True)
        ]
    else:
        result["health_scores"] = []

    return result


@router.post("")
def create_deal(payload: DealCreate, db: Session = Depends(get_db)):
    deal = Deal(**payload.model_dump())
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal_to_dict(deal)


@router.put("/{deal_id}")
def update_deal(deal_id: int, payload: DealUpdate, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(deal, field, value)
    deal.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(deal)
    return deal_to_dict(deal)


@router.post("/{deal_id}/signals")
async def add_signal(deal_id: int, payload: SignalCreate, request: Request, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    signal = DealSignal(
        deal_id=deal_id,
        signal_type=payload.signal_type,
        content=payload.content,
        timestamp=payload.timestamp or datetime.utcnow()
    )
    db.add(signal)
    db.commit()
    db.refresh(signal)

    # Log action
    log = AgentLog(
        deal_id=deal_id,
        action_type="signal_received",
        description=f"New {payload.signal_type} signal received ({len(payload.content)} chars). Queuing intelligence analysis."
    )
    db.add(log)
    db.commit()

    # Run intelligence agent in background
    import asyncio
    asyncio.create_task(_analyze_signal_background(signal.id, deal_id, request))

    return {
        "id": signal.id,
        "deal_id": deal_id,
        "signal_type": signal.signal_type,
        "timestamp": signal.timestamp.isoformat(),
        "status": "analyzing"
    }


async def _analyze_signal_background(signal_id: int, deal_id: int, request: Request):
    """Background task: run intelligence agent on a signal."""
    from agents.intelligence_agent import analyze_signal
    db = SessionLocal()
    try:
        signal = db.query(DealSignal).filter(DealSignal.id == signal_id).first()
        deal = db.query(Deal).filter(Deal.id == deal_id).first()
        if not signal or not deal:
            return

        deal_context = {
            "company": deal.company,
            "contact_name": deal.contact_name,
            "contact_title": deal.contact_title,
            "deal_value": deal.deal_value,
            "stage": deal.stage,
            "archetype": deal.archetype
        }

        # Broadcast start
        broadcast = getattr(request.app.state, 'broadcast_to_deal', None)
        if broadcast:
            await broadcast(deal_id, {
                "type": "agent_working",
                "agent": "intelligence",
                "message": f"Analyzing {signal.signal_type} signal..."
            })

        result = await analyze_signal(signal.content, signal.signal_type, deal_context)

        # Save insights
        signal.extracted_insights = result.model_dump()
        db.commit()

        # Log completion
        log = AgentLog(
            deal_id=deal_id,
            action_type="signal_analyzed",
            description=f"Intelligence agent extracted {len(result.pain_points)} pain points, {len(result.objections)} objections, {len(result.stakeholders)} stakeholders from {signal.signal_type} signal."
        )
        db.add(log)
        db.commit()

        if broadcast:
            await broadcast(deal_id, {
                "type": "signal_analyzed",
                "signal_id": signal_id,
                "insights": result.model_dump()
            })

    except Exception as e:
        logger.error(f"Error analyzing signal {signal_id}: {e}")
    finally:
        db.close()


@router.post("/{deal_id}/build-justification")
async def build_justification(deal_id: int, request: Request, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    # Set agent status to building
    if deal.justification:
        deal.justification.agent_status = "building"
    else:
        just = Justification(deal_id=deal_id, agent_status="building")
        db.add(just)
    db.commit()

    # Log
    log = AgentLog(
        deal_id=deal_id,
        action_type="artifact_build_started",
        description="Artifact agent started building full justification package."
    )
    db.add(log)
    db.commit()

    signals_data = [
        {
            "id": s.id,
            "signal_type": s.signal_type,
            "content": s.content,
            "timestamp": s.timestamp.isoformat() if s.timestamp else None,
            "extracted_insights": s.extracted_insights
        }
        for s in deal.signals
    ]

    deal_data = {
        "company": deal.company,
        "contact_name": deal.contact_name,
        "contact_title": deal.contact_title,
        "deal_value": deal.deal_value,
        "stage": deal.stage,
        "archetype": deal.archetype
    }

    async def stream_generator():
        from agents.artifact_agent import build_justification as agent_build
        final_result = None
        try:
            async for chunk in agent_build(deal_data, signals_data):
                # Extract the Python object before serializing (not JSON serializable)
                result_obj = chunk.pop("_result_obj", None)
                if chunk.get("type") == "complete":
                    final_result = result_obj
                yield f"data: {json.dumps(chunk)}\n\n"

            # Save to DB
            if final_result:
                try:
                    inner_db = SessionLocal()
                    j = inner_db.query(Justification).filter(Justification.deal_id == deal_id).first()
                    if not j:
                        j = Justification(deal_id=deal_id)
                        inner_db.add(j)

                    j.roi_model = final_result.roi_model
                    j.exec_summary = final_result.exec_summary
                    j.procurement_doc = final_result.procurement_doc
                    j.objection_responses = final_result.objection_responses
                    j.completeness_score = final_result.completeness_score
                    j.agent_status = "complete"
                    j.last_updated = datetime.utcnow()
                    inner_db.commit()

                    objection_count = len(final_result.objection_responses) if final_result.objection_responses else 0
                    log = AgentLog(
                        deal_id=deal_id,
                        action_type="artifact_built",
                        description=f"Artifact agent completed full justification build. Completeness: {final_result.completeness_score}%. ROI model, exec summary, procurement doc, and {objection_count} objection responses generated."
                    )
                    inner_db.add(log)
                    inner_db.commit()
                finally:
                    inner_db.close()

            # Broadcast completion
            broadcast = getattr(request.app.state, 'broadcast_to_deal', None)
            if broadcast and final_result:
                await broadcast(deal_id, {
                    "type": "justification_complete",
                    "completeness_score": final_result.completeness_score
                })

        except Exception as e:
            logger.error(f"Error building justification for deal {deal_id}: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        stream_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/{deal_id}/refresh-health")
async def refresh_health(deal_id: int, request: Request, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    signals_data = [
        {
            "id": s.id,
            "signal_type": s.signal_type,
            "content": s.content,
            "timestamp": s.timestamp.isoformat() if s.timestamp else None,
            "extracted_insights": s.extracted_insights
        }
        for s in deal.signals
    ]

    just_data = None
    if deal.justification:
        j = deal.justification
        just_data = {
            "completeness_score": j.completeness_score,
            "agent_status": j.agent_status,
            "roi_model": j.roi_model,
            "exec_summary": j.exec_summary,
            "procurement_doc": j.procurement_doc,
            "objection_responses": j.objection_responses
        }

    deal_data = {
        "company": deal.company,
        "contact_name": deal.contact_name,
        "contact_title": deal.contact_title,
        "deal_value": deal.deal_value,
        "stage": deal.stage,
        "archetype": deal.archetype
    }

    from agents.health_agent import score_deal_health
    result = await score_deal_health(deal_data, just_data, signals_data)

    health = HealthScore(
        deal_id=deal_id,
        overall_score=result.overall_score,
        dimensions=result.dimensions,
        risks=result.risks,
        gaps=result.gaps,
        agent_actions=result.agent_actions
    )
    db.add(health)

    log = AgentLog(
        deal_id=deal_id,
        action_type="health_scored",
        description=f"Health agent scored deal: {result.overall_score:.0f}/100 overall. {len(result.risks)} risks, {len(result.gaps)} gaps identified."
    )
    db.add(log)
    db.commit()

    broadcast = getattr(request.app.state, 'broadcast_to_deal', None)
    if broadcast:
        await broadcast(deal_id, {
            "type": "health_updated",
            "overall_score": result.overall_score,
            "risks": result.risks
        })

    return {
        "overall_score": result.overall_score,
        "dimensions": result.dimensions,
        "risks": result.risks,
        "gaps": result.gaps,
        "agent_actions": result.agent_actions
    }


@router.get("/{deal_id}/agent-log")
def get_agent_log(deal_id: int, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    logs = db.query(AgentLog).filter(AgentLog.deal_id == deal_id).order_by(AgentLog.timestamp.desc()).all()
    return [
        {
            "id": l.id,
            "action_type": l.action_type,
            "description": l.description,
            "timestamp": l.timestamp.isoformat()
        }
        for l in logs
    ]
