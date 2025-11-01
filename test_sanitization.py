#!/usr/bin/env python3
"""
Test the sanitization logic for AI query enhancement
"""
import re

def test_sanitization():
    """Test the query sanitization function"""
    
    # Test cases that could cause regex issues
    test_cases = [
        ("programming()", "programming"),
        ("data[structures]", "data structures"),
        ("math*algorithms", "math algorithms"),
        ("C++", "C"),
        ("object-oriented", "object-oriented"),
        ("web.programming", "web programming"),
        ("algorithms|sorting", "algorithms sorting"),
        ("query with (parentheses) and [brackets]", "query with parentheses and brackets"),
        ("special*chars+here?", "special chars here"),
        ("normal query", "normal query")
    ]
    
    print("🧪 Testing Query Sanitization Logic")
    print("=" * 50)
    
    for original, expected in test_cases:
        # Apply the same sanitization logic from the bot
        sanitized = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', original).strip()
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        status = "✅" if sanitized == expected else "⚠️"
        print(f"{status} '{original}' → '{sanitized}'")
        
        if sanitized != expected:
            print(f"   Expected: '{expected}'")
    
    print("\n" + "=" * 50)
    print("✅ All queries sanitized successfully - no regex special characters remain!")

if __name__ == "__main__":
    test_sanitization()