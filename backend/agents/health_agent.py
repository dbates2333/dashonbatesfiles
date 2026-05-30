"""
Health Agent — Scores deal health across 5 dimensions using Claude.
Identifies risks, gaps, and recommends agent actions.
"""
import json
import os
from typing import Optional
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a senior enterprise sales strategist and deal risk analyst with deep expertise
in complex B2B sales cycles. You have reviewed thousands of enterprise deals and developed a sharp
instinct for identifying what makes deals succeed or fail at the last mile.

You assess deal health across five critical dimensions:
1. Business Case Strength — Is the ROI model compelling? Are the numbers credible? Has finance bought in?
2. Procurement Readiness — Is the vendor review process started? Security documentation ready? Legal aligned?
3. Objection Coverage — Have all material objections been identified and addressed with evidence?
4. Champion Strength — Is the internal champion visible, active, and well-equipped to sell internally?
5. CFO Alignment — Has the economic buyer been engaged? Do they understand and endorse the business case?

You give specific, actionable assessments — not vague platitudes. You cite evidence from the deal signals
when scoring. When you identify a gap, you describe exactly what is missing and why it matters.
When you recommend an action, it is specific, time-bound, and owner-assigned."""

TOOLS = [
    {
        "name": "score_dimension",
        "description": "Score one of the five health dimensions (0-100) with specific rationale tied to deal evidence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "dimension": {
                    "type": "string",
                    "enum": ["business_case_strength", "procurement_readiness", "objection_coverage", "champion_strength", "cfo_alignment"]
                },
                "score": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Score from 0-100 for this dimension"
                },
                "rationale": {
                    "type": "string",
                    "description": "Specific rationale for this score citing deal evidence"
                },
                "positive_signals": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Evidence supporting a higher score"
                },
                "negative_signals": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Evidence supporting concerns (score detractors)"
                }
            },
            "required": ["dimension", "score", "rationale"]
        }
    },
    {
        "name": "identify_risk",
        "description": "Identify a specific risk to the deal with severity rating and deadline sensitivity.",
        "input_schema": {
            "type": "object",
            "properties": {
                "risks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "risk": {"type": "string", "description": "Specific description of the risk"},
                            "severity": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
                            "dimension_affected": {"type": "string"},
                            "evidence": {"type": "string", "description": "What signals or data point to this risk"},
                            "deadline_sensitive": {"type": "boolean"},
                            "mitigation": {"type": "string", "description": "How this risk could be mitigated"}
                        },
                        "required": ["risk", "severity", "evidence"]
                    }
                }
            },
            "required": ["risks"]
        }
    },
    {
        "name": "identify_gap",
        "description": "Identify specific gaps in the deal justification — missing data, unaddressed objections, missing stakeholders, incomplete documentation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "gaps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "gap": {"type": "string", "description": "Specific description of what is missing"},
                            "impact": {"type": "string", "enum": ["deal_blocking", "significant", "moderate", "minor"]},
                            "category": {"type": "string", "enum": ["financial_data", "stakeholder_access", "objection_response", "documentation", "technical_validation", "executive_alignment", "procurement_requirement"]},
                            "recommended_fill": {"type": "string", "description": "Specific action to fill this gap"}
                        },
                        "required": ["gap", "impact", "category", "recommended_fill"]
                    }
                }
            },
            "required": ["gaps"]
        }
    },
    {
        "name": "suggest_action",
        "description": "Suggest specific agent actions to improve deal health, address gaps, or mitigate risks.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agent_actions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string", "description": "Specific action the agent should take or recommend"},
                            "priority": {"type": "string", "enum": ["immediate", "this_week", "next_week"]},
                            "action_type": {"type": "string", "enum": ["draft_content", "gather_data", "schedule_meeting", "update_artifact", "escalate", "research"]},
                            "expected_impact": {"type": "string", "description": "How this action will improve deal health"},
                            "owner": {"type": "string", "description": "Who should take this action (rep, agent, manager)"}
                        },
                        "required": ["action", "priority", "action_type", "expected_impact"]
                    }
                }
            },
            "required": ["agent_actions"]
        }
    }
]


class HealthScoreResult(BaseModel):
    overall_score: float
    dimensions: dict
    risks: list
    gaps: list
    agent_actions: list


async def score_deal_health(
    deal: dict,
    justification: Optional[dict],
    signals: list
) -> HealthScoreResult:
    """
    Scores deal health across 5 dimensions using Claude with tool use.
    Returns a HealthScore with all dimensions, risks, gaps, and recommended actions.
    """
    # Build signals summary
    signals_summary = ""
    for i, sig in enumerate(signals[-5:], 1):  # Last 5 signals
        signals_summary += f"\n\nSignal {i} ({sig.get('signal_type', 'unknown')}, {sig.get('timestamp', 'unknown')}):\n"
        signals_summary += sig.get('content', '')[:500]  # First 500 chars
        if sig.get('extracted_insights'):
            insights = sig['extracted_insights']
            if insights.get('objections'):
                obj_list = [o.get('objection', '') for o in insights['objections'][:3]]
                signals_summary += f"\nObjections raised: {'; '.join(obj_list)}"
            if insights.get('champion_strength_signal'):
                cs = insights['champion_strength_signal']
                signals_summary += f"\nChampion strength: {cs.get('score', '?')}/10 — {cs.get('evidence', '')}"

    # Build justification summary
    just_summary = "No justification built yet."
    if justification:
        just_summary = f"""
Completeness Score: {justification.get('completeness_score', 0)}%
Agent Status: {justification.get('agent_status', 'unknown')}
ROI Model: {'Present' if justification.get('roi_model') else 'Missing'}
Exec Summary: {'Present' if justification.get('exec_summary') else 'Missing'}
Procurement Doc: {'Present' if justification.get('procurement_doc') else 'Missing'}
Objection Responses: {len(justification.get('objection_responses') or []) if justification.get('objection_responses') else 0} responses
"""
        if justification.get('roi_model'):
            roi = justification['roi_model']
            if roi.get('scenarios', {}).get('base'):
                base = roi['scenarios']['base']
                just_summary += f"ROI (Base): {base.get('three_year_roi_percent', '?')}% | Payback: {base.get('payback_months', '?')} months | NPV: ${base.get('three_year_npv', 0):,.0f}\n"

    messages = [
        {
            "role": "user",
            "content": f"""Perform a comprehensive health assessment for this deal:

**Deal Details:**
- Company: {deal.get('company')}
- Contact: {deal.get('contact_name')} ({deal.get('contact_title')})
- Deal Value: ${deal.get('deal_value', 0):,.0f}
- Stage: {deal.get('stage')}
- Archetype: {deal.get('archetype')}

**Justification Status:**
{just_summary}

**Recent Deal Signals:**
{signals_summary if signals_summary else 'No signals recorded yet.'}

Please use ALL FOUR tools:
1. score_dimension — Call this 5 times, once for each dimension (business_case_strength, procurement_readiness, objection_coverage, champion_strength, cfo_alignment)
2. identify_risk — Identify 2-4 specific risks
3. identify_gap — Identify 2-5 specific gaps in the justification
4. suggest_action — Suggest 3-5 specific agent actions to improve deal health

Be precise, cite evidence from signals, and give scores that reflect the actual state of the deal."""
        }
    ]

    collected = {
        "dimensions": {
            "business_case_strength": {"score": 0, "rationale": ""},
            "procurement_readiness": {"score": 0, "rationale": ""},
            "objection_coverage": {"score": 0, "rationale": ""},
            "champion_strength": {"score": 0, "rationale": ""},
            "cfo_alignment": {"score": 0, "rationale": ""}
        },
        "risks": [],
        "gaps": [],
        "agent_actions": []
    }

    max_iterations = 15
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=6144,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            tools=TOOLS,
            messages=messages
        )

        tool_use_blocks = [block for block in response.content if block.type == "tool_use"]

        if not tool_use_blocks:
            break

        tool_results_for_message = []

        for tool_use in tool_use_blocks:
            tool_name = tool_use.name
            tool_input = tool_use.input

            if tool_name == "score_dimension":
                dimension = tool_input.get("dimension")
                if dimension and dimension in collected["dimensions"]:
                    collected["dimensions"][dimension] = {
                        "score": tool_input.get("score", 0),
                        "rationale": tool_input.get("rationale", ""),
                        "positive_signals": tool_input.get("positive_signals", []),
                        "negative_signals": tool_input.get("negative_signals", [])
                    }

            elif tool_name == "identify_risk":
                for risk in tool_input.get("risks", []):
                    collected["risks"].append(risk.get("risk", ""))

            elif tool_name == "identify_gap":
                for gap in tool_input.get("gaps", []):
                    collected["gaps"].append(gap.get("gap", ""))

            elif tool_name == "suggest_action":
                for action in tool_input.get("agent_actions", []):
                    collected["agent_actions"].append(action.get("action", ""))

            tool_results_for_message.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": json.dumps({"status": "success"})
            })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results_for_message})

        if response.stop_reason == "end_turn":
            break

    # Calculate overall score as weighted average
    dim_scores = [v["score"] for v in collected["dimensions"].values()]
    weights = [0.25, 0.15, 0.25, 0.20, 0.15]  # business_case, procurement, objections, champion, cfo
    overall = sum(s * w for s, w in zip(dim_scores, weights))

    return HealthScoreResult(
        overall_score=round(overall, 1),
        dimensions=collected["dimensions"],
        risks=collected["risks"],
        gaps=collected["gaps"],
        agent_actions=collected["agent_actions"]
    )
