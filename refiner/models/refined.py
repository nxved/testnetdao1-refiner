from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Date, Boolean, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Base model for SQLAlchemy
Base = declarative_base()

# Define database models for credit card statement data
class StatementRecord(Base):
    __tablename__ = 'statements'
    
    record_id = Column(String, primary_key=True)
    statement_date = Column(Date, nullable=False)
    statement_period_start = Column(Date, nullable=True)
    statement_period_end = Column(Date, nullable=True)
    days_in_period = Column(Integer, nullable=True)
    card_identifier = Column(String, nullable=False)
    payment_due_date = Column(Date, nullable=True)
    currency = Column(String, nullable=True)
    statement_locale = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    account_info = relationship("AccountInfo", back_populates="statement", uselist=False)
    financial_summary = relationship("FinancialSummary", back_populates="statement", uselist=False)
    transactions = relationship("TransactionRecord", back_populates="statement")
    spending_patterns = relationship("SpendingPattern", back_populates="statement", uselist=False)
    risk_metrics = relationship("RiskMetric", back_populates="statement", uselist=False)
    engineered_features = relationship("EngineeredFeature", back_populates="statement", uselist=False)

class AccountInfo(Base):
    __tablename__ = 'account_info'
    
    record_id = Column(String, ForeignKey('statements.record_id'), primary_key=True)
    card_brand = Column(String, nullable=True)
    is_rewards_card = Column(Boolean, nullable=True)
    is_business_card = Column(Boolean, nullable=True)
    credit_limit = Column(Float, nullable=True)
    
    statement = relationship("StatementRecord", back_populates="account_info")

class FinancialSummary(Base):
    __tablename__ = 'financial_summaries'
    
    record_id = Column(String, ForeignKey('statements.record_id'), primary_key=True)
    previous_balance = Column(Float, nullable=False)
    payments_credits = Column(Float, nullable=True)
    purchases = Column(Float, nullable=False)
    closing_balance = Column(Float, nullable=False)
    minimum_payment_due = Column(Float, nullable=True)
    fees_charged = Column(Float, nullable=True)
    interest_charged = Column(Float, nullable=True)
    available_credit = Column(Float, nullable=True)
    cash_advances = Column(Float, nullable=True)
    balance_transfers = Column(Float, nullable=True)
    total_debits = Column(Float, nullable=True)
    total_credits = Column(Float, nullable=True)
    over_limit_amount = Column(Float, nullable=True)
    
    statement = relationship("StatementRecord", back_populates="financial_summary")

class TransactionRecord(Base):
    __tablename__ = 'transactions'
    
    transaction_id = Column(String, primary_key=True)
    record_id = Column(String, ForeignKey('statements.record_id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    transaction_date = Column(Date, nullable=False)
    merchant_name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    location = Column(String, nullable=True)
    is_disputed = Column(Boolean, nullable=True)
    is_recurring = Column(Boolean, nullable=True)
    payment_method = Column(String, nullable=True)
    
    statement = relationship("StatementRecord", back_populates="transactions")

class SpendingPattern(Base):
    __tablename__ = 'spending_patterns'
    
    record_id = Column(String, ForeignKey('statements.record_id'), primary_key=True)
    total_transactions = Column(Integer, nullable=True)
    spending_trend = Column(String, nullable=True)
    category_breakdown = Column(JSON, nullable=True)
    merchant_frequency = Column(JSON, nullable=True)
    seasonal_patterns = Column(JSON, nullable=True)
    recurring_transactions = Column(JSON, nullable=True)
    
    statement = relationship("StatementRecord", back_populates="spending_patterns")

class RiskMetric(Base):
    __tablename__ = 'risk_metrics'
    
    record_id = Column(String, ForeignKey('statements.record_id'), primary_key=True)
    credit_utilization_ratio = Column(Float, nullable=True)
    payment_history_score = Column(Float, nullable=True)
    risk_score = Column(Float, nullable=True)
    fraud_indicators = Column(JSON, nullable=True)
    spending_velocity = Column(Float, nullable=True)
    unusual_activity_score = Column(Float, nullable=True)
    
    statement = relationship("StatementRecord", back_populates="risk_metrics")

class EngineeredFeature(Base):
    __tablename__ = 'engineered_features'
    
    record_id = Column(String, ForeignKey('statements.record_id'), primary_key=True)
    monthly_spending_avg = Column(Float, nullable=True)
    category_diversity_score = Column(Float, nullable=True)
    merchant_loyalty_score = Column(Float, nullable=True)
    transaction_timing_patterns = Column(JSON, nullable=True)
    geographic_spending_patterns = Column(JSON, nullable=True)
    
    statement = relationship("StatementRecord", back_populates="engineered_features")
