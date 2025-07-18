import hashlib
import re
from typing import List

def mask_email(email: str) -> str:
    """
    Mask email addresses by hashing the local part (before @).
    
    Args:
        email: The email address to mask
        
    Returns:
        Masked email address with hashed local part
    """
    if not email or '@' not in email:
        return email
        
    local_part, domain = email.split('@', 1)
    hashed_local = hashlib.md5(local_part.encode()).hexdigest()
    
    return f"{hashed_local}@{domain}"

def mask_card_number(card_number: str) -> str:
    """
    Mask credit card number to show only last 4 digits.
    
    Args:
        card_number: The credit card number to mask
        
    Returns:
        Masked card number in format ****1234
    """
    if not card_number:
        return card_number
    
    # Remove any spaces, hyphens, or other separators
    clean_number = re.sub(r'[^0-9]', '', card_number)
    
    if len(clean_number) >= 4:
        return "****" + clean_number[-4:]
    return "****"

def mask_merchant_location(location: str) -> str:
    """
    Mask specific address but keep city/state for geographic analysis.
    
    Args:
        location: The location string to mask
        
    Returns:
        Masked location with city/state preserved
    """
    if not location:
        return location
    
    # Try to extract city, state pattern
    city_state_pattern = r'([A-Za-z\s]+),\s*([A-Z]{2})$'
    match = re.search(city_state_pattern, location)
    
    if match:
        city, state = match.groups()
        return f"{city}, {state}"
    
    # If no clear city/state pattern, hash the location
    hashed_location = hashlib.md5(location.encode()).hexdigest()[:8]
    return f"Location_{hashed_location}"

def detect_sensitive_transaction_data(description: str) -> List[str]:
    """
    Detect if transaction description contains sensitive PII.
    
    Args:
        description: Transaction description to scan
        
    Returns:
        List of detected PII types
    """
    if not description:
        return []
    
    detected_pii = []
    
    # Social Security Number pattern
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    if re.search(ssn_pattern, description):
        detected_pii.append('ssn')
    
    # Full credit card number pattern (not masked)
    full_card_pattern = r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
    if re.search(full_card_pattern, description):
        detected_pii.append('full_card_number')
    
    # Phone number pattern
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    if re.search(phone_pattern, description):
        detected_pii.append('phone_number')
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(email_pattern, description):
        detected_pii.append('email')
    
    # Account number pattern (generic)
    account_pattern = r'\b(?:account|acct)[\s#]*\d{6,}\b'
    if re.search(account_pattern, description, re.IGNORECASE):
        detected_pii.append('account_number')
    
    return detected_pii

def sanitize_transaction_description(description: str) -> str:
    """
    Sanitize transaction description by removing or masking PII.
    
    Args:
        description: Transaction description to sanitize
        
    Returns:
        Sanitized description with PII removed/masked
    """
    if not description:
        return description
    
    sanitized = description
    
    # Mask Social Security Numbers
    sanitized = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '***-**-****', sanitized)
    
    # Mask full credit card numbers
    sanitized = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '****-****-****-****', sanitized)
    
    # Mask phone numbers
    sanitized = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '***-***-****', sanitized)
    
    # Mask email addresses
    sanitized = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', sanitized)
    
    # Mask account numbers
    sanitized = re.sub(r'\b(?:account|acct)[\s#]*\d{6,}\b', 'ACCOUNT ***', sanitized, flags=re.IGNORECASE)
    
    return sanitized

def validate_card_identifier_format(card_identifier: str) -> bool:
    """
    Validate that card identifier is properly masked.
    
    Args:
        card_identifier: Card identifier to validate
        
    Returns:
        True if properly masked, False otherwise
    """
    if not card_identifier:
        return False
    
    # Should be in format ****1234 or similar
    masked_pattern = r'^\*{4}\d{4}$'
    return bool(re.match(masked_pattern, card_identifier))

def hash_sensitive_field(value: str, salt: str = "credit_refiner") -> str:
    """
    Hash sensitive field values for privacy protection.
    
    Args:
        value: The sensitive value to hash
        salt: Salt to use for hashing
        
    Returns:
        Hashed value
    """
    if not value:
        return value
    
    salted_value = f"{salt}_{value}"
    return hashlib.sha256(salted_value.encode()).hexdigest()