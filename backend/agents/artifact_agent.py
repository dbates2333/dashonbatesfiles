"""
Artifact Agent — Builds complete deal justification artifacts using Claude.
Generates ROI models, exec summaries, procurement docs, and objection responses.
Supports streaming for real-time progress updates.
"""
import json
import os
from typing import AsyncGenerator, Optional
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a world-class enterprise deal strategist and business case architect.
You have helped close over $2B in enterprise software deals by crafting airtight justification artifacts.

Your artifacts are known for:
- ROI models that CFOs actually believe (conservative assumptions, documented sources, sensitivity analysis)
- Executive summaries that speak the language of the C-suite (strategic framing, not feature lists)
- Procurement documents that accelerate legal review (clear SLA commitments, SOC 2 references, DPA provisions)
- Objection responses that acknowledge concerns before dismantling them

You build from signals — call transcripts, emails, CRM data — and synthesize them into compelling business cases.
Every number you include should be traceable to a signal or a stated assumption. Never fabricate metrics.
When data is missing, you note the assumption and recommend validation steps."""

TOOLS = [
    {
        "name": "build_roi_model",
        "description": "Build a comprehensive ROI model with quantified costs, benefits, payback period, and 3-year NPV. Include conservative/base/optimistic scenarios.",
        "input_schema": {
            "type": "object",
            "properties": {
                "assumptions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "label": {"type": "string"},
                            "value": {"type": "string"},
                            "source": {"type": "string", "description": "Where this assumption came from (call, email, industry benchmark)"},
                            "confidence": {"type": "string", "enum": ["high", "medium", "low"]}
                        },
                        "required": ["label", "value", "source"]
                    }
                },
                "cost_components": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string"},
                            "annual_cost": {"type": "number"},
                            "description": {"type": "string"}
                        },
                        "required": ["category", "annual_cost"]
                    }
                },
                "benefit_components": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string"},
                            "annual_value": {"type": "number"},
                            "description": {"type": "string"},
                            "confidence": {"type": "string", "enum": ["high", "medium", "low"]}
                        },
                        "required": ["category", "annual_value", "description"]
                    }
                },
                "scenarios": {
                    "type": "object",
                    "properties": {
                        "conservative": {
                            "type": "object",
                            "properties": {
                                "three_year_roi_percent": {"type": "number"},
                                "payback_months": {"type": "number"},
                                "three_year_npv": {"type": "number"},
                                "annual_savings_year1": {"type": "number"},
                                "annual_savings_year2": {"type": "number"},
                                "annual_savings_year3": {"type": "number"}
                            }
                        },
                        "base": {
                            "type": "object",
                            "properties": {
                                "three_year_roi_percent": {"type": "number"},
                                "payback_months": {"type": "number"},
                                "three_year_npv": {"type": "number"},
                                "annual_savings_year1": {"type": "number"},
                                "annual_savings_year2": {"type": "number"},
                                "annual_savings_year3": {"type": "number"}
                            }
                        },
                        "optimistic": {
                            "type": "object",
                            "properties": {
                                "three_year_roi_percent": {"type": "number"},
                                "payback_months": {"type": "number"},
                                "three_year_npv": {"type": "number"},
                                "annual_savings_year1": {"type": "number"},
                                "annual_savings_year2": {"type": "number"},
                                "annual_savings_year3": {"type": "number"}
                            }
                        }
                    }
                },
                "total_investment": {"type": "number"},
                "implementation_cost": {"type": "number"},
                "annual_contract_value": {"type": "number"}
            },
            "required": ["assumptions", "cost_components", "benefit_components", "scenarios", "total_investment"]
        }
    },
    {
        "name": "write_exec_summary",
        "description": "Write a compelling executive summary for the deal justification. This is what the CFO and CEO will read. Must be strategic, concise, and compelling.",
        "input_schema": {
            "type": "object",
            "properties": {
                "exec_summary": {
                    "type": "string",
                    "description": "Full executive summary in markdown format. Should include: Strategic Context, Business Challenge, Proposed Solution, Financial Impact, Risk of Inaction, and Recommended Next Steps. 400-600 words."
                },
                "headline_metrics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "metric": {"type": "string"},
                            "value": {"type": "string"},
                            "context": {"type": "string"}
                        }
                    },
                    "description": "3-5 top-line metrics for the exec summary header"
                }
            },
            "required": ["exec_summary", "headline_metrics"]
        }
    },
    {
        "name": "create_procurement_doc",
        "description": "Create a formal procurement readiness document covering security, compliance, vendor risk, and contractual requirements.",
        "input_schema": {
            "type": "object",
            "properties": {
                "procurement_doc": {
                    "type": "string",
                    "description": "Full procurement document in markdown format. Must include: Vendor Overview, Security & Compliance (SOC 2 Type II, GDPR, data handling), SLA Commitments, Implementation Plan, Support Terms, Contract Highlights, and Procurement Checklist."
                },
                "compliance_certifications": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of compliance certifications available"
                },
                "key_sla_metrics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "metric": {"type": "string"},
                            "commitment": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["procurement_doc", "compliance_certifications", "key_sla_metrics"]
        }
    },
    {
        "name": "generate_objection_responses",
        "description": "Generate thorough, empathetic, evidence-based responses to each identified objection. Responses should acknowledge the concern before addressing it.",
        "input_schema": {
            "type": "object",
            "properties": {
                "objection_responses": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "objection": {"type": "string"},
                            "raised_by": {"type": "string"},
                            "category": {"type": "string"},
                            "response": {"type": "string", "description": "Full response — acknowledge, evidence, reframe, next step"},
                            "supporting_data": {"type": "string", "description": "Specific data points, case studies, or references to support the response"},
                            "follow_up_action": {"type": "string", "description": "Specific follow-up action to close this objection"},
                            "status": {"type": "string", "enum": ["addressed", "needs_follow_up", "escalated"]}
                        },
                        "required": ["objection", "response", "status"]
                    }
                }
            },
            "required": ["objection_responses"]
        }
    }
]


class JustificationResult(BaseModel):
    roi_model: dict
    exec_summary: str
    exec_summary_headline_metrics: list
    procurement_doc: str
    objection_responses: list
    completeness_score: int


async def build_justification(
    deal: dict,
    signals: list,
    historical_wins: Optional[list] = None
) -> AsyncGenerator[dict, None]:
    """
    Builds a complete deal justification artifact using Claude with tool use.
    Yields progress chunks for streaming.
    Returns the complete justification when done.
    """
    historical_context = ""
    if historical_wins:
        historical_context = f"\n\nHistorical wins to reference:\n" + "\n".join(
            f"- {w.get('company', 'Unknown')}: {w.get('outcome', '')}" for w in historical_wins[:3]
        )

    signals_text = ""
    for i, signal in enumerate(signals, 1):
        signals_text += f"\n\n--- Signal {i}: {signal.get('signal_type', 'unknown').upper()} ({signal.get('timestamp', 'unknown date')}) ---\n"
        signals_text += signal.get('content', '')
        if signal.get('extracted_insights'):
            insights = signal['extracted_insights']
            if insights.get('pain_points'):
                signals_text += f"\n[Extracted Pain Points: {', '.join(p.get('description', '') for p in insights['pain_points'][:3])}]"
            if insights.get('objections'):
                signals_text += f"\n[Objections: {', '.join(o.get('objection', '') for o in insights['objections'][:3])}]"

    messages = [
        {
            "role": "user",
            "content": f"""Build a complete deal justification artifact for this deal:

**Deal Details:**
- Company: {deal.get('company')}
- Contact: {deal.get('contact_name')} ({deal.get('contact_title')})
- Deal Value: ${deal.get('deal_value', 0):,.0f}
- Stage: {deal.get('stage')}
- Archetype: {deal.get('archetype')}

**Deal Signals:**
{signals_text}
{historical_context}

Please use ALL FOUR tools to build the complete justification package:
1. build_roi_model — Build the ROI model with conservative/base/optimistic scenarios
2. write_exec_summary — Write the executive summary
3. create_procurement_doc — Create the procurement readiness document
4. generate_objection_responses — Generate responses to all identified objections

Be thorough, specific, and use actual data from the signals where available."""
        }
    ]

    collected_results = {
        "roi_model": {},
        "exec_summary": "",
        "exec_summary_headline_metrics": [],
        "procurement_doc": "",
        "objection_responses": [],
    }

    tools_completed = []
    max_iterations = 15
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8192,
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

            # Yield progress update
            yield {
                "type": "tool_progress",
                "tool": tool_name,
                "message": f"Completing: {tool_name.replace('_', ' ').title()}..."
            }

            # Store results
            if tool_name == "build_roi_model":
                collected_results["roi_model"] = tool_input
                tools_completed.append("roi_model")
                yield {"type": "section_complete", "section": "roi_model", "data": tool_input}

            elif tool_name == "write_exec_summary":
                collected_results["exec_summary"] = tool_input.get("exec_summary", "")
                collected_results["exec_summary_headline_metrics"] = tool_input.get("headline_metrics", [])
                tools_completed.append("exec_summary")
                yield {"type": "section_complete", "section": "exec_summary", "data": tool_input}

            elif tool_name == "create_procurement_doc":
                collected_results["procurement_doc"] = tool_input.get("procurement_doc", "")
                tools_completed.append("procurement_doc")
                yield {"type": "section_complete", "section": "procurement_doc", "data": tool_input}

            elif tool_name == "generate_objection_responses":
                collected_results["objection_responses"] = tool_input.get("objection_responses", [])
                tools_completed.append("objection_responses")
                yield {"type": "section_complete", "section": "objections", "data": tool_input}

            tool_results_for_message.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": json.dumps({"status": "success"})
            })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results_for_message})

        if response.stop_reason == "end_turn":
            break

    # Calculate completeness score
    score = 0
    if collected_results["roi_model"] and collected_results["roi_model"].get("scenarios"):
        score += 30
    if collected_results["exec_summary"]:
        score += 25
    if collected_results["procurement_doc"]:
        score += 20
    if collected_results["objection_responses"]:
        score += 15
        addressed = sum(1 for o in collected_results["objection_responses"] if o.get("status") == "addressed")
        if addressed == len(collected_results["objection_responses"]) and len(collected_results["objection_responses"]) > 0:
            score += 10

    yield {
        "type": "complete",
        "result": JustificationResult(
            roi_model=collected_results["roi_model"],
            exec_summary=collected_results["exec_summary"],
            exec_summary_headline_metrics=collected_results["exec_summary_headline_metrics"],
            procurement_doc=collected_results["procurement_doc"],
            objection_responses=collected_results["objection_responses"],
            completeness_score=min(score, 100)
        )
    }
