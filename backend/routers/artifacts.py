"""
Artifacts router — Get and update justification artifacts for deals.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Justification, AgentLog

router = APIRouter()


class ArtifactUpdate(BaseModel):
    roi_model: Optional[dict] = None
    exec_summary: Optional[str] = None
    procurement_doc: Optional[str] = None
    objection_responses: Optional[list] = None


class SectionUpdate(BaseModel):
    section: str  # roi_model / exec_summary / procurement_doc / objection_responses
    content: dict | str | list


def justification_to_dict(j: Justification) -> dict:
    return {
        "id": j.id,
        "deal_id": j.deal_id,
        "roi_model": j.roi_model,
        "exec_summary": j.exec_summary,
        "procurement_doc": j.procurement_doc,
        "objection_responses": j.objection_responses,
        "completeness_score": j.completeness_score,
        "agent_status": j.agent_status,
        "last_updated": j.last_updated.isoformat() if j.last_updated else None
    }


@router.get("/{deal_id}")
def get_artifact(deal_id: int, db: Session = Depends(get_db)):
    j = db.query(Justification).filter(Justification.deal_id == deal_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Justification not found for this deal")
    return justification_to_dict(j)


@router.put("/{deal_id}")
def update_artifact(deal_id: int, payload: ArtifactUpdate, db: Session = Depends(get_db)):
    j = db.query(Justification).filter(Justification.deal_id == deal_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Justification not found for this deal")

    changed_sections = []
    if payload.roi_model is not None:
        j.roi_model = payload.roi_model
        changed_sections.append("ROI model")
    if payload.exec_summary is not None:
        j.exec_summary = payload.exec_summary
        changed_sections.append("exec summary")
    if payload.procurement_doc is not None:
        j.procurement_doc = payload.procurement_doc
        changed_sections.append("procurement doc")
    if payload.objection_responses is not None:
        j.objection_responses = payload.objection_responses
        changed_sections.append("objection responses")

    j.agent_status = "needs_review"
    j.last_updated = datetime.utcnow()

    # Recalculate completeness
    score = 0
    if j.roi_model and j.roi_model.get("scenarios"):
        score += 30
    if j.exec_summary:
        score += 25
    if j.procurement_doc:
        score += 20
    if j.objection_responses:
        score += 15
        addressed = sum(1 for o in j.objection_responses if o.get("status") == "addressed")
        if addressed == len(j.objection_responses) and len(j.objection_responses) > 0:
            score += 10
    j.completeness_score = min(score, 100)

    db.commit()

    if changed_sections:
        log = AgentLog(
            deal_id=deal_id,
            action_type="section_updated",
            description=f"Rep manually updated: {', '.join(changed_sections)}. Completeness: {j.completeness_score}%."
        )
        db.add(log)
        db.commit()

    db.refresh(j)
    return justification_to_dict(j)


@router.put("/{deal_id}/section")
def update_section(deal_id: int, payload: SectionUpdate, db: Session = Depends(get_db)):
    j = db.query(Justification).filter(Justification.deal_id == deal_id).first()
    if not j:
        raise HTTPException(status_code=404, detail="Justification not found for this deal")

    valid_sections = ["roi_model", "exec_summary", "procurement_doc", "objection_responses"]
    if payload.section not in valid_sections:
        raise HTTPException(status_code=400, detail=f"Invalid section. Must be one of: {valid_sections}")

    setattr(j, payload.section, payload.content)
    j.last_updated = datetime.utcnow()
    j.agent_status = "needs_review"

    # Recalculate completeness
    score = 0
    if j.roi_model and j.roi_model.get("scenarios"):
        score += 30
    if j.exec_summary:
        score += 25
    if j.procurement_doc:
        score += 20
    if j.objection_responses:
        score += 15
        addressed = sum(1 for o in j.objection_responses if o.get("status") == "addressed")
        if addressed == len(j.objection_responses) and len(j.objection_responses) > 0:
            score += 10
    j.completeness_score = min(score, 100)

    db.commit()

    log = AgentLog(
        deal_id=deal_id,
        action_type="section_updated",
        description=f"Rep updated section: {payload.section}. Completeness: {j.completeness_score}%."
    )
    db.add(log)
    db.commit()

    db.refresh(j)
    return justification_to_dict(j)
