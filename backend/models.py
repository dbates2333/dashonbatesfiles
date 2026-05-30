from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    contact_name = Column(String, nullable=False)
    contact_title = Column(String, nullable=False)
    deal_value = Column(Float, nullable=False)
    stage = Column(String, nullable=False)  # discovery/technical_eval/business_case/legal/closed_won/closed_lost
    archetype = Column(String, nullable=False)  # CFO_led/IT_led/Procurement_heavy/Champion_driven
    rep_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    signals = relationship("DealSignal", back_populates="deal", cascade="all, delete-orphan")
    justification = relationship("Justification", back_populates="deal", uselist=False, cascade="all, delete-orphan")
    health_scores = relationship("HealthScore", back_populates="deal", cascade="all, delete-orphan")
    agent_logs = relationship("AgentLog", back_populates="deal", cascade="all, delete-orphan")


class DealSignal(Base):
    __tablename__ = "deal_signals"

    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    signal_type = Column(String, nullable=False)  # call/email/meeting
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    extracted_insights = Column(JSON, nullable=True)

    deal = relationship("Deal", back_populates="signals")


class Justification(Base):
    __tablename__ = "justifications"

    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), unique=True, nullable=False)
    roi_model = Column(JSON, nullable=True)
    exec_summary = Column(Text, nullable=True)
    procurement_doc = Column(Text, nullable=True)
    objection_responses = Column(JSON, nullable=True)  # array of {objection, response, status}
    completeness_score = Column(Integer, default=0)  # 0-100
    agent_status = Column(String, default="needs_review")  # building/complete/needs_review
    last_updated = Column(DateTime, default=datetime.utcnow)

    deal = relationship("Deal", back_populates="justification")


class HealthScore(Base):
    __tablename__ = "health_scores"

    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    overall_score = Column(Float, nullable=False)
    dimensions = Column(JSON, nullable=False)  # {business_case_strength, procurement_readiness, objection_coverage, champion_strength, cfo_alignment}
    risks = Column(JSON, nullable=False)  # array of strings
    gaps = Column(JSON, nullable=False)  # array of strings
    agent_actions = Column(JSON, nullable=False)  # array of strings
    computed_at = Column(DateTime, default=datetime.utcnow)

    deal = relationship("Deal", back_populates="health_scores")


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False)
    action_type = Column(String, nullable=False)  # signal_analyzed/artifact_built/health_scored/section_updated
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    deal = relationship("Deal", back_populates="agent_logs")
