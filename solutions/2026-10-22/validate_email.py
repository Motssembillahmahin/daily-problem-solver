#!/usr/bin/env python3
"""
Email Validator - Validate email addresses
Usage: python validate_email.py <email>
"""

import re
import sys

def validate_email(email: str) -> dict:
    """Validate an email address."""
    # Basic regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    is_valid = bool(re.match(pattern, email))
    
    # Additional checks
    checks = {
        "format": is_valid,
        "has_at": "@" in email,
        "has_domain": "." in email.split("@")[-1] if "@" in email else False,
        "no_spaces": " " not in email,
        "length": len(email) <= 254,
    }
    
    return {
        "email": email,
        "valid": all(checks.values()),
        "checks": checks
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_email.py <email>")
        sys.exit(1)
    
    email = sys.argv[1]
    result = validate_email(email)
    
    print(f"\nEmail: {result['email']}")
    print(f"Valid: {result['valid']}")
    print(f"\nChecks:")
    for check, passed in result['checks'].items():
        print(f"  {check}: {'\u2713' if passed else '\u2717'}")
