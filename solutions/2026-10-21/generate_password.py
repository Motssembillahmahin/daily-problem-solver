#!/usr/bin/env python3
"""
Password Generator - Generate secure passwords
Usage: python generate_password.py [--length 16] [--count 5]
"""

import secrets
import string
import argparse

def generate_password(length: int = 16, use_special: bool = True) -> str:
    """Generate a secure password."""
    characters = string.ascii_letters + string.digits
    if use_special:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one of each type
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
    ]
    
    if use_special:
        password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    # Fill the rest
    password.extend(secrets.choice(characters) for _ in range(length - len(password)))
    
    # Shuffle
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    
    return "".join(password_list)

def check_password_strength(password: str) -> dict:
    """Check password strength."""
    checks = {
        "length": len(password) >= 12,
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "digits": any(c.isdigit() for c in password),
        "special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
    }
    
    score = sum(checks.values())
    
    return {
        "password": password,
        "score": score,
        "max_score": 5,
        "strength": ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"][score - 1],
        "checks": checks
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate secure passwords")
    parser.add_argument("--length", type=int, default=16, help="Password length")
    parser.add_argument("--count", type=int, default=1, help="Number of passwords")
    parser.add_argument("--no-special", action="store_true", help="Exclude special characters")
    
    args = parser.parse_args()
    
    print(f"\nGenerating {args.count} password(s) (length: {args.length}):\n")
    
    for i in range(args.count):
        password = generate_password(args.length, not args.no_special)
        strength = check_password_strength(password)
        
        print(f"{i+1}. {password}")
        print(f"   Strength: {strength['strength']} ({strength['score']}/{strength['max_score']})")
        print()
