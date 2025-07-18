from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List

class Settings(BaseSettings):
    """Global settings configuration using environment variables"""
    
    INPUT_DIR: str = Field(
        default="/input",
        description="Directory containing input files to process"
    )
    
    OUTPUT_DIR: str = Field(
        default="/output",
        description="Directory where output files will be written"
    )
    
    REFINEMENT_ENCRYPTION_KEY: str = Field(
        default=None,
        description="Key to symmetrically encrypt the refinement. This is derived from the original file encryption key"
    )
    
    # Schema Configuration - Updated for Credit Card Data
    SCHEMA_NAME: str = Field(
        default="Credit Card Transaction Analytics",
        description="Name of the schema"
    )
    
    SCHEMA_VERSION: str = Field(
        default="1.0.0",
        description="Version of the schema"
    )
    
    SCHEMA_DESCRIPTION: str = Field(
        default="Schema for credit card transaction data, representing normalized financial transactions with privacy preservation and AI-ready insights",
        description="Description of the schema"
    )
    
    SCHEMA_DIALECT: str = Field(
        default="sqlite",
        description="Dialect of the schema"
    )
    
    # Credit Card Data Processing Configuration
    DATA_TYPE: str = Field(
        default="credit_card",
        description="Type of data being processed (credit_card, google_drive, etc.)"
    )
    
    # Financial Data Configuration
    SUPPORTED_CURRENCIES: List[str] = Field(
        default=[
            'USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 'NZD', 'SEK', 'NOK', 'DKK',
            'INR', 'CNY', 'KRW', 'SGD', 'HKD', 'THB', 'MYR', 'IDR', 'PHP', 'VND',
            'BRL', 'MXN', 'ARS', 'CLP', 'COP', 'PEN', 'ZAR', 'EGP', 'NGN', 'KES',
            'AED', 'SAR', 'QAR', 'KWD', 'BHD', 'OMR', 'TRY', 'PLN', 'CZK', 'HUF',
            'RUB', 'UAH', 'ILS', 'JOD', 'LBP', 'PKR', 'BDT', 'LKR', 'NPR', 'BTN'
        ],
        description="List of supported ISO 4217 currency codes"
    )
    
    SUPPORTED_COUNTRIES: List[str] = Field(
        default=[
            'US', 'CA', 'MX', 'GB', 'IE', 'FR', 'DE', 'IT', 'ES', 'PT', 'NL', 'BE',
            'AT', 'CH', 'SE', 'NO', 'DK', 'FI', 'IS', 'PL', 'CZ', 'SK', 'HU', 'RO',
            'BG', 'HR', 'SI', 'EE', 'LV', 'LT', 'GR', 'CY', 'MT', 'LU', 'AU', 'NZ',
            'JP', 'KR', 'CN', 'HK', 'TW', 'SG', 'MY', 'TH', 'VN', 'PH', 'ID', 'IN',
            'PK', 'BD', 'LK', 'NP', 'BT', 'MM', 'KH', 'LA', 'BN', 'MN', 'AE', 'SA',
            'KW', 'QA', 'BH', 'OM', 'JO', 'IL', 'TR', 'EG', 'ZA', 'KE', 'UG', 'TZ',
            'RW', 'ET', 'GH', 'NG', 'CI', 'SN', 'MA', 'TN', 'DZ', 'LY', 'SD', 'BR',
            'AR', 'CL', 'CO', 'PE', 'EC', 'UY', 'PY', 'BO', 'VE', 'GY', 'SR', 'GF'
        ],
        description="List of supported ISO 3166-1 alpha-2 country codes"
    )
    
    # Data Quality Configuration
    MIN_QUALITY_SCORE: float = Field(
        default=70.0,
        description="Minimum quality score threshold for transaction data (0-100)"
    )
    
    MAX_TRANSACTION_AMOUNT: float = Field(
        default=100000.0,
        description="Maximum reasonable transaction amount for validation"
    )
    
    MIN_TRANSACTION_AMOUNT: float = Field(
        default=0.01,
        description="Minimum transaction amount for validation"
    )
    
    # Privacy Configuration
    ANONYMIZATION_METHOD: str = Field(
        default="k_anonymity",
        description="Anonymization method to use (k_anonymity, differential_privacy, synthetic_data)"
    )
    
    PRIVACY_LEVEL: str = Field(
        default="medium",
        description="Privacy level (low, medium, high, maximum)"
    )
    
    K_ANONYMITY_VALUE: int = Field(
        default=5,
        description="K-value for k-anonymity privacy preservation"
    )
    
    DIFFERENTIAL_PRIVACY_EPSILON: float = Field(
        default=1.0,
        description="Epsilon value for differential privacy"
    )
    
    # Processing Configuration
    BATCH_SIZE: int = Field(
        default=1000,
        description="Batch size for processing large transaction datasets"
    )
    
    MAX_MEMORY_USAGE_MB: int = Field(
        default=512,
        description="Maximum memory usage in MB for processing"
    )
    
    ENABLE_STREAMING: bool = Field(
        default=True,
        description="Enable streaming processing for large datasets"
    )
    
    # Input Format Configuration
    SUPPORTED_INPUT_FORMATS: List[str] = Field(
        default=["json", "zip", "csv"],
        description="List of supported input file formats"
    )
    
    UNIVERSAL_SCHEMA_VERSION: str = Field(
        default="1.0.0",
        description="Version of the UniversalTransactionSchema being used"
    )
    
    # Optional, required if using https://pinata.cloud (IPFS pinning service)
    PINATA_API_KEY: Optional[str] = Field(
        default=None,
        description="Pinata API key"
    )
    
    PINATA_API_SECRET: Optional[str] = Field(
        default=None,
        description="Pinata API secret"
    )

    IPFS_GATEWAY_URL: str = Field(
        default="https://gateway.pinata.cloud/ipfs",
        description="IPFS gateway URL for accessing uploaded files. Recommended to use own dedicated gateway to avoid congestion and rate limiting. Example: 'https://ipfs.my-dao.org/ipfs' (Note: won't work for third-party files)"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 