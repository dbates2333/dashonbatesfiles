export type DealStage = 'discovery' | 'technical_eval' | 'business_case' | 'legal' | 'closed_won' | 'closed_lost'
export type DealArchetype = 'CFO_led' | 'IT_led' | 'Procurement_heavy' | 'Champion_driven'
export type AgentStatus = 'building' | 'complete' | 'needs_review' | 'not_started'

export interface DealDimension {
  score: number
  rationale: string
  positive_signals?: string[]
  negative_signals?: string[]
}

export interface HealthDimensions {
  business_case_strength: DealDimension
  procurement_readiness: DealDimension
  objection_coverage: DealDimension
  champion_strength: DealDimension
  cfo_alignment: DealDimension
}

export interface HealthScore {
  overall_score: number
  dimensions: HealthDimensions
  risks: string[]
  gaps: string[]
  agent_actions: string[]
  computed_at: string
}

export interface JustificationStatus {
  completeness_score: number
  agent_status: AgentStatus
  last_updated: string | null
}

export interface ROIScenario {
  three_year_roi_percent: number
  payback_months: number
  three_year_npv: number
  annual_savings_year1: number
  annual_savings_year2: number
  annual_savings_year3: number
}

export interface ROIModel {
  assumptions: Array<{
    label: string
    value: string
    source: string
    confidence: 'high' | 'medium' | 'low'
  }>
  cost_components: Array<{
    category: string
    annual_cost: number
    description: string
  }>
  benefit_components: Array<{
    category: string
    annual_value: number
    description: string
    confidence: 'high' | 'medium' | 'low'
  }>
  scenarios: {
    conservative: ROIScenario
    base: ROIScenario
    optimistic: ROIScenario
  }
  total_investment: number
  implementation_cost: number
  annual_contract_value: number
}

export interface ObjectionResponse {
  objection: string
  raised_by?: string
  category?: string
  response: string
  supporting_data?: string
  follow_up_action?: string
  status: 'addressed' | 'needs_follow_up' | 'escalated'
}

export interface Justification {
  id: number
  deal_id: number
  roi_model: ROIModel | null
  exec_summary: string | null
  procurement_doc: string | null
  objection_responses: ObjectionResponse[] | null
  completeness_score: number
  agent_status: AgentStatus
  last_updated: string | null
}

export interface DealSignal {
  id: number
  signal_type: 'call' | 'email' | 'meeting'
  content: string
  timestamp: string
  extracted_insights?: {
    pain_points?: Array<{
      description: string
      quote?: string
      business_impact?: string
      urgency: 'critical' | 'high' | 'medium' | 'low'
      department?: string
    }>
    stakeholders?: Array<{
      name: string
      title: string
      role: string
      sentiment: string
      key_concern?: string
      influence_score?: number
    }>
    objections?: Array<{
      objection: string
      raised_by?: string
      category: string
      severity: string
      quote?: string
    }>
    champion_strength_signal?: {
      score: number
      evidence: string
    }
  }
}

export interface Deal {
  id: number
  company: string
  contact_name: string
  contact_title: string
  deal_value: number
  stage: DealStage
  archetype: DealArchetype
  rep_name?: string
  created_at: string
  updated_at?: string
  latest_health: HealthScore | null
  justification_status: JustificationStatus | null
  signals?: DealSignal[]
  justification?: Justification | null
  health_scores?: HealthScore[]
}

export interface AgentLogEntry {
  id: number
  action_type: string
  description: string
  timestamp: string
}

export interface PipelineDeal extends Deal {
  signal_count: number
  health: HealthScore | null
}

export interface PipelineAlert {
  deal_id: number
  company: string
  deal_value: number
  stage: string
  overall_score: number
  alerts: Array<{
    severity: 'critical' | 'high' | 'medium' | 'low'
    type: string
    message: string
  }>
  top_risks: string[]
}

export interface PipelineStats {
  total_pipeline_value: number
  total_deals: number
  avg_health_score: number
  at_risk_count: number
  building_count: number
  healthy_count: number
  stage_breakdown: Record<string, { count: number; value: number }>
  completeness_distribution: Record<string, number>
}

export interface StreamChunk {
  type: 'tool_progress' | 'section_complete' | 'complete' | 'error'
  tool?: string
  message?: string
  section?: string
  data?: unknown
  result?: Justification
}
