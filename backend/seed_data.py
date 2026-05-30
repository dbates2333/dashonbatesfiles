"""
Seed data — 8 realistic enterprise deals with rich signals, justifications, and health scores.
"""
from datetime import datetime, timedelta
import json
from sqlalchemy.orm import Session
from models import Deal, DealSignal, Justification, HealthScore, AgentLog


def dt(days_ago: int, hours: int = 0) -> datetime:
    return datetime.utcnow() - timedelta(days=days_ago, hours=hours)


DEALS = [
    {
        "company": "Apex Manufacturing",
        "contact_name": "Sandra Kowalski",
        "contact_title": "VP of Operations",
        "deal_value": 340000,
        "stage": "business_case",
        "archetype": "CFO_led",
        "rep_name": "Marcus Chen"
    },
    {
        "company": "Meridian Health",
        "contact_name": "Dr. James Okafor",
        "contact_title": "Chief Medical Informatics Officer",
        "deal_value": 185000,
        "stage": "technical_eval",
        "archetype": "IT_led",
        "rep_name": "Priya Nair"
    },
    {
        "company": "Quantum Dynamics",
        "contact_name": "Rachel Thornton",
        "contact_title": "CFO",
        "deal_value": 520000,
        "stage": "legal",
        "archetype": "CFO_led",
        "rep_name": "Marcus Chen"
    },
    {
        "company": "Vertex Capital",
        "contact_name": "Anthony DeLuca",
        "contact_title": "Head of Technology",
        "deal_value": 95000,
        "stage": "discovery",
        "archetype": "Champion_driven",
        "rep_name": "Sarah Mills"
    },
    {
        "company": "Ironclad Logistics",
        "contact_name": "Brenda Hartley",
        "contact_title": "SVP Supply Chain",
        "deal_value": 280000,
        "stage": "business_case",
        "archetype": "Procurement_heavy",
        "rep_name": "Priya Nair"
    },
    {
        "company": "Nova Pharmaceuticals",
        "contact_name": "Dr. Kevin Walsh",
        "contact_title": "VP R&D Operations",
        "deal_value": 440000,
        "stage": "technical_eval",
        "archetype": "IT_led",
        "rep_name": "Sarah Mills"
    },
    {
        "company": "Sterling Financial",
        "contact_name": "Christine Park",
        "contact_title": "COO",
        "deal_value": 215000,
        "stage": "business_case",
        "archetype": "CFO_led",
        "rep_name": "Marcus Chen"
    },
    {
        "company": "Cascade Energy",
        "contact_name": "Tom Bergstrom",
        "contact_title": "Director of Digital Transformation",
        "deal_value": 175000,
        "stage": "discovery",
        "archetype": "Champion_driven",
        "rep_name": "Sarah Mills"
    }
]

SIGNALS = {
    "Apex Manufacturing": [
        {
            "signal_type": "call",
            "content": """Call Transcript — Discovery Call with Sandra Kowalski, VP Operations
Date: April 2, 2026 | Duration: 47 min | Attendees: Marcus Chen (AE), Sandra Kowalski (VP Ops), Derek Mills (IT Director)

Marcus: Sandra, thanks for making time. You mentioned on the intro call that you're running into some bottlenecks around the quarterly close process. Can you walk us through what that looks like right now?

Sandra: Sure. So we have 14 plants across the Midwest and Southeast, and every quarter close is basically a war. Each plant has its own reporting templates, half of them are still on Excel 2016, and my team spends the last 10 days of every quarter manually consolidating everything. Last quarter we found a $2.3M discrepancy in materials cost that took us 3 weeks to trace back to a misaligned formula in the Birmingham plant's spreadsheet.

Marcus: Three weeks to close a $2.3M discrepancy — what does that cost you in terms of delayed decisions?

Sandra: More than you'd think. Our CEO can't make capital allocation decisions until close is done, so we're pushing CapEx decisions by 4-6 weeks every quarter. We had a $4.7M equipment purchase for the Toledo facility sitting in limbo last cycle because we didn't have clean numbers. The vendor gave us a 30-day window and we missed it.

Derek: From IT's perspective, the bigger issue is the security risk. We're emailing spreadsheets with full P&L data around to 14 sites. No audit trail, no access controls, no versioning. Our CISO has flagged it twice in the last year.

Sandra: And we're about to go through an SOX audit. Our external auditors from PwC already flagged our consolidation process as a material weakness risk. That's a conversation our CFO — David Reyes — does not want to have in October.

Marcus: David Reyes is your CFO — has he been part of these conversations yet?

Sandra: Not directly, but this is absolutely on his radar. He told me at our last QBR that if I couldn't solve the consolidation problem before Q3 close, he was going to take ownership of it and go directly to procurement for a top-down solution. I'd rather we find something I can champion.

Marcus: That's helpful context. What would a successful outcome look like for you by Q3 close?

Sandra: Single source of truth across all 14 plants, close cycle under 5 days, and something I can show PwC that eliminates the material weakness flag. If you can do that, I can get David in the room.""",
            "timestamp": dt(58),
            "extracted_insights": {
                "pain_points": [
                    {"description": "Manual quarterly close process taking 10+ days across 14 plants", "quote": "my team spends the last 10 days of every quarter manually consolidating everything", "business_impact": "$4.7M equipment purchase missed vendor window due to delayed close", "urgency": "critical", "department": "Finance/Operations"},
                    {"description": "Spreadsheet-based consolidation causing material data discrepancies", "quote": "we found a $2.3M discrepancy in materials cost that took us 3 weeks to trace back", "business_impact": "$2.3M discrepancy, 3-week investigation", "urgency": "critical", "department": "Finance"},
                    {"description": "Security risk from emailing P&L spreadsheets with no audit trail", "quote": "No audit trail, no access controls, no versioning. Our CISO has flagged it twice", "business_impact": "SOX compliance risk, material weakness flag from PwC", "urgency": "high", "department": "IT/Security"}
                ],
                "stakeholders": [
                    {"name": "Sandra Kowalski", "title": "VP of Operations", "role": "champion", "sentiment": "positive", "engagement_level": "high", "key_concern": "Solving consolidation before Q3 close to maintain ownership vs CFO takeover", "influence_score": 7},
                    {"name": "David Reyes", "title": "CFO", "role": "economic_buyer", "sentiment": "neutral", "engagement_level": "low", "key_concern": "Eliminating material weakness risk before SOX audit, CapEx decision delays", "influence_score": 10},
                    {"name": "Derek Mills", "title": "IT Director", "role": "technical_buyer", "sentiment": "positive", "engagement_level": "medium", "key_concern": "Eliminating spreadsheet email security risk, audit trail", "influence_score": 6}
                ],
                "financial_data": {
                    "budget_mentioned": False,
                    "current_costs": [
                        {"category": "Operations staff time - quarterly close", "amount": "~$180K/year (est. 10 days × 14 plants)", "frequency": "annual"},
                        {"category": "Missed CapEx window (Toledo equipment)", "amount": "$4.7M delayed purchase", "frequency": "one-time"}
                    ],
                    "roi_signals": [
                        {"metric": "Close cycle reduction", "current_state": "10+ days", "target_state": "Under 5 days", "estimated_value": "4-6 weeks faster CapEx decisions"},
                        {"metric": "Data discrepancy investigation", "current_state": "$2.3M discrepancy, 3 week investigation", "target_state": "Real-time reconciliation", "estimated_value": "3 weeks of FTE time per quarter"}
                    ],
                    "finance_involvement": True,
                    "payback_sensitivity": "CFO David Reyes will need to approve — strong ROI story needed"
                },
                "objections": [],
                "champion_strength_signal": {"score": 7, "evidence": "Sandra is motivated to solve this before CFO takes over the problem. She's offering to bring in the CFO if solution is credible. Good coaching signals — shared internal urgency context."}
            }
        },
        {
            "signal_type": "call",
            "content": """Call Transcript — Business Case Review with Sandra Kowalski + David Reyes (CFO)
Date: April 12, 2026 | Duration: 38 min | Attendees: Marcus Chen (AE), Sandra Kowalski, David Reyes (CFO)

Marcus: David, appreciate you joining. We've been working with Sandra on quantifying the impact of the current close process. I want to walk you through what we've found and get your perspective.

David Reyes: Sure. I'll be direct with you — we get a lot of vendors in here. What I care about is payback period and total cost of ownership. Sandra tells me you're at $340K. Walk me through how you justify that.

Marcus: Absolutely. Based on what Sandra shared, your current close process costs roughly $180K per year in FTE time alone — that's 10 days × 3 FTEs × 14 plants at fully-loaded rates. Add in the $75K your team spent on the Birmingham discrepancy investigation last year, and you're at $255K in quantifiable costs annually.

David Reyes: That $180K number — where does that come from?

Sandra: I can validate that, David. I ran the FTE analysis. 12 people across corporate and plants, 10 days, and that's conservative. It doesn't include my time or Derek's team.

David Reyes: Okay. And the $340K — is that all year one? Or is there a multi-year commitment?

Marcus: Year one all-in including implementation. Year 2 and 3 are $115K annually for the enterprise license. So your 3-year total is $570K against a conservative $765K in savings — that's 34% ROI over 3 years, payback in 18 months.

David Reyes: Eighteen months. That's longer than I'd like. Our internal hurdle rate for OpEx tools is 12 months. I'm not saying no, but you need to sharpen the pencil. What am I missing in the savings side?

Sandra: David, we also have the PwC issue. If they flag the consolidation process as a material weakness in October, that's a remediation cost. Those aren't cheap.

David Reyes: That's a different conversation. I need to see the financial case stand on its own. Marcus, can you get me a revised model that shows the compliance cost avoidance separately and tightens the assumptions?

Marcus: Absolutely — I'll have a revised model to you by end of week.""",
            "timestamp": dt(48),
            "extracted_insights": {
                "pain_points": [
                    {"description": "CFO questioning 18-month payback period — below internal 12-month hurdle rate", "quote": "Eighteen months. That's longer than I'd like. Our internal hurdle rate for OpEx tools is 12 months.", "urgency": "critical", "department": "Finance"}
                ],
                "stakeholders": [
                    {"name": "David Reyes", "title": "CFO", "role": "economic_buyer", "sentiment": "neutral", "engagement_level": "medium", "key_concern": "Payback period must hit 12-month internal hurdle rate. Wants compliance cost avoidance modeled separately.", "influence_score": 10},
                    {"name": "Sandra Kowalski", "title": "VP Operations", "role": "champion", "sentiment": "positive", "engagement_level": "high", "key_concern": "PwC material weakness risk needs to be quantified", "influence_score": 7}
                ],
                "financial_data": {
                    "budget_mentioned": True,
                    "budget_range": "$340K year one, $115K/year thereafter",
                    "current_costs": [
                        {"category": "FTE close process costs", "amount": "$180K/year", "frequency": "annual"},
                        {"category": "Discrepancy investigation (Birmingham)", "amount": "$75K", "frequency": "annual"}
                    ],
                    "roi_signals": [
                        {"metric": "3-year ROI", "current_state": "18-month payback", "target_state": "Must reach 12-month hurdle", "estimated_value": "Need to quantify compliance cost avoidance"}
                    ],
                    "payback_sensitivity": "CFO explicit: 12-month internal hurdle rate. 18-month current model is below threshold. Need compliance cost avoidance model.",
                    "finance_involvement": True
                },
                "objections": [
                    {"objection": "18-month payback exceeds 12-month internal hurdle rate for OpEx tools", "raised_by": "David Reyes (CFO)", "category": "roi", "severity": "blocking", "quote": "Eighteen months. That's longer than I'd like. Our internal hurdle rate for OpEx tools is 12 months.", "addressed": False}
                ],
                "champion_strength_signal": {"score": 8, "evidence": "Sandra brought CFO into room and actively defended financials. Coach is equipped and advocating. CFO is engaged and giving clear requirements — positive signal."}
            }
        },
        {
            "signal_type": "email",
            "content": """From: Sandra Kowalski <s.kowalski@apexmfg.com>
To: Marcus Chen <m.chen@dealflowai.com>
Subject: Re: Revised ROI Model - Urgent
Date: April 18, 2026

Marcus,

Thanks for the revised model you sent Thursday. I reviewed it with David this morning.

Here's where we stand:
- David accepts the $255K annual savings baseline
- He is NOT yet accepting the compliance cost avoidance ($95K/year) because he says we haven't quantified what a material weakness remediation actually costs. He wants a reference — does your legal team have any benchmarks on SOX remediation costs for manufacturing companies our size?
- He's also asking whether we can do a phased implementation — pilot 3 plants in Q3, expand to all 14 in Q4. He thinks this gets payback to 11 months in year one. Is that something you can structure?

More urgently: our Q3 audit prep timeline got moved up. PwC is coming in August, not October. That means we need a decision by June 15 at the latest to have anything deployed before August 1.

If you can get David the SOX benchmark data and confirm the phased structure, I think we can get this done. He's willing to approve if payback clears the hurdle.

Sandra

P.S. Derek asked whether you have SOC 2 Type II certification. We'll need that for the IT security review regardless.""",
            "timestamp": dt(42),
            "extracted_insights": {
                "pain_points": [
                    {"description": "PwC audit timeline moved to August — decision deadline now June 15", "urgency": "critical", "business_impact": "Must deploy before August 1 or miss SOX audit window", "department": "Finance/Legal"}
                ],
                "stakeholders": [
                    {"name": "David Reyes", "title": "CFO", "role": "economic_buyer", "sentiment": "neutral", "engagement_level": "high", "key_concern": "Needs SOX remediation cost benchmark to accept compliance savings figure. Wants phased implementation to hit 11-month payback.", "influence_score": 10}
                ],
                "financial_data": {
                    "budget_mentioned": True,
                    "current_costs": [],
                    "roi_signals": [
                        {"metric": "Phased implementation payback", "current_state": "18 months full deployment", "target_state": "11 months with 3-plant pilot", "estimated_value": "Clears 12-month hurdle rate"}
                    ],
                    "payback_sensitivity": "CFO willing to approve if phased structure gets payback to 11 months. Needs SOX benchmark data.",
                    "finance_involvement": True
                },
                "objections": [
                    {"objection": "CFO not accepting compliance cost avoidance without SOX remediation cost benchmarks", "raised_by": "David Reyes (CFO)", "category": "roi", "severity": "significant", "addressed": False},
                    {"objection": "SOC 2 Type II certification required for IT security review", "raised_by": "Derek Mills (IT Director)", "category": "security", "severity": "significant", "addressed": False}
                ],
                "champion_strength_signal": {"score": 9, "evidence": "Sandra relaying CFO requirements clearly, coaching well, creating urgency with real deadline. Extremely strong champion behavior."}
            }
        }
    ],
    "Meridian Health": [
        {
            "signal_type": "call",
            "content": """Call Transcript — Technical Deep Dive: Meridian Health EHR Integration
Date: March 28, 2026 | Duration: 55 min | Attendees: Priya Nair (AE), Dr. James Okafor (CMIO), Raj Patel (Enterprise Architect)

Priya: Raj, Dr. Okafor, thanks for making time for the technical session. I know last week's demo raised some questions about the EHR integration layer. Can we start there?

Raj Patel: Sure. We're running Epic Clarity on-prem at all seven sites. The concern is how your platform handles the HL7 FHIR endpoints. Our current Epic version is 2022 and our IT team is protective of anything that touches the clinical data pipeline. What's the actual integration model?

Priya: Great question. Our platform uses SMART on FHIR R4 — we don't write to Epic, we read structured data via the FHIR API. No direct database connections, no HL7 v2 legacy messaging.

Raj Patel: Okay, SMART on FHIR is acceptable in principle. But we've had two third-party integrations go sideways in the last 18 months. One vendor caused a 4-hour clinical system degradation at our Hartford site. After that, our CIO — Linda Torres — requires a formal integration risk assessment for anything touching Epic. That's a 6-8 week process.

Dr. Okafor: From my side, the clinical staff workflow is the priority. Our hospitalists currently spend 2.2 hours per shift on documentation outside of Epic. That's 4 hours per physician per day if you count both shifts. We have 340 physicians. The math on that is not small.

Priya: Can you walk me through what that documentation looks like? Is it structured note-taking, or is it more administrative?

Dr. Okafor: Mix of both. Probably 70% is pulling data from Epic into our analytics dashboards manually — things that should be automated. The other 30% is narrative documentation that goes into a separate quality reporting system that doesn't talk to Epic. Our CMO wants to eliminate that second system entirely.

Raj Patel: Which is why the integration complexity matters. If we replace the quality system, it needs to be rock-solid. We can't afford another Hartford incident.""",
            "timestamp": dt(62),
            "extracted_insights": {
                "pain_points": [
                    {"description": "340 physicians spending 2.2 hours/shift on manual documentation outside Epic", "quote": "Our hospitalists currently spend 2.2 hours per shift on documentation outside of Epic", "business_impact": "~$3.2M/year in physician time (340 physicians × 2.2 hrs × $200/hr blended)", "urgency": "high", "department": "Clinical Operations"},
                    {"description": "Separate quality reporting system not integrated with Epic causing duplicate work", "urgency": "high", "department": "IT/Clinical"}
                ],
                "stakeholders": [
                    {"name": "Dr. James Okafor", "title": "CMIO", "role": "champion", "sentiment": "positive", "engagement_level": "high", "key_concern": "Reducing physician documentation burden, eliminating duplicate quality system", "influence_score": 8},
                    {"name": "Raj Patel", "title": "Enterprise Architect", "role": "technical_buyer", "sentiment": "neutral", "engagement_level": "medium", "key_concern": "Integration risk — previous incident caused 4-hour outage, CIO now requires formal risk assessment", "influence_score": 7},
                    {"name": "Linda Torres", "title": "CIO", "role": "blocker", "sentiment": "unknown", "engagement_level": "low", "key_concern": "Formal integration risk assessment required for anything touching Epic", "influence_score": 9}
                ],
                "financial_data": {
                    "budget_mentioned": False,
                    "roi_signals": [
                        {"metric": "Physician documentation time", "current_state": "2.2 hours/shift × 340 physicians", "target_state": "Reduce by 60%", "estimated_value": "~$3.2M/year"}
                    ],
                    "finance_involvement": False
                },
                "objections": [
                    {"objection": "CIO requires 6-8 week formal integration risk assessment for anything touching Epic after previous vendor caused 4-hour outage", "raised_by": "Raj Patel (Enterprise Architect)", "category": "integration", "severity": "blocking", "addressed": False}
                ],
                "champion_strength_signal": {"score": 7, "evidence": "Dr. Okafor is engaged and providing quantified business case. Good champion. But IT gatekeeper (Linda Torres/CIO) not yet engaged."}
            }
        },
        {
            "signal_type": "email",
            "content": """From: Raj Patel <r.patel@meridianhealth.org>
To: Priya Nair <p.nair@dealflowai.com>
Subject: Integration Risk Assessment Requirements
Date: April 5, 2026

Priya,

Following our call, I've confirmed the integration risk assessment requirements with Linda Torres (CIO). The formal process requires:

1. Security questionnaire (HITRUST CSF v11.2 — 328 questions)
2. Proof of SOC 2 Type II (current report within 12 months)
3. BAA (Business Associate Agreement) execution
4. Integration architecture diagram reviewed by our Epic Technical team
5. Penetration test results within 24 months
6. Disaster recovery runbook

Linda also wants to know if your platform is hosted on AWS GovCloud or equivalent. We have several federal grant programs that require data sovereignty.

Timeline: If you can get us items 1-3 by April 20, we can schedule the Epic architecture review for early May. Without that, we can't move to a procurement decision before July.

Dr. Okafor is supportive but this process is non-negotiable.

—Raj""",
            "timestamp": dt(54),
            "extracted_insights": {
                "pain_points": [],
                "stakeholders": [
                    {"name": "Linda Torres", "title": "CIO", "role": "blocker", "sentiment": "neutral", "engagement_level": "medium", "key_concern": "HITRUST CSF compliance, SOC 2 Type II, GovCloud data sovereignty", "influence_score": 9}
                ],
                "financial_data": {"budget_mentioned": False, "finance_involvement": False},
                "objections": [
                    {"objection": "HITRUST CSF v11.2 questionnaire (328 questions) required", "raised_by": "Linda Torres (CIO)", "category": "security", "severity": "blocking", "addressed": False},
                    {"objection": "Platform must be hosted on AWS GovCloud or equivalent for federal grant data sovereignty", "raised_by": "Linda Torres (CIO)", "category": "security", "severity": "significant", "addressed": False}
                ],
                "champion_strength_signal": {"score": 6, "evidence": "Dr. Okafor acknowledged as supportive but process gating from CIO is slowing progress. Champion needs to help expedite."}
            }
        }
    ],
    "Quantum Dynamics": [
        {
            "signal_type": "call",
            "content": """Call Transcript — Legal Review Kickoff: Quantum Dynamics
Date: April 20, 2026 | Duration: 42 min | Attendees: Marcus Chen (AE), Rachel Thornton (CFO), Patricia Sloane (General Counsel), Helen Wu (VP Procurement)

Rachel: Marcus, we're at the legal stage, so I want to be clear — business case is approved. The $520K is in the budget. This call is about getting through legal and procurement so we can execute before Q2 close.

Marcus: Understood, Rachel. That's exactly why we're here.

Patricia Sloane: I've reviewed the MSA you sent. There are four issues I need resolved before we can sign. First, the indemnification clause is mutual but our standard is vendor-side only. Second, your limitation of liability is capped at 12 months ACV — we need 24 months. Third, the data processing addendum needs to reference CCPA in addition to GDPR. And fourth, the auto-renewal clause requires 90-day notice — we need 120 days.

Marcus: Patricia, those are all negotiable. I'll get our legal team on points 1, 2, and 4 today. On the DPA — we do have a CCPA addendum, I just need to confirm it's included in the version we sent. Can I get you a redline by Thursday?

Patricia: Thursday works.

Helen Wu: From procurement, I need to flag the vendor security review. We're in the middle of rolling out our third-party risk program. Any new vendor above $100K requires a full TPRM assessment — we use BitSight and SecurityScorecard. Can you share your latest security ratings?

Marcus: Our BitSight score is 820 and SecurityScorecard is 92. I can send the documentation today.

Helen: Also, payment terms. Your standard is Net 30 — we pay Net 60 on all vendors. That's not negotiable on our side.

Rachel: Patricia, if legal is resolved by end of April, can we target a May 10 signature date?

Patricia: Doable if we get clean redlines. The indemnification language will take 3-4 business days on our side.""",
            "timestamp": dt(40),
            "extracted_insights": {
                "pain_points": [],
                "stakeholders": [
                    {"name": "Rachel Thornton", "title": "CFO", "role": "economic_buyer", "sentiment": "positive", "engagement_level": "high", "key_concern": "Execute before Q2 close — timeline is critical", "influence_score": 10},
                    {"name": "Patricia Sloane", "title": "General Counsel", "role": "blocker", "sentiment": "neutral", "engagement_level": "high", "key_concern": "4 specific legal redlines: indemnification, liability cap, CCPA DPA, auto-renewal notice", "influence_score": 8},
                    {"name": "Helen Wu", "title": "VP Procurement", "role": "blocker", "sentiment": "neutral", "engagement_level": "medium", "key_concern": "TPRM assessment, Net 60 payment terms", "influence_score": 7}
                ],
                "financial_data": {
                    "budget_mentioned": True,
                    "budget_range": "$520K approved",
                    "current_costs": [],
                    "finance_involvement": True
                },
                "objections": [
                    {"objection": "Indemnification clause must be vendor-side only (not mutual)", "raised_by": "Patricia Sloane (General Counsel)", "category": "procurement", "severity": "significant", "addressed": False},
                    {"objection": "Limitation of liability must be 24 months ACV not 12 months", "raised_by": "Patricia Sloane (General Counsel)", "category": "procurement", "severity": "significant", "addressed": False},
                    {"objection": "DPA must include CCPA reference", "raised_by": "Patricia Sloane (General Counsel)", "category": "procurement", "severity": "significant", "addressed": False},
                    {"objection": "Auto-renewal notice period must be 120 days not 90 days", "raised_by": "Patricia Sloane (General Counsel)", "category": "procurement", "severity": "minor", "addressed": False},
                    {"objection": "Full TPRM assessment required (BitSight/SecurityScorecard) for vendors >$100K", "raised_by": "Helen Wu (VP Procurement)", "category": "security", "severity": "significant", "addressed": False}
                ],
                "champion_strength_signal": {"score": 10, "evidence": "CFO is directly driving execution, budget is approved, she set May 10 target. This deal is in execution mode."}
            }
        }
    ],
    "Vertex Capital": [
        {
            "signal_type": "call",
            "content": """Call Transcript — Discovery: Vertex Capital Partners
Date: May 5, 2026 | Duration: 32 min | Attendees: Sarah Mills (AE), Anthony DeLuca (Head of Tech)

Sarah: Anthony, thanks for reaching out. You mentioned in your email that you're looking at automating your LP reporting process. Tell me more about what's driving that.

Anthony: We're a $3.2B private equity fund. Our LP reporting is completely manual right now — Excel models, PDFs, a lot of copy-paste from our portfolio monitoring system into quarterly packages. We have 87 LPs and our IR team is two people. Last quarter close took 22 days and both of them were working nights and weekends.

Sarah: 22 days — and are those 87 LP reports customized or templated?

Anthony: Most have some customization. Different LPs have different reporting requirements. Some want fund-level, some want by-company, some require co-investment carve-outs. It's a mess.

Sarah: Who else is involved in the decision here? Is this just an IT-led initiative or is your CFO aware?

Anthony: Right now it's just me driving it. I have buy-in from our Head of IR — Jessica Chen — and she's the one who really needs this. But the CFO, Michael Burnham, will need to sign off on anything. He's been pretty focused on cost control this year, so I want to have a really tight business case before I bring it to him.

Sarah: What's your budget thinking?

Anthony: Honestly I don't know yet. Jessica thinks the two IR people are worth way more than what we're paying if they weren't doing manual reports. But I don't have numbers. I need help building the case.""",
            "timestamp": dt(25),
            "extracted_insights": {
                "pain_points": [
                    {"description": "87 LPs with customized reporting requirements, entirely manual with 2-person IR team", "quote": "22 days and both of them were working nights and weekends", "business_impact": "22-day close cycle, IR team capacity maxed", "urgency": "high", "department": "Investor Relations"}
                ],
                "stakeholders": [
                    {"name": "Anthony DeLuca", "title": "Head of Technology", "role": "champion", "sentiment": "positive", "engagement_level": "high", "key_concern": "Needs tight business case before bringing to CFO", "influence_score": 6},
                    {"name": "Jessica Chen", "title": "Head of IR", "role": "influencer", "sentiment": "positive", "engagement_level": "medium", "key_concern": "IR team capacity, reporting accuracy", "influence_score": 7},
                    {"name": "Michael Burnham", "title": "CFO", "role": "economic_buyer", "sentiment": "unknown", "engagement_level": "low", "key_concern": "Cost control focus this year", "influence_score": 10}
                ],
                "financial_data": {"budget_mentioned": False, "finance_involvement": False},
                "objections": [],
                "champion_strength_signal": {"score": 5, "evidence": "Anthony is motivated but self-admittedly early stage. Needs help building business case. CFO not yet engaged. Medium champion strength."}
            }
        }
    ],
    "Ironclad Logistics": [
        {
            "signal_type": "call",
            "content": """Call Transcript — Business Case Review: Ironclad Logistics
Date: April 8, 2026 | Duration: 51 min | Attendees: Priya Nair (AE), Brenda Hartley (SVP Supply Chain), Victor Osei (Procurement Director), Linda Ramos (CFO)

Brenda: Priya, we've been working through the business case for six weeks now. My team has validated the numbers. Linda is here because procurement has some requirements we need to work through.

Victor Osei: Let me be direct. Our procurement process for software above $250K requires an RFP. We have three other vendors responding — SAP, Oracle, and a company called SupplyBridge. Our scoring committee evaluates on eight criteria. You're currently ranked second.

Priya: Victor, thank you for being direct. Who's ranked first right now?

Victor: SAP. They have an existing relationship — we're already on SAP ERP. Integration story is simpler on paper.

Linda Ramos: From a financial standpoint, our concern is implementation risk. The last two software projects we did — one $180K, one $340K — both went over budget by more than 30%. I've seen your implementation timeline: 16 weeks. What happens if we're at week 20 and we're not live?

Priya: Linda, that's a fair question. We have contractual implementation guarantees — if we miss the committed go-live date, we extend the contract by the same number of weeks at no charge and we assign a dedicated implementation PM at our cost.

Brenda: That's actually more than SAP offered.

Victor: SAP's integration story is stronger, but their implementation cost is $180K more. Priya, your differentiator needs to be clearer. Why you over SAP?

Linda: And if you can address the implementation risk contractually, I want that in writing before we score the RFP.""",
            "timestamp": dt(52),
            "extracted_insights": {
                "pain_points": [],
                "stakeholders": [
                    {"name": "Brenda Hartley", "title": "SVP Supply Chain", "role": "champion", "sentiment": "positive", "engagement_level": "high", "key_concern": "Getting to decision, validated business case", "influence_score": 8},
                    {"name": "Victor Osei", "title": "Procurement Director", "role": "blocker", "sentiment": "neutral", "engagement_level": "high", "key_concern": "RFP process, competitive evaluation — currently ranked 2nd behind SAP", "influence_score": 8},
                    {"name": "Linda Ramos", "title": "CFO", "role": "economic_buyer", "sentiment": "neutral", "engagement_level": "medium", "key_concern": "Implementation risk — 2 previous projects went 30%+ over budget", "influence_score": 10}
                ],
                "financial_data": {"budget_mentioned": True, "budget_range": "$280K", "finance_involvement": True},
                "objections": [
                    {"objection": "SAP has stronger integration story due to existing ERP relationship — currently ranked first in RFP scoring", "raised_by": "Victor Osei (Procurement Director)", "category": "competitive", "severity": "blocking", "addressed": False},
                    {"objection": "CFO concerned about implementation risk — 2 previous projects 30%+ over budget", "raised_by": "Linda Ramos (CFO)", "category": "vendor_risk", "severity": "significant", "addressed": True},
                    {"objection": "RFP process required — 3 other vendors responding, formal 8-criteria scoring", "raised_by": "Victor Osei", "category": "procurement", "severity": "significant", "addressed": False}
                ],
                "champion_strength_signal": {"score": 7, "evidence": "Brenda is a strong champion and has done the business case work. But procurement process is formal and SAP has home field advantage."}
            }
        },
        {
            "signal_type": "email",
            "content": """From: Victor Osei <v.osei@ironcladlogistics.com>
To: Priya Nair <p.nair@dealflowai.com>
Subject: RFP Scoring Update + Clarification Needed
Date: April 25, 2026

Priya,

Following this week's RFP scoring committee, I'm providing an update:

Current rankings:
1. DealFlow AI — 74.2 points (up from 2nd)
2. SAP SupplyChain Analytics — 71.8 points
3. SupplyBridge — 58.1 points
4. Oracle SCM Cloud — 52.4 points

You moved to first place largely on total cost of ownership (your implementation guarantee was a significant differentiator) and support model.

However, the committee flagged two items for clarification before final scoring:

1. Security: We need your SOC 2 Type II report and penetration test results. Our CISO, Robert Chin, will review. This is required for any vendor above $100K.

2. References: We need two customer references in logistics/supply chain at comparable scale (500+ employees, multi-DC environment). Please provide by May 5.

If these are resolved, I expect you will hold or improve your position for the final committee vote on May 12.

Victor Osei
Director of Procurement, Ironclad Logistics""",
            "timestamp": dt(35),
            "extracted_insights": {
                "pain_points": [],
                "stakeholders": [
                    {"name": "Victor Osei", "title": "Procurement Director", "role": "blocker", "sentiment": "positive", "engagement_level": "high", "key_concern": "SOC 2 Type II, logistics references needed before May 5", "influence_score": 8},
                    {"name": "Robert Chin", "title": "CISO", "role": "technical_buyer", "sentiment": "unknown", "engagement_level": "low", "key_concern": "SOC 2 Type II and pen test results", "influence_score": 7}
                ],
                "financial_data": {"budget_mentioned": False, "finance_involvement": False},
                "objections": [
                    {"objection": "SOC 2 Type II report and penetration test results required by CISO", "raised_by": "Robert Chin (CISO)", "category": "security", "severity": "blocking", "addressed": False},
                    {"objection": "Two logistics/supply chain references needed (500+ employees, multi-DC) by May 5", "raised_by": "Victor Osei", "category": "vendor_risk", "severity": "significant", "addressed": False}
                ],
                "champion_strength_signal": {"score": 7, "evidence": "Moved to first place in RFP — positive trajectory. Champion Brenda has clearly been advocating internally."}
            }
        }
    ],
    "Nova Pharmaceuticals": [
        {
            "signal_type": "call",
            "content": """Call Transcript — Technical Discovery: Nova Pharmaceuticals R&D Operations
Date: April 15, 2026 | Duration: 63 min | Attendees: Sarah Mills (AE), Dr. Kevin Walsh (VP R&D Ops), Sunil Kapoor (Head of Data Engineering), Maria Santos (Regulatory Affairs Director)

Dr. Walsh: The context is that we run 12 Phase II and Phase III clinical trials simultaneously. Each trial has its own data management system — different CROs, different EDC platforms (Medidata, Veeva Vault, some legacy Oracle Health Sciences). The problem is trial-level reporting to our executive team takes 2 weeks to compile. By the time we report, the data is stale.

Sarah: What decisions are being delayed because of that 2-week lag?

Dr. Walsh: Portfolio allocation. We have $340M in active R&D spend. Our CSO makes go/no-go decisions on trial continuation based on interim data. If that data is 2 weeks stale, she's making calls on imperfect information. Last year we had a Phase II trial that should have been stopped 3 weeks earlier — we estimate that cost us roughly $2.1M in unnecessary continuation spending.

Sunil: From a data engineering standpoint, we have 14 data pipelines, and 9 of them are maintained by one person. That's a key-person dependency risk. If she leaves, we have a problem.

Maria: Regulatory is my concern. FDA 21 CFR Part 11 compliance requires full audit trails on all data that goes into regulatory submissions. Some of what we're looking at would touch that pipeline.

Sarah: Maria, do you have FDA audit trail requirements today that you're meeting with existing systems?

Maria: Yes, but barely. Our last FDA inspection flagged two items on data traceability. We remediated them, but it's fragile. Any new system needs to be 21 CFR Part 11 compliant out of the box — we can't do a remediation project on top of an implementation.""",
            "timestamp": dt(45),
            "extracted_insights": {
                "pain_points": [
                    {"description": "2-week lag in R&D trial reporting causing stale data for go/no-go decisions on $340M portfolio", "quote": "our CSO makes go/no-go decisions on trial continuation based on interim data. If that data is 2 weeks stale...", "business_impact": "$2.1M in unnecessary Phase II trial continuation due to delayed decision", "urgency": "critical", "department": "R&D/Operations"},
                    {"description": "Key-person dependency: 9 of 14 data pipelines maintained by one person", "urgency": "high", "business_impact": "Business continuity risk if key person leaves", "department": "Data Engineering"}
                ],
                "stakeholders": [
                    {"name": "Dr. Kevin Walsh", "title": "VP R&D Operations", "role": "champion", "sentiment": "positive", "engagement_level": "high", "key_concern": "Real-time trial data for CSO portfolio decisions", "influence_score": 8},
                    {"name": "Sunil Kapoor", "title": "Head of Data Engineering", "role": "technical_buyer", "sentiment": "positive", "engagement_level": "medium", "key_concern": "Key-person risk on data pipelines", "influence_score": 6},
                    {"name": "Maria Santos", "title": "Regulatory Affairs Director", "role": "technical_buyer", "sentiment": "neutral", "engagement_level": "medium", "key_concern": "21 CFR Part 11 compliance — FDA recently flagged data traceability issues", "influence_score": 8}
                ],
                "financial_data": {
                    "budget_mentioned": False,
                    "roi_signals": [
                        {"metric": "Unnecessary trial continuation", "current_state": "$2.1M lost last year due to stale data", "target_state": "Real-time decision support", "estimated_value": "$2M+ per year"}
                    ],
                    "finance_involvement": False
                },
                "objections": [
                    {"objection": "Platform must be 21 CFR Part 11 compliant out of the box — FDA recently flagged data traceability, can't do remediation project simultaneously", "raised_by": "Maria Santos (Regulatory Affairs)", "category": "security", "severity": "blocking", "addressed": False}
                ],
                "champion_strength_signal": {"score": 7, "evidence": "Dr. Walsh has quantified the business case well. Strong technical team engagement. Regulatory compliance gating is a real blocker."}
            }
        }
    ],
    "Sterling Financial": [
        {
            "signal_type": "call",
            "content": """Call Transcript — Discovery: Sterling Financial Group
Date: April 22, 2026 | Duration: 44 min | Attendees: Marcus Chen (AE), Christine Park (COO)

Christine: Marcus, I'll give you the background. We're a $4.2B RIA. We've been growing through acquisition — 7 firms in the last 3 years. Each acquired firm brought its own CRM, its own reporting stack, its own compliance workflows. We have 4 different CRMs right now, none of them talking to each other.

Marcus: What's the operational impact of that?

Christine: Our advisor productivity is suffering. We have 280 advisors who are supposed to be serving clients, but they're spending an estimated 40% of their time on administrative workflows — reconciling client data across systems, generating reports manually. Our top quartile advisors are losing roughly $180K each per year in lost AUM time.

Marcus: Is there a technology budget allocated for this?

Christine: We have a $2.1M technology modernization budget for this fiscal year. This project is in scope. Our CFO — Andrew Kim — is the final approver. He's been burned by failed CRM migrations before, so he's going to ask hard questions about implementation risk.

Marcus: What happened with the previous CRM migration?

Christine: We tried to consolidate to Salesforce Financial Services Cloud 18 months ago. Got to week 10 of implementation, hit data migration issues with one of the acquired firms — the historical records were in a legacy format nobody anticipated. We paused the project. $420K spent, zero benefit realized. Andrew lost confidence in our ability to execute.

Marcus: That's really helpful context. What would it take to rebuild that confidence?

Christine: Phased approach, milestone-based payments, and contractual guarantees. Andrew wants skin in the game from the vendor.""",
            "timestamp": dt(38),
            "extracted_insights": {
                "pain_points": [
                    {"description": "4 different CRMs across 7 acquired firms with no integration — 280 advisors losing 40% of time to administrative workflows", "quote": "our top quartile advisors are losing roughly $180K each per year in lost AUM time", "business_impact": "$180K/advisor/year in lost productivity — estimated $50M+ total opportunity cost", "urgency": "high", "department": "Wealth Management Operations"}
                ],
                "stakeholders": [
                    {"name": "Christine Park", "title": "COO", "role": "champion", "sentiment": "positive", "engagement_level": "high", "key_concern": "Advisor productivity, successful implementation after previous failure", "influence_score": 8},
                    {"name": "Andrew Kim", "title": "CFO", "role": "economic_buyer", "sentiment": "negative", "engagement_level": "low", "key_concern": "Previous $420K CRM project failed — requires phased approach, milestone payments, vendor skin in the game", "influence_score": 10}
                ],
                "financial_data": {
                    "budget_mentioned": True,
                    "budget_range": "$2.1M technology modernization budget (this project in scope)",
                    "finance_involvement": True
                },
                "objections": [
                    {"objection": "CFO burned by previous CRM migration failure ($420K, zero benefit) — requires phased approach and milestone-based payments", "raised_by": "Andrew Kim (CFO)", "category": "vendor_risk", "severity": "blocking", "addressed": False},
                    {"objection": "Implementation risk from complex multi-CRM data migration across 7 acquired firm datasets", "raised_by": "Christine Park (COO)", "category": "integration", "severity": "significant", "addressed": False}
                ],
                "champion_strength_signal": {"score": 6, "evidence": "Christine is motivated and has budget context. But CFO is gun-shy from previous failure. Champion needs help building a credibility-first approach."}
            }
        }
    ],
    "Cascade Energy": [
        {
            "signal_type": "call",
            "content": """Call Transcript — Initial Discovery: Cascade Energy Partners
Date: May 12, 2026 | Duration: 29 min | Attendees: Sarah Mills (AE), Tom Bergstrom (Director of Digital Transformation)

Sarah: Tom, you came in through our LinkedIn ad about field operations digitization. What's the initiative you're working on?

Tom: We operate 340 natural gas distribution assets across the Pacific Northwest. Right now, 90% of our field maintenance records are paper-based. Work orders are on clipboards, compliance certifications are in binders, and our maintenance history database is 7 years out of date. Our regulatory exposure on that is real — we had an PHMSA inspection last year and got cited for records management.

Sarah: Was that a fine?

Tom: Not yet, but they put us on a corrective action plan. We have 18 months to modernize or face escalating penalties. The potential fine structure is $250K-$2M per incident. We had 3 incidents last year. That's the math.

Sarah: Who's driving the budget for this? Is there executive sponsorship?

Tom: I'm driving it internally. My sponsor is our VP of Operations, Greg Aldridge. We don't have a formal budget yet — this came out of the PHMSA corrective action response. I'm building the business case to get one approved by our board.

Sarah: What's your timeline for the board decision?

Tom: Our next board meeting is July 8. I need to have a proposal ready by June 20. If the board approves, we want to start implementation in Q3.""",
            "timestamp": dt(18),
            "extracted_insights": {
                "pain_points": [
                    {"description": "340 gas distribution assets with 90% paper-based maintenance records — PHMSA corrective action plan with 18-month deadline", "quote": "We had an PHMSA inspection last year and got cited for records management", "business_impact": "$250K-$2M per incident fine, 3 incidents last year = up to $6M exposure", "urgency": "critical", "department": "Operations/Compliance"}
                ],
                "stakeholders": [
                    {"name": "Tom Bergstrom", "title": "Director of Digital Transformation", "role": "champion", "sentiment": "positive", "engagement_level": "high", "key_concern": "Building board-ready business case for June 20", "influence_score": 5},
                    {"name": "Greg Aldridge", "title": "VP of Operations", "role": "influencer", "sentiment": "unknown", "engagement_level": "low", "key_concern": "Corrective action compliance", "influence_score": 7}
                ],
                "financial_data": {
                    "budget_mentioned": False,
                    "roi_signals": [
                        {"metric": "PHMSA fine avoidance", "current_state": "$250K-$2M per incident × 3 incidents", "target_state": "Full compliance eliminates fine risk", "estimated_value": "Up to $6M in avoided penalties"}
                    ],
                    "finance_involvement": False
                },
                "objections": [],
                "champion_strength_signal": {"score": 4, "evidence": "Tom is early stage, no budget approved, no CFO engagement yet. Low champion strength — building capability."}
            }
        }
    ]
}


def build_apex_justification():
    return {
        "roi_model": {
            "assumptions": [
                {"label": "FTE fully-loaded cost", "value": "$95/hour", "source": "Sandra Kowalski confirmed in April 2 call", "confidence": "high"},
                {"label": "Close process FTEs (corporate + plants)", "value": "12 FTEs", "source": "Sandra Kowalski, April 2 call", "confidence": "high"},
                {"label": "Days to close per quarter (current)", "value": "10 days", "source": "Sandra Kowalski, April 2 call", "confidence": "high"},
                {"label": "Close process reduction", "value": "60% (10 days → 4 days)", "source": "Customer benchmark from similar manufacturing deployments", "confidence": "medium"},
                {"label": "SOX remediation cost avoidance (material weakness)", "value": "$95K/year", "source": "Big 4 benchmarks for mid-market manufacturing", "confidence": "medium"},
                {"label": "Discount rate (NPV)", "value": "8%", "source": "Standard enterprise software NPV calculation", "confidence": "high"}
            ],
            "cost_components": [
                {"category": "Year 1 License + Implementation", "annual_cost": 340000, "description": "Full platform license plus implementation services, data migration, training"},
                {"category": "Year 2-3 Annual License", "annual_cost": 115000, "description": "Annual enterprise license renewal"}
            ],
            "benefit_components": [
                {"category": "Close Process FTE Savings", "annual_value": 182880, "description": "12 FTEs × 6 days saved per quarter × 4 quarters × $95/hr × 8hrs/day", "confidence": "high"},
                {"category": "Discrepancy Investigation Elimination", "annual_value": 75000, "description": "Estimated annual cost of manual reconciliation and error remediation (Birmingham incident baseline)", "confidence": "medium"},
                {"category": "CapEx Decision Acceleration", "annual_value": 47000, "description": "4-6 week faster CapEx decisions — opportunity cost of delayed capital deployment", "confidence": "low"},
                {"category": "SOX/Compliance Cost Avoidance", "annual_value": 95000, "description": "PwC material weakness remediation cost avoidance — Big 4 benchmark for mid-market manufacturing", "confidence": "medium"}
            ],
            "scenarios": {
                "conservative": {
                    "three_year_roi_percent": 31.2,
                    "payback_months": 18.4,
                    "three_year_npv": 132000,
                    "annual_savings_year1": 182880,
                    "annual_savings_year2": 257880,
                    "annual_savings_year3": 257880
                },
                "base": {
                    "three_year_roi_percent": 52.8,
                    "payback_months": 14.2,
                    "three_year_npv": 287400,
                    "annual_savings_year1": 257880,
                    "annual_savings_year2": 399880,
                    "annual_savings_year3": 399880
                },
                "optimistic": {
                    "three_year_roi_percent": 87.4,
                    "payback_months": 9.8,
                    "three_year_npv": 498600,
                    "annual_savings_year1": 399880,
                    "annual_savings_year2": 541880,
                    "annual_savings_year3": 541880
                }
            },
            "total_investment": 570000,
            "implementation_cost": 45000,
            "annual_contract_value": 340000
        },
        "exec_summary": """## Executive Summary: Apex Manufacturing — Operational Finance Transformation

### Strategic Context
Apex Manufacturing operates 14 production facilities across the Midwest and Southeast, generating significant quarterly reporting complexity that directly impedes executive decision-making velocity. The current state — a manual, spreadsheet-driven consolidation process — represents both a financial risk and a strategic liability as the business scales.

### Business Challenge
Each quarter, Apex's finance and operations teams spend 10+ days in a manual consolidation process involving 14 plant sites, 12 FTEs, and spreadsheets with no audit trail. This process produced a $2.3M materials cost discrepancy in Q3 2025 that required 3 weeks to investigate — during which time CEO-level capital allocation decisions were frozen. Most critically, a $4.7M equipment purchase for the Toledo facility expired during a close cycle delay.

**The stakes have increased**: PwC's timeline for the SOX audit has been accelerated to August 2026. PwC has already flagged Apex's consolidation process as a material weakness risk. Remediation outside of a technology solution would cost an estimated $95K+ annually and still not address the root cause.

### Proposed Solution
DealFlow AI's operational finance platform provides:
- Real-time multi-plant consolidation eliminating manual aggregation
- Role-based data access with full audit trail (SOX-compliant)
- Automated reconciliation with exception flagging
- CFO-ready close dashboards reducing review cycles

### Financial Impact
| Scenario | 3-Year ROI | Payback Period | 3-Year NPV |
|----------|-----------|----------------|------------|
| Conservative | 31.2% | 18.4 months | $132K |
| **Base Case** | **52.8%** | **14.2 months** | **$287K** |
| Optimistic | 87.4% | 9.8 months | $499K |

With the phased structure (3-plant pilot in Q3, full rollout Q4), year-1 payback reaches **11.1 months** — clearing Apex's 12-month internal hurdle rate.

### Risk of Inaction
- **PwC material weakness flag** in August 2026 SOX audit (decision deadline: June 15, 2026)
- Continued quarterly CapEx decision delays of 4-6 weeks
- Ongoing exposure to undiscovered data discrepancies in multi-plant P&L

### Recommended Next Steps
1. CFO signature on phased implementation SOW by June 10
2. Pilot plant selection (recommended: Toledo, Birmingham, Chicago) by June 17
3. Technical kickoff with Derek Mills' IT team: June 24""",
        "procurement_doc": """## Procurement & Vendor Readiness Document
### DealFlow AI × Apex Manufacturing

---

#### 1. Vendor Overview
**DealFlow AI, Inc.**
- Founded: 2021 | Employees: 340
- ARR: $47M | Customer Count: 280 enterprise customers
- Headquarters: San Francisco, CA
- Primary Contact: Marcus Chen, Enterprise Account Executive

---

#### 2. Security & Compliance

| Certification | Status | Report Date |
|--------------|--------|-------------|
| SOC 2 Type II | ✅ Current | March 2026 |
| ISO 27001 | ✅ Certified | January 2026 |
| GDPR | ✅ Compliant | N/A |
| CCPA | ✅ Compliant | N/A |

**Infrastructure:** AWS GovCloud-compatible, US-East hosting, AES-256 encryption at rest, TLS 1.3 in transit.

**Data Handling:** Customer data is logically isolated per tenant. No data used for model training. Full customer data export available within 48 hours of request. Data destruction within 30 days of contract termination.

**Access Controls:** SSO integration (SAML 2.0, Okta/Azure AD), MFA enforced, role-based access control with full audit logging.

---

#### 3. SLA Commitments

| Metric | Commitment |
|--------|-----------|
| Platform Uptime | 99.9% (measured monthly) |
| RTO | 4 hours |
| RPO | 1 hour |
| Support Response (P1) | 1 hour |
| Support Response (P2) | 4 hours |
| Support Response (P3) | 1 business day |

---

#### 4. Implementation Plan

**Phase 1 — Pilot (Q3 2026): 8 weeks**
- Weeks 1-2: Environment setup, SSO configuration, data model mapping
- Weeks 3-5: Toledo, Birmingham, Chicago plant data migration and validation
- Weeks 6-7: User acceptance testing with Sandra's finance team
- Week 8: Go-live, hypercare support

**Phase 2 — Full Rollout (Q4 2026): 8 weeks**
- Remaining 11 plants onboarded in 2 cohorts
- CFO dashboard configuration
- PwC audit documentation package

---

#### 5. Contract Highlights
- Term: 3 years with annual true-up
- Payment: Net 30 from invoice (flexible to Net 45 on request)
- Auto-renewal: 90-day notice required for cancellation
- Implementation guarantee: If go-live delayed beyond contracted date due to vendor fault, contract extended by equivalent days at no charge
- Data portability: Full export in standard formats (CSV, JSON) available on request""",
        "objection_responses": [
            {
                "objection": "18-month payback exceeds 12-month internal hurdle rate for OpEx tools",
                "raised_by": "David Reyes (CFO)",
                "category": "roi",
                "response": "David, you're absolutely right to hold us to the 12-month hurdle. Here's how we close that gap: the phased implementation structure (3-plant pilot in Q3, full rollout in Q4) means you realize savings from the three highest-volume plants in Q3 while the full investment is split across two quarters. On a cash-adjusted basis, year-1 payback drops from 18.4 months to 11.1 months.\n\nThe conservative model uses only the FTE savings and error remediation — it deliberately excludes the compliance cost avoidance because you wanted that substantiated separately. The SOX remediation benchmark from Big 4 firms for mid-market manufacturing with a material weakness flag ranges from $85K-$140K annually in external advisory costs. I can provide two reference letters from peer companies who went through this process. With that component included at the low end, base-case payback is 11.8 months even without the phased structure.\n\nAction: I'll send you (1) revised phased model showing 11.1-month payback and (2) SOX remediation benchmark references by Thursday.",
                "supporting_data": "Phased implementation model: $170K in Q3 savings (3 plants) against $170K investment tranche = break-even in Q3. Full-year payback of 11.1 months. SOX Big 4 benchmark: $85K-$140K annually for mid-market material weakness remediation.",
                "follow_up_action": "Send revised phased ROI model and SOX benchmark data to David Reyes by April 24",
                "status": "needs_follow_up"
            },
            {
                "objection": "SOC 2 Type II certification required for IT security review",
                "raised_by": "Derek Mills (IT Director)",
                "category": "security",
                "response": "Derek, we have a current SOC 2 Type II report (March 2026 — 12-month audit period). I'm attaching it to this response. The report covers Security, Availability, and Confidentiality trust service criteria.\n\nAdditionally, our platform holds ISO 27001 certification (January 2026) and we're compliant with GDPR and CCPA. All data is AES-256 encrypted at rest, TLS 1.3 in transit, and your Apex data will be logically isolated in its own tenant with no cross-customer data access. We support SSO via SAML 2.0 (Okta or Azure AD) with MFA enforcement and role-based access controls with full audit logging — which directly addresses the audit trail gap your CISO flagged.\n\nAction: Sending SOC 2 Type II report and security questionnaire responses today.",
                "supporting_data": "SOC 2 Type II report (March 2026), ISO 27001 certificate, GDPR/CCPA compliance documentation available immediately.",
                "follow_up_action": "Send SOC 2 Type II report and complete security package to Derek Mills",
                "status": "addressed"
            }
        ],
        "completeness_score": 72,
        "agent_status": "needs_review"
    }


def build_quantum_justification():
    return {
        "roi_model": {
            "assumptions": [
                {"label": "Budget approved", "value": "$520K all-in", "source": "Rachel Thornton (CFO) confirmed April 20 call", "confidence": "high"},
                {"label": "Current data operations cost", "value": "$2.1M/year (8 FTE data analysts)", "source": "Rachel Thornton Q3 business case review", "confidence": "high"},
                {"label": "Process efficiency gain", "value": "65%", "source": "Average across 12 comparable deployments", "confidence": "high"},
                {"label": "Discount rate", "value": "8%", "source": "Standard", "confidence": "high"}
            ],
            "cost_components": [
                {"category": "Year 1 License + Implementation", "annual_cost": 520000, "description": "Full platform + enterprise implementation"},
                {"category": "Year 2-3 Annual License", "annual_cost": 175000, "description": "Annual renewal"}
            ],
            "benefit_components": [
                {"category": "Data Analyst FTE Savings", "annual_value": 1365000, "description": "8 FTEs × $262.5K fully loaded × 65% efficiency redeployment", "confidence": "high"},
                {"category": "Revenue Acceleration", "annual_value": 380000, "description": "2-week faster reporting cycles enabling earlier strategic decisions", "confidence": "medium"}
            ],
            "scenarios": {
                "conservative": {
                    "three_year_roi_percent": 142,
                    "payback_months": 5.8,
                    "three_year_npv": 1820000,
                    "annual_savings_year1": 910000,
                    "annual_savings_year2": 1365000,
                    "annual_savings_year3": 1365000
                },
                "base": {
                    "three_year_roi_percent": 196,
                    "payback_months": 4.1,
                    "three_year_npv": 2540000,
                    "annual_savings_year1": 1365000,
                    "annual_savings_year2": 1745000,
                    "annual_savings_year3": 1745000
                },
                "optimistic": {
                    "three_year_roi_percent": 248,
                    "payback_months": 3.2,
                    "three_year_npv": 3180000,
                    "annual_savings_year1": 1745000,
                    "annual_savings_year2": 2125000,
                    "annual_savings_year3": 2125000
                }
            },
            "total_investment": 870000,
            "implementation_cost": 68000,
            "annual_contract_value": 520000
        },
        "exec_summary": """## Executive Summary: Quantum Dynamics — Data Operations Modernization

### Status: Legal Review In Progress — Expected Close May 10, 2026

Quantum Dynamics has completed business case approval with CFO Rachel Thornton and is in final legal review. The $520K engagement has been approved in budget. This summary is provided for internal reference during contract execution.

### Business Case Summary
Quantum Dynamics operates a $2.1M/year data operations function with 8 data analysts supporting enterprise reporting. The platform delivers 65% efficiency gains across this function, generating $1.37M in annual savings against a $520K investment — a 4.1-month payback on the base case.

### Open Legal Items (as of April 20, 2026)
1. Indemnification clause — redline in progress, due April 24
2. Limitation of liability — negotiating 24-month ACV cap
3. DPA CCPA addendum — confirmed available, being incorporated
4. Auto-renewal notice period — 90 → 120 days, accepted in principle

### Target Close: May 10, 2026""",
        "procurement_doc": """## Procurement Document: Quantum Dynamics

**Status:** IN LEGAL REVIEW

### Vendor Due Diligence — Complete
- SOC 2 Type II: ✅ Provided (March 2026)
- Security questionnaire: ✅ Complete
- TPRM Assessment: ✅ BitSight 820, SecurityScorecard 92
- BAA: Not required (no PHI)
- Insurance certificates: ✅ Provided

### Contract Red Lines — In Progress
| Item | Status | Owner |
|------|--------|-------|
| Indemnification (vendor-side only) | In negotiation | Legal (Patricia Sloane) |
| Liability cap (24-month ACV) | In negotiation | Legal |
| CCPA DPA addendum | Drafted by vendor | Awaiting signature |
| 120-day auto-renewal notice | Agreed in principle | Legal |
| Net 60 payment terms | Accepted by vendor | Procurement (Helen Wu) |

### Target Signature: May 10, 2026""",
        "objection_responses": [
            {
                "objection": "Indemnification clause must be vendor-side only (not mutual)",
                "raised_by": "Patricia Sloane (General Counsel)",
                "category": "procurement",
                "response": "Patricia, our standard MSA is mutual indemnification reflecting our belief that both parties bear responsibility for their own actions. However, we recognize that Quantum's standard is vendor-side indemnification and we're prepared to accept that position with a carve-out: we retain the right to seek indemnification from you in cases of gross negligence or willful misconduct on your side. Our legal team is preparing a redline today for your review by April 24.",
                "follow_up_action": "Legal team to deliver redline MSA by April 24",
                "status": "needs_follow_up"
            },
            {
                "objection": "Limitation of liability must be 24 months ACV not 12 months",
                "raised_by": "Patricia Sloane (General Counsel)",
                "category": "procurement",
                "response": "We can accept 24-month ACV limitation of liability. Our standard 12-month cap reflects our risk model, but given the size of this engagement and Quantum's profile, we'll move to 18 months as our compromise position — this is the position we hold with 85% of enterprise accounts. If Patricia needs 24 months, we'll require an annual cap on aggregate liability of 2× ACV. Sending this position in the redline.",
                "follow_up_action": "Include 18-month liability cap (or 24-month with 2× ACV aggregate) in redline",
                "status": "needs_follow_up"
            },
            {
                "objection": "DPA must include CCPA reference",
                "raised_by": "Patricia Sloane (General Counsel)",
                "category": "procurement",
                "response": "Confirmed. Our standard DPA includes GDPR compliance provisions. Our CCPA addendum is a separate document that we're incorporating into the contract package. I've already requested our legal team add it to the redline. This should be a straightforward addition with no negotiation required.",
                "follow_up_action": "Attach CCPA addendum to redline DPA",
                "status": "addressed"
            },
            {
                "objection": "Auto-renewal notice period must be 120 days not 90 days",
                "raised_by": "Patricia Sloane (General Counsel)",
                "category": "procurement",
                "response": "Accepted. We'll update the auto-renewal notice period to 120 days in the redline. No issue on our side.",
                "follow_up_action": "Update contract language to 120 days",
                "status": "addressed"
            },
            {
                "objection": "Full TPRM assessment required (BitSight/SecurityScorecard) for vendors above $100K",
                "raised_by": "Helen Wu (VP Procurement)",
                "category": "security",
                "response": "Our current BitSight score is 820 (A rating) and SecurityScorecard is 92/100 (A). I'll send the official documentation with current ratings today. We also have a current SOC 2 Type II report and are happy to complete any supplemental security questionnaire your CISO requires.",
                "supporting_data": "BitSight: 820 (A rating). SecurityScorecard: 92/100 (A). SOC 2 Type II: March 2026.",
                "follow_up_action": "Send BitSight/SecurityScorecard documentation to Helen Wu today",
                "status": "addressed"
            }
        ],
        "completeness_score": 95,
        "agent_status": "complete"
    }


def build_meridian_justification():
    return {
        "roi_model": {
            "assumptions": [
                {"label": "Physicians impacted", "value": "340 hospitalists", "source": "Dr. Okafor, March 28 call", "confidence": "high"},
                {"label": "Documentation time per shift", "value": "2.2 hours", "source": "Dr. Okafor, March 28 call", "confidence": "high"},
                {"label": "Physician blended fully-loaded rate", "value": "$200/hour", "source": "Healthcare industry benchmark", "confidence": "medium"},
                {"label": "Time savings from automation", "value": "60% of documentation time", "source": "Healthcare AI benchmark — 3 comparable deployments", "confidence": "medium"}
            ],
            "cost_components": [
                {"category": "Year 1 License + Implementation", "annual_cost": 185000, "description": "Full platform with Epic FHIR integration"},
                {"category": "Year 2-3 Annual License", "annual_cost": 68000, "description": "Annual renewal"}
            ],
            "benefit_components": [
                {"category": "Physician Time Recovery", "annual_value": 2995200, "description": "340 physicians × 2.2 hrs × 60% saved × 365 days × 2 shifts / 2 × $200/hr", "confidence": "medium"},
                {"category": "Quality System Elimination", "annual_value": 140000, "description": "Annual cost of operating separate quality reporting system", "confidence": "medium"}
            ],
            "scenarios": {
                "conservative": {
                    "three_year_roi_percent": 387,
                    "payback_months": 2.8,
                    "three_year_npv": 5820000,
                    "annual_savings_year1": 1497600,
                    "annual_savings_year2": 2995200,
                    "annual_savings_year3": 3135200
                },
                "base": {
                    "three_year_roi_percent": 498,
                    "payback_months": 2.1,
                    "three_year_npv": 7640000,
                    "annual_savings_year1": 2995200,
                    "annual_savings_year2": 3135200,
                    "annual_savings_year3": 3135200
                },
                "optimistic": {
                    "three_year_roi_percent": 612,
                    "payback_months": 1.8,
                    "three_year_npv": 9420000,
                    "annual_savings_year1": 3275200,
                    "annual_savings_year2": 3415200,
                    "annual_savings_year3": 3415200
                }
            },
            "total_investment": 321000,
            "implementation_cost": 32000,
            "annual_contract_value": 185000
        },
        "exec_summary": """## Executive Summary: Meridian Health — Clinical Documentation Transformation

### The Opportunity
Meridian Health's 340 hospitalists spend 2.2 hours per shift — approximately 35% of their time — on documentation activities outside of Epic. At fully-loaded physician rates, this represents $2.9M in annual productivity loss. More critically, this burden is directly correlated with physician burnout and is limiting Meridian's capacity to serve its patient population.

### Integration Path
The platform integrates via SMART on FHIR R4 (read-only), requiring no Epic write access and preserving all existing clinical workflows. We've completed 12 SMART on FHIR integrations with Epic 2022 environments without incident. We will complete CIO Linda Torres' formal integration risk assessment process in parallel with technical scoping.

### Financial Case
Base case: 498% ROI over 3 years, 2.1-month payback. Conservative case (40% efficiency gain vs. 60%) still delivers 387% ROI and 2.8-month payback.

### Status
In technical evaluation — integration risk assessment in progress. Target decision: late May 2026.""",
        "procurement_doc": None,
        "objection_responses": [
            {
                "objection": "CIO requires 6-8 week formal integration risk assessment for anything touching Epic after previous vendor caused 4-hour outage",
                "raised_by": "Raj Patel / Linda Torres (CIO)",
                "category": "integration",
                "response": "We fully respect Linda's governance process and have completed this assessment with comparable healthcare systems. Our SMART on FHIR R4 integration is read-only — we do not write to Epic, trigger clinical workflows, or touch the care delivery pipeline. The previous incident was caused by a vendor using direct HL7 v2 database connections. Our architecture is categorically different.\n\nWe've prepared a complete integration architecture document for the Epic Technical team review, including: (1) FHIR API call frequency limits (staying within Epic's recommended bounds), (2) circuit breaker implementation that automatically disconnects if Epic response times degrade, (3) separate API credentials with read-only scopes. We're ready to schedule the Epic architecture review at Linda's earliest convenience.",
                "supporting_data": "12 completed Epic SMART on FHIR integrations, zero clinical incidents. Architecture document available for Linda Torres' review.",
                "follow_up_action": "Schedule Epic architecture review with Raj Patel and Linda Torres for early May",
                "status": "needs_follow_up"
            }
        ],
        "completeness_score": 45,
        "agent_status": "needs_review"
    }


def build_ironclad_justification():
    return {
        "roi_model": {
            "assumptions": [
                {"label": "Current manual supply chain process cost", "value": "$1.2M/year", "source": "Brenda Hartley business case validation", "confidence": "high"},
                {"label": "Process efficiency improvement", "value": "40%", "source": "Logistics industry benchmark", "confidence": "medium"}
            ],
            "cost_components": [
                {"category": "Year 1 License + Implementation", "annual_cost": 280000, "description": "Full platform + supply chain integration"},
                {"category": "Year 2-3 Annual License", "annual_cost": 98000, "description": "Annual renewal"}
            ],
            "benefit_components": [
                {"category": "Supply Chain Process Savings", "annual_value": 480000, "description": "40% efficiency on $1.2M annual process costs", "confidence": "high"},
                {"category": "Inventory Optimization", "annual_value": 180000, "description": "3-5% reduction in excess inventory carrying costs", "confidence": "medium"}
            ],
            "scenarios": {
                "conservative": {
                    "three_year_roi_percent": 68,
                    "payback_months": 9.8,
                    "three_year_npv": 481000,
                    "annual_savings_year1": 320000,
                    "annual_savings_year2": 480000,
                    "annual_savings_year3": 480000
                },
                "base": {
                    "three_year_roi_percent": 112,
                    "payback_months": 7.2,
                    "three_year_npv": 744000,
                    "annual_savings_year1": 480000,
                    "annual_savings_year2": 660000,
                    "annual_savings_year3": 660000
                },
                "optimistic": {
                    "three_year_roi_percent": 148,
                    "payback_months": 5.8,
                    "three_year_npv": 980000,
                    "annual_savings_year1": 660000,
                    "annual_savings_year2": 840000,
                    "annual_savings_year3": 840000
                }
            },
            "total_investment": 476000,
            "implementation_cost": 42000,
            "annual_contract_value": 280000
        },
        "exec_summary": """## Executive Summary: Ironclad Logistics — Supply Chain Operations

### Competitive Position
DealFlow AI currently leads the Ironclad RFP scoring with 74.2 points vs. SAP at 71.8 points, driven by total cost of ownership advantage and implementation guarantee. Final committee vote is May 12.

### Differentiation vs. SAP
- $180K lower total implementation cost
- Contractual go-live guarantee (SAP does not offer)
- Purpose-built supply chain analytics vs. SAP's broader ERP module
- Implementation timeline: 16 weeks vs. SAP's 24 weeks

### Financial Case
Base case: 112% ROI over 3 years, 7.2-month payback. Brenda Hartley's team has validated the savings assumptions.

### Open Items to Close
1. SOC 2 Type II and pen test results → CISO Robert Chin (due May 5)
2. Two logistics references (500+ employees, multi-DC) → May 5
3. SAP counter-offer likely before May 12 committee vote""",
        "procurement_doc": None,
        "objection_responses": [
            {
                "objection": "SAP has stronger integration story due to existing ERP relationship — currently ranked first in RFP scoring",
                "raised_by": "Victor Osei",
                "category": "competitive",
                "response": "The SAP integration advantage is real on paper but overstated in practice. SAP's supply chain analytics module requires significant customization to work with non-SAP data sources — and Ironclad has three non-SAP operational systems (fleet management, WMS, TMS). The integration story for SAP means 6-8 months of SI work on top of the implementation timeline, plus ongoing SAP consultant dependency. Our platform has native connectors for all three of Ironclad's existing systems, delivered out of the box.\n\nMost importantly: SAP's implementation risk. Ironclad's CFO Linda Ramos flagged that two previous implementations went 30%+ over budget. SAP ERP implementations historically overrun by an industry average of 47% per Gartner. Our contractual implementation guarantee eliminates that risk exposure.",
                "supporting_data": "Gartner: ERP implementation overruns average 47%. Our implementation guarantee: if delayed, contract extended at no charge. SAP does not offer equivalent.",
                "follow_up_action": "Prepare competitive battlecard specific to SAP and share with Brenda Hartley for internal advocacy",
                "status": "needs_follow_up"
            }
        ],
        "completeness_score": 65,
        "agent_status": "needs_review"
    }


HEALTH_SCORES = {
    "Apex Manufacturing": {
        "overall_score": 58.0,
        "dimensions": {
            "business_case_strength": {"score": 72, "rationale": "Strong cost baseline validated by Sandra Kowalski. ROI model built with actual FTE data. CFO engaged and gave specific requirements. Gap: 18-month payback below 12-month hurdle — phased structure closes this to 11 months but hasn't been formally resubmitted.", "positive_signals": ["CFO engaged directly in business case review", "FTE costs validated by champion", "PwC timeline creates real urgency"], "negative_signals": ["18-month payback below 12-month internal hurdle rate", "SOX compliance savings not yet accepted by CFO", "Revised model not yet formally delivered"]},
            "procurement_readiness": {"score": 45, "rationale": "SOC 2 Type II requested but not confirmed delivered. IT security review initiated by Derek Mills but not yet completed. No legal or procurement engagement yet — deal is at business case stage.", "positive_signals": ["SOC 2 Type II available (March 2026)"], "negative_signals": ["SOC 2 not yet sent to Derek Mills", "No legal review initiated", "Procurement not yet engaged"]},
            "objection_coverage": {"score": 52, "rationale": "Main CFO objection (payback period) has a solution path (phased model) but revised materials not delivered. SOC 2 objection has a clear answer but documentation not sent. Both objections remain technically open.", "positive_signals": ["Clear solution path for both objections", "Champion is coaching the approach"], "negative_signals": ["CFO payback objection unresolved — revised model not delivered", "SOC 2 documentation not sent to Derek Mills", "Decision deadline June 15 creates risk"]},
            "champion_strength": {"score": 78, "rationale": "Sandra Kowalski is an exceptional champion — brought CFO into room, actively relays requirements, coaches on internal dynamics, and has real skin in the game (CFO takeover threat). Her April 18 email demonstrates high-quality intelligence sharing.", "positive_signals": ["Brought CFO into business case review", "Proactively shared audit timeline acceleration", "Providing coaching on CFO requirements"], "negative_signals": ["Champion's ability to influence CFO is limited to business case — procurement and legal not yet in scope"]},
            "cfo_alignment": {"score": 38, "rationale": "CFO David Reyes engaged and gave specific requirements — positive. However, he has NOT accepted the ROI model. He explicitly rejected the 18-month payback and demanded a revised model with SOX benchmark data. Until revised model is delivered and accepted, CFO alignment is conditional at best.", "positive_signals": ["CFO attended business case review", "Gave specific, actionable feedback", "Indicated willingness to approve if hurdle rate met"], "negative_signals": ["18-month payback explicitly rejected", "Compliance savings not accepted without benchmark data", "Revised model still pending as of April 18 email"]}
        },
        "risks": [
            "CRITICAL: June 15 decision deadline — PwC audit moved to August. If revised ROI model not delivered and approved by early June, deal misses window entirely.",
            "CFO payback objection unaddressed: David Reyes explicitly questioned 18-month payback on April 12 call. Revised model with phased structure not confirmed delivered as of last signal (April 18).",
            "SOC 2 Type II not yet sent to Derek Mills — IT security review cannot proceed without it, blocking procurement pathway.",
            "Competitive risk: If CFO searches for alternatives due to delayed response, SAP or Oracle could enter the conversation before June 15."
        ],
        "gaps": [
            "Revised ROI model with phased structure (11-month payback) and SOX benchmark data not confirmed delivered to David Reyes — this is the deal's #1 blocker.",
            "SOC 2 Type II documentation package not sent to Derek Mills (IT Director) — required to initiate security review track.",
            "No formal procurement or legal engagement initiated despite June 15 deadline — 6-8 week contract process needs to start immediately.",
            "Compliance cost avoidance ($95K/year) not yet validated with SOX remediation cost benchmarks — CFO will not accept without this data."
        ],
        "agent_actions": [
            "URGENT: Draft revised ROI model email with phased implementation analysis (11.1-month payback) and SOX remediation benchmark references for Marcus Chen to send to David Reyes by April 24.",
            "Send SOC 2 Type II report and full security package to Derek Mills today — this must happen before June 15 security review can complete.",
            "Create timeline warning: Deal must reach legal/procurement stage by May 10 to execute before June 15 deadline. Recommend Marcus Chen escalate to manager.",
            "Research and compile 2-3 SOX remediation cost references from comparable manufacturing companies to substantiate $95K compliance savings figure."
        ]
    },
    "Meridian Health": {
        "overall_score": 47.5,
        "dimensions": {
            "business_case_strength": {"score": 68, "rationale": "Strong quantified ROI — 340 physicians × 2.2 hrs/shift is a compelling number. ROI model built. However, CFO/finance not yet engaged. Business case approval will require healthcare finance leadership involvement.", "positive_signals": ["Physician time savings quantified ($2.9M/year)", "Two-use case framing (documentation + quality system elimination)", "ROI model complete"], "negative_signals": ["No CFO/finance engagement", "Integration concerns could delay implementation and reduce first-year savings"]},
            "procurement_readiness": {"score": 22, "rationale": "HITRUST CSF questionnaire (328 questions), SOC 2 Type II, BAA, Epic architecture review, pen test results, and DR runbook all required. None confirmed submitted. GovCloud data sovereignty question outstanding. This is a 6-8 week process with significant documentation requirements.", "positive_signals": ["Security requirements clearly defined by Raj Patel", "Explicit timeline: items 1-3 by April 20 to hit May schedule"], "negative_signals": ["HITRUST CSF 328 questions not yet started", "SOC 2 not confirmed submitted", "BAA not yet executed", "GovCloud hosting not confirmed", "Epic architecture review not scheduled"]},
            "objection_coverage": {"score": 38, "rationale": "Primary technical objection (integration risk / CIO governance process) has been addressed conceptually with SMART on FHIR architecture explanation. But CIO Linda Torres has not received or accepted this response. HITRUST and GovCloud requirements not addressed.", "positive_signals": ["Integration architecture response prepared"], "negative_signals": ["CIO Linda Torres not yet directly engaged", "HITRUST CSF response not submitted", "GovCloud hosting answer outstanding", "Integration risk assessment not yet scheduled"]},
            "champion_strength": {"score": 58, "rationale": "Dr. Okafor is a strong clinical champion but his authority is limited by IT/CIO gating. He acknowledged being supportive but 'the process is non-negotiable.' He needs to actively sponsor the vendor relationship through the risk assessment process.", "positive_signals": ["Dr. Okafor has quantified the physician pain", "Technical team (Raj Patel) is engaged and providing specific requirements"], "negative_signals": ["CIO Linda Torres is the real gatekeeper and has not been directly engaged", "Dr. Okafor has not publicly sponsored the vendor through CIO's process"]},
            "cfo_alignment": {"score": 35, "rationale": "CFO not engaged. Finance not part of the evaluation. At $185K this deal likely doesn't require CFO sign-off at Meridian, but CMIO needs to confirm approval path and budget availability.", "positive_signals": ["Deal size ($185K) may not require CFO-level approval"], "negative_signals": ["No budget confirmation", "No finance engagement", "Approval path not mapped"]}
        },
        "risks": [
            "Integration risk assessment gating: Raj Patel explicitly stated 6-8 week process with Linda Torres (CIO) approval required. Deal cannot move to procurement without this — and the clock hasn't started.",
            "HITRUST CSF v11.2 questionnaire (328 questions) not yet started — this is the most time-consuming procurement requirement and needs to begin immediately.",
            "GovCloud hosting question unanswered — if platform is not on GovCloud-equivalent, deal may be structurally blocked for federal grant data programs.",
            "Budget not confirmed — no finance engagement and no budget approval signal. At $185K, this needs to be validated."
        ],
        "gaps": [
            "HITRUST CSF v11.2 questionnaire (328 questions) not submitted — required before integration risk assessment can proceed.",
            "GovCloud data sovereignty question from CIO Linda Torres outstanding — must answer before architecture review can be scheduled.",
            "CIO Linda Torres not directly engaged — all communications through Raj Patel. Need direct executive relationship with IT leadership.",
            "Budget / finance approval path not mapped — who signs the PO at Meridian for a $185K software investment?"
        ],
        "agent_actions": [
            "Start HITRUST CSF v11.2 questionnaire completion — assign to security team immediately. This is the critical path gating item.",
            "Research and confirm GovCloud hosting capability / compliance — answer CIO's data sovereignty question.",
            "Request meeting with CIO Linda Torres through Dr. Okafor — executive-to-executive security and integration conversation.",
            "Map Meridian Health approval path for $185K software purchase — confirm budget holder and approval timeline."
        ]
    },
    "Quantum Dynamics": {
        "overall_score": 89.5,
        "dimensions": {
            "business_case_strength": {"score": 96, "rationale": "Business case fully approved by CFO Rachel Thornton. $520K in budget. ROI model complete with conservative/base/optimistic scenarios. Strong financial framing. This is a done deal on the business side.", "positive_signals": ["CFO personally driving execution", "Budget explicitly confirmed as approved", "ROI model complete and accepted", "CFO set May 10 target date"], "negative_signals": ["None material"]},
            "procurement_readiness": {"score": 88, "rationale": "Active legal negotiation on 4 specific items. TPRM assessment initiated. BitSight/SecurityScorecard scores available. Deal is deep in procurement process — this is good procurement readiness, not a gap.", "positive_signals": ["Legal review actively in progress", "TPRM assessment documented (BitSight 820, SS 92)", "4 legal items specifically identified and being addressed"], "negative_signals": ["Indemnification and liability cap still in negotiation — risk of deadlock"]},
            "objection_coverage": {"score": 92, "rationale": "All 5 legal objections have been addressed or are actively being negotiated. CCPA DPA confirmed. Auto-renewal accepted. Net 60 accepted. Only open items are indemnification and liability cap — both have clear negotiating positions.", "positive_signals": ["5 of 5 objections with documented response", "3 of 5 already accepted/resolved", "Clear negotiating position on remaining 2"], "negative_signals": ["Indemnification negotiation could delay if no compromise found"]},
            "champion_strength": {"score": 92, "rationale": "CFO Rachel Thornton is directly managing execution. Highest possible champion strength — economic buyer is the champion.", "positive_signals": ["CFO is personally attending legal calls", "CFO set May 10 target date", "CFO aligned all parties in one room"], "negative_signals": ["None"]},
            "cfo_alignment": {"score": 98, "rationale": "CFO is the champion. Budget approved. Business case accepted. She is driving the timeline. Perfect CFO alignment.", "positive_signals": ["CFO attended legal kickoff", "Budget confirmed approved", "Target date set by CFO"], "negative_signals": ["None"]}
        },
        "risks": [
            "Legal negotiation delay: Indemnification (mutual vs. vendor-side) and liability cap (12 vs. 24 months ACV) could deadlock if legal teams don't agree by late April — jeopardizing May 10 target.",
            "Procurement TPRM holdout: If Robert Chin (CISO) finds issues with security documentation, could add 1-2 weeks to timeline.",
            "Q2 close urgency creates artificial pressure — if May 10 slips, Rachel may lose internal momentum for Q2 close."
        ],
        "gaps": [
            "Legal redline for indemnification clause not yet delivered — promised by April 24, needs to be a priority.",
            "CCPA DPA addendum attachment to redline not yet confirmed complete.",
            "18-month liability cap counter-position not yet formally communicated to Patricia Sloane."
        ],
        "agent_actions": [
            "PRIORITY: Ensure legal redline is delivered to Patricia Sloane by April 24 EOD — include indemnification, liability cap (18-month proposal), CCPA DPA addendum, and 120-day auto-renewal.",
            "Send BitSight and SecurityScorecard documentation to Helen Wu today to unblock TPRM review.",
            "Prepare escalation plan if legal items not resolved by April 30 — Rachel Thornton should be briefed on risk to May 10 target.",
            "Confirm Net 60 payment terms are documented in contract and communicated to Helen Wu."
        ]
    },
    "Vertex Capital": {
        "overall_score": 31.0,
        "dimensions": {
            "business_case_strength": {"score": 28, "rationale": "Business case not yet built. Deal is in early discovery. Anthony acknowledged needing help building the case. No ROI model, no exec summary, no financial validation. Jessica Chen (Head of IR) is supportive but not quantified.", "positive_signals": ["Pain point identified (22-day close, 2-person IR team)", "Champion aware of CFO's cost-control focus"], "negative_signals": ["No ROI model", "No financial data collected", "CFO not engaged", "No budget confirmed"]},
            "procurement_readiness": {"score": 5, "rationale": "Deal is in discovery. No procurement process initiated. No vendor requirements communicated.", "positive_signals": [], "negative_signals": ["No procurement engagement", "No technical requirements", "No security requirements"]},
            "objection_coverage": {"score": 15, "rationale": "No objections formally raised yet, but CFO's known cost-control focus is a pre-emptive concern. No objection responses prepared.", "positive_signals": ["Anthony is proactively building the case before CFO engagement"], "negative_signals": ["CFO's cost-control posture not yet addressed", "No objection preparation"]},
            "champion_strength": {"score": 48, "rationale": "Anthony DeLuca has good intent but limited authority. He acknowledged needing to build a business case before approaching CFO. Jessica Chen (Head of IR) is the actual end-user champion. Neither has CFO access demonstrated.", "positive_signals": ["Anthony is self-motivated", "Jessica Chen has visible pain and is supportive"], "negative_signals": ["Anthony admitted he doesn't have CFO-level authority yet", "No demonstrated path to economic buyer", "No budget confirmation from CFO level"]},
            "cfo_alignment": {"score": 8, "rationale": "CFO Michael Burnham completely unengaged. Known to be focused on cost control. No budget committed. No business case presented. Anthony specifically said he needs help building the case before bringing it to CFO.", "positive_signals": ["CFO focus on cost control means ROI-driven pitch will resonate if numbers are strong"], "negative_signals": ["CFO not engaged at all", "No budget confirmed", "Previous approach is bottom-up with no CFO sponsorship"]}
        },
        "risks": [
            "No path to economic buyer: Anthony has not demonstrated he can get Michael Burnham (CFO) into the conversation. Deal could stall indefinitely without executive sponsorship.",
            "Deal is in early discovery with no urgency signal — 'nice to have' risk is high. No board mandate, no compliance deadline, no competitive pressure.",
            "Jessica Chen (Head of IR) is the real champion but hasn't been directly engaged in the sales process yet.",
            "CFO is focused on cost control — without a bulletproof business case, deal will not move forward."
        ],
        "gaps": [
            "ROI model not built — this is the critical path to CFO engagement. Need to quantify: IR FTE value ($X per person), close cycle reduction (22 days → target), and LP customization cost.",
            "Jessica Chen (Head of IR) not yet a direct participant in the deal — she needs to be brought in as a champion alongside Anthony.",
            "No urgency identified — deal needs a compelling event (upcoming board meeting, LP request, hiring pressure) to create momentum.",
            "Budget not confirmed — need explicit budget discussion with Anthony to qualify the deal."
        ],
        "agent_actions": [
            "Build ROI model for Anthony immediately — quantify IR FTE time savings, LP reporting customization cost, and close cycle reduction. Give Anthony the business case he needs.",
            "Request introduction to Jessica Chen (Head of IR) through Anthony — she is the real end-user champion and needs to be in the process.",
            "Identify urgency: Ask Anthony when the next LP reporting cycle is, whether there are any investor requests driving urgency, or if there's a board-level initiative.",
            "Schedule CFO pre-engagement: Coach Anthony on how to position the business case to Michael Burnham, focusing on cost-per-LP-report and competitive LP service quality."
        ]
    },
    "Ironclad Logistics": {
        "overall_score": 64.5,
        "dimensions": {
            "business_case_strength": {"score": 78, "rationale": "Business case validated by Brenda Hartley's team over 6 weeks. ROI model built with logistics industry benchmarks. CFO Linda Ramos engaged and gave implementation risk requirements. Strong fundamentals.", "positive_signals": ["6 weeks of business case validation", "CFO engaged and gave specific requirements", "Competitive position: first place in RFP scoring"], "negative_signals": ["Implementation risk objection still concerns CFO despite contractual guarantee not yet in writing"]},
            "procurement_readiness": {"score": 62, "rationale": "Active RFP process — first place in scoring. SOC 2 Type II and pen test results requested by May 5. References requested by May 5. CISO review required. This is an active procurement process with clear requirements.", "positive_signals": ["First place in RFP scoring (74.2 vs. SAP 71.8)", "Clear requirements from Victor Osei", "May 5 deadlines are actionable"], "negative_signals": ["SOC 2 and pen test not yet confirmed submitted", "References not yet identified/submitted", "CISO Robert Chin not yet satisfied"]},
            "objection_coverage": {"score": 55, "rationale": "Competitive objection (SAP) has a response prepared but battlecard not yet shared with Brenda for internal advocacy. SOC 2 objection not yet resolved. References not yet provided. Implementation risk partially addressed (verbal guarantee) but CFO wants it in writing.", "positive_signals": ["Competitive response prepared and credible", "Implementation guarantee offered (strong differentiator vs. SAP)"], "negative_signals": ["SOC 2 and references not yet submitted", "Implementation guarantee not yet in writing per CFO Linda Ramos"]},
            "champion_strength": {"score": 72, "rationale": "Brenda Hartley is a strong champion who drove 6 weeks of business case work and brought CFO and Procurement into the process. Her internal advocacy has moved deal to first place in RFP. Solid champion with demonstrated internal influence.", "positive_signals": ["Brought CFO and Procurement into formal evaluation", "6 weeks of business case work completed", "Deal moved to first place in RFP"], "negative_signals": ["Cannot directly influence procurement scoring — Victor Osei controls that process"]},
            "cfo_alignment": {"score": 55, "rationale": "CFO Linda Ramos is engaged and gave clear requirements. Implementation risk concern partially addressed but wants contractual guarantee in writing. Budget ($280K) appears allocated for winner of RFP.", "positive_signals": ["CFO is part of formal evaluation", "Budget allocated for RFP winner"], "negative_signals": ["Implementation guarantee not yet in written contract language", "CFO has history of project cost overruns (30%+) — still cautious"]}
        },
        "risks": [
            "May 5 deadline for SOC 2 and references is 10 days away — if missed, CISO Robert Chin review cannot complete before May 12 committee vote.",
            "SAP counter-offer risk: SAP will almost certainly respond aggressively before May 12. SAP's existing ERP relationship gives them home-field advantage with procurement.",
            "Implementation guarantee needs to be in contract language before CFO Linda Ramos will accept it — verbal commitment from last call is insufficient.",
            "RFP lead is narrow (74.2 vs. 71.8) — any stumble on SOC 2, references, or SAP's counter could flip the result."
        ],
        "gaps": [
            "SOC 2 Type II report and pen test results not submitted to CISO Robert Chin — due May 5, critical path.",
            "Two logistics references (500+ employees, multi-DC) not yet identified or submitted — due May 5.",
            "Implementation guarantee not in formal contract language — CFO Linda Ramos specifically requested written contractual guarantee.",
            "Competitive battlecard vs. SAP not shared with Brenda Hartley for internal advocacy — needed before May 12 committee vote."
        ],
        "agent_actions": [
            "IMMEDIATE: Submit SOC 2 Type II and pen test results to CISO Robert Chin today — May 5 deadline cannot slip.",
            "IMMEDIATE: Identify and confirm two logistics references (500+ employees, multi-DC environment) and submit to Victor Osei by May 5.",
            "Prepare written implementation guarantee language for inclusion in contract — share with Brenda Hartley and Patricia Sloane draft today.",
            "Create SAP competitive battlecard and share with Brenda Hartley for internal advocacy before May 12 committee vote."
        ]
    },
    "Nova Pharmaceuticals": {
        "overall_score": 53.0,
        "dimensions": {
            "business_case_strength": {"score": 72, "rationale": "Strong quantified pain: $2.1M in unnecessary trial continuation from stale data, $340M portfolio at stake. R&D Operations champion has good metrics. However, CFO not engaged, budget not confirmed.", "positive_signals": ["$2.1M quantified cost from stale decision-making", "$340M portfolio creates urgency for accurate data", "Two-use-case framing (trial reporting + key-person risk)"], "negative_signals": ["Budget not confirmed", "No CFO engagement", "Implementation timeline concern from 21 CFR Part 11 requirements"]},
            "procurement_readiness": {"score": 35, "rationale": "21 CFR Part 11 compliance is the primary gating requirement. FDA previously flagged data traceability. Maria Santos (Regulatory Affairs) not yet satisfied that platform is compliant out of the box. No formal vendor assessment initiated.", "positive_signals": ["Requirements clearly identified"], "negative_signals": ["21 CFR Part 11 compliance not yet demonstrated", "Regulatory Affairs not yet satisfied", "No formal vendor assessment process initiated", "HITRUST may also be required for pharmaceutical"]},
            "objection_coverage": {"score": 42, "rationale": "Primary regulatory objection (21 CFR Part 11) has not been formally addressed. Maria Santos expressed concern directly and set a clear requirement. No response prepared.", "positive_signals": ["Objection clearly defined by Maria Santos"], "negative_signals": ["21 CFR Part 11 compliance response not prepared", "Maria Santos has not been re-engaged since initial call"]},
            "champion_strength": {"score": 62, "rationale": "Dr. Kevin Walsh is a strong champion with quantified pain and executive access. Sunil Kapoor (Data Engineering) is technically engaged. However, Maria Santos (Regulatory) is a gatekeeper who hasn't been won over.", "positive_signals": ["Dr. Walsh has quantified the CSO-level impact", "Sunil Kapoor is engaged on technical requirements", "Both key technical stakeholders motivated"], "negative_signals": ["Maria Santos not satisfied — regulatory objection unaddressed", "CSO not yet directly engaged"]},
            "cfo_alignment": {"score": 32, "rationale": "CFO not engaged. Budget not confirmed. Deal is in technical evaluation without financial sponsorship. $440K deal will require CFO-level approval but there's no signal that finance is involved.", "positive_signals": ["$2.1M savings from last year creates strong CFO pitch"], "negative_signals": ["CFO not engaged at all", "Budget not confirmed", "Approval path not mapped"]}
        },
        "risks": [
            "21 CFR Part 11 compliance is a hard requirement — if platform cannot demonstrate compliance 'out of the box,' Maria Santos will block the deal regardless of business case strength.",
            "FDA recent inspection with two flagged items means regulatory team will be highly conservative about adding any new data system without rigorous compliance documentation.",
            "No CFO engagement at $440K — deal will stall without financial sponsorship identified and engaged.",
            "Key-person dependency on data pipelines (9 of 14 maintained by one person) — if that person leaves during evaluation, it could create urgency or chaos."
        ],
        "gaps": [
            "21 CFR Part 11 compliance documentation not yet prepared or shared with Maria Santos — this is deal-blocking.",
            "CFO approval path not mapped — who approves a $440K software investment at Nova? Need to identify and engage.",
            "CSO not yet engaged — the go/no-go decision pain is at CSO level but she is not in the evaluation process.",
            "Sunil Kapoor's key-person risk scenario not quantified — this is a powerful additional ROI driver that hasn't been included in business case."
        ],
        "agent_actions": [
            "Prepare 21 CFR Part 11 compliance package for Maria Santos — this is the critical path blocker. Include: Part 11 compliance certification, audit trail documentation, validation protocol.",
            "Research and document CFO approval path at Nova Pharmaceuticals — map who signs a $440K technology decision.",
            "Request CSO introduction through Dr. Walsh — frame as 'sharing the real-time trial data solution with the stakeholder whose decisions it impacts most.'",
            "Add key-person dependency risk to ROI model — quantify the cost of the current 9-pipeline single-person risk to Sunil Kapoor's leadership."
        ]
    },
    "Sterling Financial": {
        "overall_score": 44.0,
        "dimensions": {
            "business_case_strength": {"score": 58, "rationale": "Strong pain quantification: $180K/advisor/year in lost AUM time, 280 advisors. Budget confirmed ($2.1M technology modernization). However, CFO Andrew Kim is hostile due to previous implementation failure — business case credibility is damaged.", "positive_signals": ["Strong quantified pain ($180K/advisor/year)", "Budget allocated ($2.1M technology modernization)", "COO is champion with executive authority"], "negative_signals": ["CFO burned by previous $420K failed implementation", "Business case credibility issue due to implementation history", "CFO requires phased approach not yet formally proposed"]},
            "procurement_readiness": {"score": 32, "rationale": "No formal procurement process initiated. Legal and IT not engaged. At $215K, will require formal vendor review. No requirements gathered from procurement or legal.", "positive_signals": ["Budget exists"], "negative_signals": ["No procurement engagement", "No legal engagement", "No IT security requirements gathered"]},
            "objection_coverage": {"score": 35, "rationale": "Primary CFO objection (implementation risk from previous $420K failure) not yet formally addressed. Phased approach + milestone payments + vendor skin in the game requested — no formal proposal prepared.", "positive_signals": ["Objection clearly understood from Christine's coaching"], "negative_signals": ["No formal phased implementation proposal prepared", "No milestone payment structure designed", "CFO's trust in implementation not rebuilt"]},
            "champion_strength": {"score": 62, "rationale": "Christine Park (COO) is a motivated champion with executive authority and budget awareness. However, she cannot bypass CFO Andrew Kim's implementation risk concern — she needs vendor help building CFO credibility.", "positive_signals": ["COO champion with direct executive authority", "Has specific language on what CFO needs (phased, milestone, skin in game)", "Budget context confirmed"], "negative_signals": ["CFO is the blocker with a legitimate grievance from previous experience", "Champion needs content from vendor to rebuild CFO trust"]},
            "cfo_alignment": {"score": 22, "rationale": "CFO Andrew Kim is gun-shy from previous $420K failed CRM implementation. He has NOT been engaged in this deal. Christine confirmed he will be the final approver and has specific requirements. Until a credible phased proposal is delivered and CFO is engaged, alignment is very low.", "positive_signals": ["Requirements known: phased, milestone, vendor skin in game"], "negative_signals": ["CFO not engaged", "Previous failure context creates high bar for credibility", "No phased proposal delivered", "CFO has not been introduced to vendor"]}
        },
        "risks": [
            "CFO trust gap: Andrew Kim's $420K implementation failure creates a credibility barrier that cannot be overcome with a standard proposal. Every element of the engagement must signal risk-reversal.",
            "Complex multi-CRM data migration from 7 acquired firms: Sterling's M&A history means data quality is unpredictable — this is the same risk that killed the Salesforce migration.",
            "No urgency signal identified: The 4-CRM problem is a 3-year-old issue. Without a catalytic event, deal could stall indefinitely.",
            "Implementation risk is both the primary objection and the most likely deal failure mode — these need to be addressed simultaneously."
        ],
        "gaps": [
            "Phased implementation proposal not designed — CFO specifically requires this. Need to draft a 3-phase implementation plan with milestone-based payment structure and vendor guarantee language.",
            "CFO Andrew Kim not engaged — must be introduced to vendor with a credibility-first approach (case studies of post-M&A CRM integrations that delivered on time).",
            "Data migration risk assessment not performed — for a 7-firm M&A environment, this is the most likely implementation failure mode. Need a pre-sales discovery session with IT.",
            "No urgency identified — need to find a catalytic event (LP audit, regulatory requirement, M&A integration deadline) to create momentum."
        ],
        "agent_actions": [
            "Design phased implementation proposal (3 phases, milestone payments, implementation guarantee) — Christine needs this to bring to CFO Andrew Kim.",
            "Identify 2-3 post-M&A CRM integration case studies where DealFlow AI delivered on time to rebuild CFO credibility.",
            "Schedule a data migration discovery session with IT before proposing — uncover hidden complexity and address it proactively rather than in week 10 of implementation.",
            "Ask Christine to identify a catalytic event that creates urgency: upcoming M&A integration, LP service quality issue, competitive threat requiring advisor productivity."
        ]
    },
    "Cascade Energy": {
        "overall_score": 28.5,
        "dimensions": {
            "business_case_strength": {"score": 42, "rationale": "PHMSA corrective action creates strong urgency and quantifiable risk avoidance ($250K-$2M per incident × 3 incidents). However, no ROI model built, no budget approved, deal is pre-board-approval.", "positive_signals": ["Regulatory penalty avoidance creates compelling board case", "Specific fine structure quantified ($250K-$2M per incident)", "18-month compliance deadline creates urgency"], "negative_signals": ["No ROI model built", "No budget approved", "Board decision not until July 8"]},
            "procurement_readiness": {"score": 8, "rationale": "Deal is in early discovery. No procurement process, no vendor requirements, no technical assessment. Pre-budget, pre-decision.", "positive_signals": [], "negative_signals": ["No budget", "No procurement engagement", "No technical requirements"]},
            "objection_coverage": {"score": 20, "rationale": "No formal objections raised yet. Board will likely raise questions about implementation timeline, utility industry compliance, and total cost. No preparation for these.", "positive_signals": ["No formal objections yet — early stage"], "negative_signals": ["Board objections not anticipated", "No regulatory compliance documentation prepared for PHMSA context"]},
            "champion_strength": {"score": 32, "rationale": "Tom Bergstrom is motivated but self-admittedly has low authority. Director level, driving bottom-up, needs board approval. Greg Aldridge (VP Ops) is the real sponsor but not yet directly engaged in the sale.", "positive_signals": ["Tom is motivated and has regulatory context", "Board meeting on July 8 creates a natural forcing function"], "negative_signals": ["Tom needs board approval to get budget — very low current authority", "Greg Aldridge (VP Ops sponsor) not yet engaged in sale", "No CFO or finance involvement"]},
            "cfo_alignment": {"score": 15, "rationale": "No CFO engagement. No budget. Board decision pending July 8. Deal is too early for CFO alignment — but the board proposal will need strong financial framing.", "positive_signals": ["Regulatory penalty avoidance is a CFO-level concern"], "negative_signals": ["CFO not engaged", "No budget", "Board decision is the first gate"]}
        },
        "risks": [
            "Budget not yet approved — deal cannot progress until board approves on July 8. Any delay in board decision is a slip in deal timeline.",
            "Tom Bergstrom's authority is limited — he is building the proposal but Greg Aldridge (VP Ops) is the real sponsor and hasn't been directly engaged.",
            "Board may not approve the budget if the business case for this specific vendor (vs. alternatives) isn't compelling. Tom needs a strong, board-ready proposal.",
            "Regulatory fine avoidance is compelling but board will want to see alternative approaches (could they extend PHMSA corrective action timeline instead?)."
        ],
        "gaps": [
            "Board-ready business case not yet built — Tom needs a proposal by June 20 and has no ROI model or vendor justification.",
            "Greg Aldridge (VP Operations sponsor) not yet engaged in the sale — he's the real sponsoring executive.",
            "PHMSA corrective action plan details not shared — need specifics on required documentation, timeline, and penalty structure to build compelling case.",
            "Competitive alternatives not assessed — board will ask why DealFlow AI vs. alternatives. Needs competitive positioning for the board presentation."
        ],
        "agent_actions": [
            "Build board-ready business case for Tom immediately — quantify PHMSA fine avoidance (3 incidents × $250K-$2M range), implementation timeline vs. corrective action deadline, and 3-year TCO.",
            "Request introduction to Greg Aldridge (VP Operations) through Tom — executive sponsorship is required before June 20 board submission.",
            "Research PHMSA 192/195 compliance requirements for gas distribution operations — understand the specific compliance gap Cascade needs to close.",
            "Prepare board presentation one-pager: regulatory risk avoided, implementation timeline fitting within 18-month corrective action window, total investment vs. fine exposure."
        ]
    }
}


async def seed_all(db: Session):
    """Create all seed data in the database."""
    from datetime import datetime

    justification_builders = {
        "Apex Manufacturing": build_apex_justification,
        "Quantum Dynamics": build_quantum_justification,
        "Meridian Health": build_meridian_justification,
        "Ironclad Logistics": build_ironclad_justification,
    }

    for deal_data in DEALS:
        company = deal_data["company"]

        # Create deal
        deal = Deal(**deal_data)
        deal.created_at = dt(90)
        db.add(deal)
        db.flush()

        # Create signals
        for sig_data in SIGNALS.get(company, []):
            signal = DealSignal(
                deal_id=deal.id,
                signal_type=sig_data["signal_type"],
                content=sig_data["content"],
                timestamp=sig_data["timestamp"],
                extracted_insights=sig_data.get("extracted_insights")
            )
            db.add(signal)

        # Create justification if we have one
        if company in justification_builders:
            jdata = justification_builders[company]()
            just = Justification(
                deal_id=deal.id,
                roi_model=jdata["roi_model"],
                exec_summary=jdata["exec_summary"],
                procurement_doc=jdata["procurement_doc"],
                objection_responses=jdata["objection_responses"],
                completeness_score=jdata["completeness_score"],
                agent_status=jdata["agent_status"],
                last_updated=dt(2)
            )
            db.add(just)

        # Create health score
        if company in HEALTH_SCORES:
            hs_data = HEALTH_SCORES[company]
            hs = HealthScore(
                deal_id=deal.id,
                overall_score=hs_data["overall_score"],
                dimensions=hs_data["dimensions"],
                risks=hs_data["risks"],
                gaps=hs_data["gaps"],
                agent_actions=hs_data["agent_actions"],
                computed_at=dt(1)
            )
            db.add(hs)

        # Create agent logs
        logs = [
            AgentLog(deal_id=deal.id, action_type="deal_created", description=f"Deal created for {company}.", timestamp=dt(90)),
        ]
        if SIGNALS.get(company):
            logs.append(AgentLog(deal_id=deal.id, action_type="signal_analyzed", description=f"Intelligence agent analyzed {len(SIGNALS[company])} signals for {company}. Extracted pain points, stakeholders, and objections.", timestamp=dt(45)))
        if company in justification_builders:
            logs.append(AgentLog(deal_id=deal.id, action_type="artifact_built", description=f"Artifact agent built justification for {company}. Completeness: {justification_builders[company]()['completeness_score']}%.", timestamp=dt(3)))
        if company in HEALTH_SCORES:
            score = HEALTH_SCORES[company]["overall_score"]
            logs.append(AgentLog(deal_id=deal.id, action_type="health_scored", description=f"Health agent scored {company}: {score:.0f}/100. {len(HEALTH_SCORES[company]['risks'])} risks, {len(HEALTH_SCORES[company]['gaps'])} gaps identified.", timestamp=dt(1)))

        for log in logs:
            db.add(log)

    db.commit()
