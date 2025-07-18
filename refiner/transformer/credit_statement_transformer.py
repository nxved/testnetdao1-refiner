from typing import Dict, Any, List
from datetime import datetime
from refiner.models.refined import Base
from refiner.transformer.base_transformer import DataTransformer
from refiner.models.refined import (
    StatementRecord, AccountInfo, FinancialSummary, TransactionRecord,
    SpendingPattern, RiskMetric, EngineeredFeature
)
from refiner.models.unrefined import CreditStatement
from refiner.utils.date import parse_timestamp
from refiner.utils.pii import (
    sanitize_transaction_description,
    mask_merchant_location,
    validate_card_identifier_format,
    detect_sensitive_transaction_data
)


class CreditStatementTransformer(DataTransformer):
    """
    Transformer for credit card statement data.
    Converts raw credit statement JSON into normalized database records.
    """
    
    def transform(self, data: Dict[str, Any]) -> List[Base]:
        """
        Transform raw credit statement data into SQLAlchemy model instances.
        
        Args:
            data: Dictionary containing credit statement data
            
        Returns:
            List of SQLAlchemy model instances
        """
        # Validate data with Pydantic
        unrefined_statement = CreditStatement.model_validate(data)
        
        models = []
        
        # Create main statement record
        statement_record = self._create_statement_record(unrefined_statement)
        models.append(statement_record)
        
        # Create account info if present
        if unrefined_statement.account_info:
            account_info = self._create_account_info(unrefined_statement)
            models.append(account_info)
        
        # Create financial summary (required)
        financial_summary = self._create_financial_summary(unrefined_statement)
        models.append(financial_summary)
        
        # Create transaction records (required)
        transaction_records = self._create_transaction_records(unrefined_statement)
        models.extend(transaction_records)
        
        # Create spending patterns if present
        if unrefined_statement.spending_patterns:
            spending_pattern = self._create_spending_pattern(unrefined_statement)
            models.append(spending_pattern)
        
        # Create risk metrics if present
        if unrefined_statement.risk_metrics:
            risk_metric = self._create_risk_metric(unrefined_statement)
            models.append(risk_metric)
        
        # Create engineered features if present
        if unrefined_statement.engineered_features:
            engineered_feature = self._create_engineered_feature(unrefined_statement)
            models.append(engineered_feature)
        
        return models
    
    def _create_statement_record(self, statement: CreditStatement) -> StatementRecord:
        """Create the main statement record with card identifier validation."""
        # Validate card identifier format for security
        card_identifier = statement.statement_metadata.card_identifier
        if not validate_card_identifier_format(card_identifier):
            print(f"Warning: Card identifier {card_identifier} may not be properly masked")
        
        return StatementRecord(
            record_id=statement.statement_metadata.record_id,
            statement_date=self._parse_date(statement.statement_metadata.statement_date),
            statement_period_start=self._parse_date(statement.statement_metadata.statement_period.start_date) if statement.statement_metadata.statement_period else None,
            statement_period_end=self._parse_date(statement.statement_metadata.statement_period.end_date) if statement.statement_metadata.statement_period else None,
            days_in_period=statement.statement_metadata.days_in_period,
            card_identifier=card_identifier,
            payment_due_date=self._parse_date(statement.statement_metadata.payment_due_date) if statement.statement_metadata.payment_due_date else None,
            currency=statement.statement_metadata.currency,
            statement_locale=statement.statement_metadata.statement_locale
        )
    
    def _create_account_info(self, statement: CreditStatement) -> AccountInfo:
        """Create account info record."""
        return AccountInfo(
            record_id=statement.statement_metadata.record_id,
            card_brand=statement.account_info.card_brand,
            is_rewards_card=statement.account_info.is_rewards_card,
            is_business_card=statement.account_info.is_business_card,
            credit_limit=statement.account_info.credit_limit
        )
    
    def _create_financial_summary(self, statement: CreditStatement) -> FinancialSummary:
        """Create financial summary record."""
        return FinancialSummary(
            record_id=statement.statement_metadata.record_id,
            previous_balance=statement.financial_summary.previous_balance,
            payments_credits=statement.financial_summary.payments_credits,
            purchases=statement.financial_summary.purchases,
            closing_balance=statement.financial_summary.closing_balance,
            minimum_payment_due=statement.financial_summary.minimum_payment_due,
            fees_charged=statement.financial_summary.fees_charged,
            interest_charged=statement.financial_summary.interest_charged,
            available_credit=statement.financial_summary.available_credit,
            cash_advances=statement.financial_summary.cash_advances,
            balance_transfers=statement.financial_summary.balance_transfers,
            total_debits=statement.financial_summary.total_debits,
            total_credits=statement.financial_summary.total_credits,
            over_limit_amount=statement.financial_summary.over_limit_amount
        )
    
    def _create_transaction_records(self, statement: CreditStatement) -> List[TransactionRecord]:
        """Create transaction records with PII protection."""
        transactions = []
        
        for txn in statement.transactions:
            # Sanitize transaction description for PII
            sanitized_description = sanitize_transaction_description(txn.description)
            
            # Mask merchant location while preserving geographic data
            masked_location = mask_merchant_location(txn.location) if txn.location else None
            
            # Detect any remaining PII issues
            pii_detected = detect_sensitive_transaction_data(sanitized_description)
            if pii_detected:
                # Log PII detection for security audit
                print(f"PII detected in transaction {txn.transaction_id}: {pii_detected}")
            
            transaction = TransactionRecord(
                transaction_id=txn.transaction_id,
                record_id=statement.statement_metadata.record_id,
                amount=txn.amount,
                description=sanitized_description,
                transaction_date=self._parse_date(txn.date),
                merchant_name=txn.merchant_name,
                category=txn.category,
                location=masked_location,
                is_disputed=txn.is_disputed,
                is_recurring=txn.is_recurring,
                payment_method=txn.payment_method
            )
            transactions.append(transaction)
        
        return transactions
    
    def _create_spending_pattern(self, statement: CreditStatement) -> SpendingPattern:
        """Create spending pattern record."""
        return SpendingPattern(
            record_id=statement.statement_metadata.record_id,
            total_transactions=statement.spending_patterns.total_transactions,
            spending_trend=statement.spending_patterns.spending_trend,
            category_breakdown=statement.spending_patterns.category_breakdown,
            merchant_frequency=statement.spending_patterns.merchant_frequency,
            seasonal_patterns=statement.spending_patterns.seasonal_patterns,
            recurring_transactions=statement.spending_patterns.recurring_transactions
        )
    
    def _create_risk_metric(self, statement: CreditStatement) -> RiskMetric:
        """Create risk metric record."""
        return RiskMetric(
            record_id=statement.statement_metadata.record_id,
            credit_utilization_ratio=statement.risk_metrics.credit_utilization_ratio,
            payment_history_score=statement.risk_metrics.payment_history_score,
            risk_score=statement.risk_metrics.risk_score,
            fraud_indicators=statement.risk_metrics.fraud_indicators,
            spending_velocity=statement.risk_metrics.spending_velocity,
            unusual_activity_score=statement.risk_metrics.unusual_activity_score
        )
    
    def _create_engineered_feature(self, statement: CreditStatement) -> EngineeredFeature:
        """Create engineered feature record."""
        return EngineeredFeature(
            record_id=statement.statement_metadata.record_id,
            monthly_spending_avg=statement.engineered_features.monthly_spending_avg,
            category_diversity_score=statement.engineered_features.category_diversity_score,
            merchant_loyalty_score=statement.engineered_features.merchant_loyalty_score,
            transaction_timing_patterns=statement.engineered_features.transaction_timing_patterns,
            geographic_spending_patterns=statement.engineered_features.geographic_spending_patterns
        )
    
    def _parse_date(self, date_str: str):
        """Parse date string to date object."""
        if not date_str:
            return None
        
        try:
            # Try parsing as ISO date first
            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
        except ValueError:
            try:
                # Try parsing as date only
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                # Return None if unable to parse
                return None