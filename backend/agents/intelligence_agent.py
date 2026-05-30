"""
Intelligence Agent — Extracts structured insights from deal signals using Claude.
Uses tool use to extract pain points, stakeholders, financial data, and objections.
"""
import json
import os
from typing import Optional
from anthropic import Anthropic
from pydantic import BaseModel

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an elite enterprise sales intelligence analyst with 20+ years of experience
analyzing B2B deal signals. Your job is to extract structured, actionable insights from sales calls,
emails, and meeting notes.

You excel at:
- Identifying unstated pain points and business drivers beneath surface-level complaints
- Recognizing stakeholder dynamics, champions, blockers, and their influence levels
- Extracting financial data, ROI signals, and cost-of-inaction indicators
- Cataloging objections with precision — noting exact quotes, who raised them, and context
- Assessing champion strength based on language, engagement patterns, and internal advocacy signals

Be highly specific. Use exact quotes where available. Assign confidence scores to your extractions.
When you see vague language, note the ambiguity rather than inventing specifics."""

TOOLS = [
    {
        "name": "extract_pain_points",
        "description": "Extract business pain points, challenges, and problems from the signal content. Include direct quotes, business impact estimates, and urgency signals.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pain_points": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string", "description": "Clear description of the pain point"},
                            "quote": {"type": "string", "description": "Direct quote from the signal if available"},
                            "business_impact": {"type": "string", "description": "Estimated business impact (revenue, cost, time)"},
                            "urgency": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
                            "department": {"type": "string", "description": "Department or function experiencing this pain"}
                        },
                        "required": ["description", "urgency"]
                    }
                }
            },
            "required": ["pain_points"]
        }
    },
    {
        "name": "identify_stakeholders",
        "description": "Identify all stakeholders mentioned or implied in the signal. Assess their role, influence, sentiment, and engagement level.",
        "input_schema": {
            "type": "object",
            "properties": {
                "stakeholders": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "title": {"type": "string"},
                            "role": {"type": "string", "enum": ["champion", "economic_buyer", "technical_buyer", "blocker", "influencer", "end_user"]},
                            "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative", "unknown"]},
                            "engagement_level": {"type": "string", "enum": ["high", "medium", "low", "unknown"]},
                            "key_concern": {"type": "string", "description": "Their primary concern or interest"},
                            "influence_score": {"type": "integer", "minimum": 1, "maximum": 10}
                        },
                        "required": ["name", "title", "role", "sentiment"]
                    }
                }
            },
            "required": ["stakeholders"]
        }
    },
    {
        "name": "extract_financials",
        "description": "Extract all financial data, cost information, ROI signals, budget mentions, and quantified business value from the signal.",
        "input_schema": {
            "type": "object",
            "properties": {
                "budget_mentioned": {"type": "boolean"},
                "budget_range": {"type": "string", "description": "Budget range if mentioned (e.g., '$200K-$300K', 'under $500K')"},
                "current_costs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string"},
                            "amount": {"type": "string"},
                            "frequency": {"type": "string", "enum": ["annual", "monthly", "one-time", "unknown"]}
                        },
                        "required": ["category", "amount"]
                    }
                },
                "roi_signals": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "metric": {"type": "string", "description": "The metric being measured (e.g., 'time savings', 'error reduction')"},
                            "current_state": {"type": "string"},
                            "target_state": {"type": "string"},
                            "estimated_value": {"type": "string"}
                        },
                        "required": ["metric", "current_state"]
                    }
                },
                "payback_sensitivity": {"type": "string", "description": "Notes on payback period sensitivity or concerns"},
                "finance_involvement": {"type": "boolean", "description": "Whether finance/CFO is involved in evaluation"}
            },
            "required": ["budget_mentioned", "finance_involvement"]
        }
    },
    {
        "name": "identify_objections",
        "description": "Identify all objections, concerns, hesitations, and blockers raised in the signal. Include who raised them and context.",
        "input_schema": {
            "type": "object",
            "properties": {
                "objections": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "objection": {"type": "string", "description": "The specific objection or concern"},
                            "raised_by": {"type": "string", "description": "Who raised this objection (name/title)"},
                            "category": {"type": "string", "enum": ["price", "roi", "integration", "security", "timeline", "vendor_risk", "internal_priority", "procurement", "competitive", "technical", "other"]},
                            "severity": {"type": "string", "enum": ["blocking", "significant", "minor"]},
                            "quote": {"type": "string", "description": "Direct quote if available"},
                            "addressed": {"type": "boolean", "description": "Whether this objection was addressed in the conversation"}
                        },
                        "required": ["objection", "category", "severity"]
                    }
                },
                "champion_strength_signal": {
                    "type": "object",
                    "properties": {
                        "score": {"type": "integer", "minimum": 1, "maximum": 10},
                        "evidence": {"type": "string", "description": "Specific evidence for this score"},
                        "coaching_quality": {"type": "string", "enum": ["excellent", "good", "adequate", "poor", "unknown"]},
                        "access_granted": {"type": "boolean", "description": "Whether champion is granting access to key stakeholders"}
                    },
                    "required": ["score", "evidence"]
                }
            },
            "required": ["objections", "champion_strength_signal"]
        }
    }
]


class InsightResult(BaseModel):
    pain_points: list
    stakeholders: list
    financial_data: dict
    objections: list
    champion_strength_signal: dict
    raw_tool_calls: list


async def analyze_signal(signal_content: str, signal_type: str, deal_context: dict) -> InsightResult:
    """
    Analyzes a deal signal using Claude with tool use to extract structured insights.
    Runs the full agent loop until Claude stops requesting tools.
    """
    deal_summary = f"""
Company: {deal_context.get('company', 'Unknown')}
Contact: {deal_context.get('contact_name', 'Unknown')} ({deal_context.get('contact_title', 'Unknown')})
Deal Value: ${deal_context.get('deal_value', 0):,.0f}
Stage: {deal_context.get('stage', 'Unknown')}
Archetype: {deal_context.get('archetype', 'Unknown')}
"""

    messages = [
        {
            "role": "user",
            "content": f"""Analyze this {signal_type} signal from the deal with:
{deal_summary}

Signal Content:
---
{signal_content}
---

Please use ALL four tools to extract comprehensive insights. Be thorough and specific."""
        }
    ]

    tool_results = {
        "pain_points": [],
        "stakeholders": [],
        "financial_data": {},
        "objections": [],
        "champion_strength_signal": {"score": 5, "evidence": "Insufficient data"},
        "raw_tool_calls": []
    }

    # Agent loop — keep calling until Claude stops requesting tools
    max_iterations = 10
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
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

        # Process tool use blocks
        tool_use_blocks = [block for block in response.content if block.type == "tool_use"]

        if not tool_use_blocks:
            # No more tool calls — we're done
            break

        # Collect tool results
        tool_results_for_message = []

        for tool_use in tool_use_blocks:
            tool_name = tool_use.name
            tool_input = tool_use.input

            tool_results["raw_tool_calls"].append({
                "tool": tool_name,
                "input": tool_input
            })

            # Store results by tool type
            if tool_name == "extract_pain_points":
                tool_results["pain_points"] = tool_input.get("pain_points", [])
            elif tool_name == "identify_stakeholders":
                tool_results["stakeholders"] = tool_input.get("stakeholders", [])
            elif tool_name == "extract_financials":
                tool_results["financial_data"] = tool_input
            elif tool_name == "identify_objections":
                tool_results["objections"] = tool_input.get("objections", [])
                if "champion_strength_signal" in tool_input:
                    tool_results["champion_strength_signal"] = tool_input["champion_strength_signal"]

            tool_results_for_message.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": json.dumps({"status": "success", "data": tool_input})
            })

        # Add assistant response and tool results to message history
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results_for_message})

        # If stop reason is end_turn, we're done
        if response.stop_reason == "end_turn":
            break

    return InsightResult(
        pain_points=tool_results["pain_points"],
        stakeholders=tool_results["stakeholders"],
        financial_data=tool_results["financial_data"],
        objections=tool_results["objections"],
        champion_strength_signal=tool_results["champion_strength_signal"],
        raw_tool_calls=tool_results["raw_tool_calls"]
    )
