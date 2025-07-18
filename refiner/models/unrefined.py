from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class StatementPeriod(BaseModel):
    start_date: str
    end_date: str

class StatementMetadata(BaseModel):
    record_id: str
    statement_date: str
    statement_period: Optional[StatementPeriod] = None
    days_in_period: Optional[int] = None
    card_identifier: str
    payment_due_date: Optional[str] = None
    currency: Optional[str] = None
    statement_locale: Optional[str] = None

class AccountInfo(BaseModel):
    card_brand: Optional[str] = None
    is_rewards_card: Optional[bool] = None
    is_business_card: Optional[bool] = None
    credit_limit: Optional[float] = None

class FinancialSummary(BaseModel):
    previous_balance: float
    payments_credits: Optional[float] = None
    purchases: float
    closing_balance: float
    minimum_payment_due: Optional[float] = None
    fees_charged: Optional[float] = None
    interest_charged: Optional[float] = None
    available_credit: Optional[float] = None
    cash_advances: Optional[float] = None
    balance_transfers: Optional[float] = None
    total_debits: Optional[float] = None
    total_credits: Optional[float] = None
    over_limit_amount: Optional[float] = None

class Transaction(BaseModel):
    transaction_id: str
    amount: float
    description: str
    date: str
    merchant_name: str
    category: Optional[str] = None
    location: Optional[str] = None
    is_disputed: Optional[bool] = None
    is_recurring: Optional[bool] = None
    payment_method: Optional[str] = None

class SpendingPatterns(BaseModel):
    total_transactions: Optional[int] = None
    spending_trend: Optional[str] = None
    category_breakdown: Optional[Dict[str, float]] = None
    merchant_frequency: Optional[Dict[str, int]] = None
    seasonal_patterns: Optional[Dict[str, Any]] = None
    recurring_transactions: Optional[List[Dict[str, Any]]] = None

class RiskMetrics(BaseModel):
    credit_utilization_ratio: Optional[float] = None
    payment_history_score: Optional[float] = None
    risk_score: Optional[float] = None
    fraud_indicators: Optional[List[str]] = None
    spending_velocity: Optional[float] = None
    unusual_activity_score: Optional[float] = None

class EngineeredFeatures(BaseModel):
    monthly_spending_avg: Optional[float] = None
    category_diversity_score: Optional[float] = None
    merchant_loyalty_score: Optional[float] = None
    transaction_timing_patterns: Optional[Dict[str, Any]] = None
    geographic_spending_patterns: Optional[Dict[str, Any]] = None

class CreditStatement(BaseModel):
    statement_metadata: StatementMetadata
    account_info: Optional[AccountInfo] = None
    financial_summary: FinancialSummary
    transactions: List[Transaction]
    spending_patterns: Optional[SpendingPatterns] = None
    risk_metrics: Optional[RiskMetrics] = None
    engineered_features: Optional[EngineeredFeatures] = None