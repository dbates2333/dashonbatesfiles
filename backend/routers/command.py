"""
Command router — CRO Command View endpoints.
Pipeline health overview, alerts, and aggregate stats.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Deal, HealthScore, Justification

router = APIRouter()


def get_latest_health(deal: Deal) -> dict | None:
    if not deal.health_scores:
        return None
    latest = max(deal.health_scores, key=lambda h: h.computed_at)
    return {
        "overall_score": latest.overall_score,
        "dimensions": latest.dimensions,
        "risks": latest.risks,
        "gaps": latest.gaps,
        "agent_actions": latest.agent_actions,
        "computed_at": latest.computed_at.isoformat()
    }


@router.get("/pipeline")
def get_pipeline(db: Session = Depends(get_db)):
    """All deals with health scores for CRO view."""
    deals = db.query(Deal).all()
    result = []
    for deal in deals:
        health = get_latest_health(deal)
        just = deal.justification

        result.append({
            "id": deal.id,
            "company": deal.company,
            "contact_name": deal.contact_name,
            "contact_title": deal.contact_title,
            "deal_value": deal.deal_value,
            "stage": deal.stage,
            "archetype": deal.archetype,
            "rep_name": deal.rep_name,
            "health": health,
            "justification_status": {
                "completeness_score": just.completeness_score if just else 0,
                "agent_status": just.agent_status if just else "not_started",
                "last_updated": just.last_updated.isoformat() if just and just.last_updated else None
            },
            "signal_count": len(deal.signals)
        })

    # Sort by deal value descending
    result.sort(key=lambda x: x["deal_value"], reverse=True)
    return result


@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    """Deals needing immediate attention — score < 60 or specific critical gaps."""
    deals = db.query(Deal).all()
    alerts = []

    for deal in deals:
        health = get_latest_health(deal)
        if not health:
            continue

        deal_alerts = []

        # Score-based alerts
        if health["overall_score"] < 40:
            deal_alerts.append({
                "severity": "critical",
                "type": "low_health_score",
                "message": f"Overall deal health critically low: {health['overall_score']:.0f}/100"
            })
        elif health["overall_score"] < 60:
            deal_alerts.append({
                "severity": "high",
                "type": "low_health_score",
                "message": f"Deal health below threshold: {health['overall_score']:.0f}/100"
            })

        # Dimension-based alerts
        dims = health.get("dimensions", {})
        if dims.get("cfo_alignment", {}).get("score", 100) < 40:
            deal_alerts.append({
                "severity": "critical",
                "type": "cfo_misalignment",
                "message": f"CFO alignment critical: {dims['cfo_alignment']['score']}/100 — economic buyer not engaged"
            })
        if dims.get("objection_coverage", {}).get("score", 100) < 50:
            deal_alerts.append({
                "severity": "high",
                "type": "unaddressed_objections",
                "message": f"Objection coverage low: {dims['objection_coverage']['score']}/100 — key objections unanswered"
            })
        if dims.get("champion_strength", {}).get("score", 100) < 45:
            deal_alerts.append({
                "severity": "high",
                "type": "weak_champion",
                "message": f"Champion strength weak: {dims['champion_strength']['score']}/100 — insufficient internal advocacy"
            })

        # Gap-based alerts (look for critical keywords)
        for gap in health.get("gaps", []):
            gap_lower = gap.lower()
            if any(kw in gap_lower for kw in ["cfo", "cfr", "blocking", "security", "soc 2", "procurement"]):
                deal_alerts.append({
                    "severity": "high",
                    "type": "critical_gap",
                    "message": gap[:200]
                })

        if deal_alerts:
            alerts.append({
                "deal_id": deal.id,
                "company": deal.company,
                "deal_value": deal.deal_value,
                "stage": deal.stage,
                "overall_score": health["overall_score"],
                "alerts": deal_alerts[:5],  # Cap at 5 alerts per deal
                "top_risks": health.get("risks", [])[:2]
            })

    # Sort by severity and deal value
    def alert_priority(a):
        has_critical = any(al["severity"] == "critical" for al in a["alerts"])
        return (0 if has_critical else 1, -a["deal_value"])

    alerts.sort(key=alert_priority)
    return alerts


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Aggregate pipeline statistics for CRO view."""
    deals = db.query(Deal).all()

    total_pipeline_value = sum(d.deal_value for d in deals)
    total_deals = len(deals)

    health_scores = []
    at_risk_count = 0
    building_count = 0

    for deal in deals:
        health = get_latest_health(deal)
        if health:
            health_scores.append(health["overall_score"])
            if health["overall_score"] < 60:
                at_risk_count += 1

        if deal.justification and deal.justification.agent_status == "building":
            building_count += 1

    avg_health = sum(health_scores) / len(health_scores) if health_scores else 0

    # Stage breakdown
    stage_breakdown = {}
    for deal in deals:
        stage = deal.stage
        if stage not in stage_breakdown:
            stage_breakdown[stage] = {"count": 0, "value": 0}
        stage_breakdown[stage]["count"] += 1
        stage_breakdown[stage]["value"] += deal.deal_value

    # Completeness distribution
    completeness_buckets = {"0-30": 0, "31-60": 0, "61-90": 0, "91-100": 0}
    for deal in deals:
        score = deal.justification.completeness_score if deal.justification else 0
        if score <= 30:
            completeness_buckets["0-30"] += 1
        elif score <= 60:
            completeness_buckets["31-60"] += 1
        elif score <= 90:
            completeness_buckets["61-90"] += 1
        else:
            completeness_buckets["91-100"] += 1

    return {
        "total_pipeline_value": total_pipeline_value,
        "total_deals": total_deals,
        "avg_health_score": round(avg_health, 1),
        "at_risk_count": at_risk_count,
        "building_count": building_count,
        "healthy_count": sum(1 for s in health_scores if s >= 75),
        "stage_breakdown": stage_breakdown,
        "completeness_distribution": completeness_buckets
    }
