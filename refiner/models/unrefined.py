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
    transaction_date: str  # Renamed from 'date' to match proof schema
    posting_date: Optional[str] = None
    description: str
    amount: float
    transaction_type: Optional[str] = None  # PURCHASE|PAYMENT|CASH_ADVANCE|FEE|INTEREST|REFUND
    day_of_week: Optional[int] = None  # 1-7, Monday-Sunday
    day_of_month: Optional[int] = None
    is_weekend: Optional[bool] = None
    merchant_name: str
    merchant_id: Optional[str] = None
    category_primary: Optional[str] = None  # Renamed from 'category'
    category_detailed: Optional[str] = None
    channel: Optional[str] = None  # POS|ONLINE|ATM|MOBILE|RECURRING|OTHER
    currency: Optional[str] = "USD"
    transaction_country: Optional[str] = "US"
    transaction_locale: Optional[str] = "en_US"
    is_international: Optional[bool] = False
    is_recurring: Optional[bool] = None
    location: Optional[str] = None  # Kept for backward compatibility
    is_disputed: Optional[bool] = None
    payment_method: Optional[str] = None  # Kept for additional detail

class SpendingPatterns(BaseModel):
    total_transactions: Optional[int] = None
    average_transaction_amount: Optional[float] = None
    std_dev_transaction_amount: Optional[float] = None
    median_transaction_amount: Optional[float] = None
    max_transaction_amount: Optional[float] = None
    min_transaction_amount: Optional[float] = None
    transactions_per_day: Optional[float] = None
    weekend_spending_ratio: Optional[float] = None
    night_spending_ratio: Optional[float] = None
    category_distribution: Optional[Dict[str, Any]] = None  # Renamed from category_breakdown
    channel_distribution: Optional[Dict[str, Any]] = None  # Added
    spending_trend: Optional[str] = None  # Kept
    merchant_frequency: Optional[Dict[str, int]] = None  # Kept for additional detail
    seasonal_patterns: Optional[Dict[str, Any]] = None  # Kept
    recurring_transactions: Optional[List[Dict[str, Any]]] = None  # Kept

class VelocityIndicators(BaseModel):
    max_daily_transactions: Optional[int] = None
    max_daily_amount: Optional[float] = None
    unusual_activity_flag: Optional[bool] = False

class RiskMetrics(BaseModel):
    credit_utilization_ratio: Optional[float] = None
    payment_ratio: Optional[float] = None  # Renamed from payment_history_score
    cash_advance_ratio: Optional[float] = None
    international_transaction_ratio: Optional[float] = None
    high_risk_merchant_ratio: Optional[float] = None
    velocity_indicators: Optional[VelocityIndicators] = None  # Added nested structure
    # Kept for backward compatibility
    payment_history_score: Optional[float] = None
    risk_score: Optional[float] = None
    fraud_indicators: Optional[List[str]] = None
    spending_velocity: Optional[float] = None
    unusual_activity_score: Optional[float] = None

class PaymentHistory(BaseModel):
    payment_status: Optional[str] = None  # PAID_FULL|PAID_MINIMUM|PAID_PARTIAL|NO_PAYMENT

class EngineeredFeatures(BaseModel):
    days_since_last_transaction: Optional[int] = None
    days_since_last_payment: Optional[int] = None
    spending_trend: Optional[str] = None  # INCREASING|STABLE|DECREASING
    spending_velocity: Optional[float] = None
    unique_merchants_count: Optional[int] = None
    merchant_diversity_score: Optional[float] = None
    new_merchant_ratio: Optional[float] = None
    essential_spending_ratio: Optional[float] = None
    discretionary_spending_ratio: Optional[float] = None
    subscription_spending_ratio: Optional[float] = None
    spending_consistency_score: Optional[float] = None
    payment_reliability_score: Optional[float] = None
    merchant_loyalty_score: Optional[float] = None
    # Kept for backward compatibility
    monthly_spending_avg: Optional[float] = None
    category_diversity_score: Optional[float] = None  # Already exists
    transaction_timing_patterns: Optional[Dict[str, Any]] = None
    geographic_spending_patterns: Optional[Dict[str, Any]] = None

class CreditStatement(BaseModel):
    statement_metadata: StatementMetadata
    account_info: Optional[AccountInfo] = None
    financial_summary: FinancialSummary
    transactions: List[Transaction]
    spending_patterns: Optional[SpendingPatterns] = None
    risk_metrics: Optional[RiskMetrics] = None
    payment_history: Optional[PaymentHistory] = None  # Added
    engineered_features: Optional[EngineeredFeatures] = None