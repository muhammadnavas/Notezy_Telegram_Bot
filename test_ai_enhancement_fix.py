#!/usr/bin/env python3
"""
Test the fixed AI query enhancement to ensure no regex errors
"""
import os
import sys
import asyncio
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class MockMessage:
    def __init__(self, text):
        self.text = text
    
    async def reply_text(self, text, parse_mode=None, disable_web_page_preview=None):
        print("🤖 BOT RESPONSE:")
        print("=" * 60)
        print(text)
        print("=" * 60)

class MockUpdate:
    def __init__(self, text):
        self.message = MockMessage(text)

class MockContext:
    def __init__(self, args=None):
        self.args = args or []

async def test_ai_enhancement():
    """Test AI query enhancement with problematic queries"""
    
    from bot import search
    
    # Test queries that might cause regex issues
    problematic_queries = [
        "programming()",
        "data[structures]",
        "math*",
        "C++",
        "object-oriented",
        "web.programming",
        "algorithms|sorting"
    ]
    
    print("🧪 Testing AI query enhancement with potentially problematic queries...")
    print("=" * 70)
    
    for query in problematic_queries:
        print(f"\n🔍 Testing: '{query}'")
        print("-" * 40)
        
        update = MockUpdate(query)
        context = MockContext(args=[])
        
        try:
            await search(update, context)
            print(f"✅ Success: '{query}' processed without errors")
        except Exception as e:
            print(f"❌ Error with '{query}': {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(test_ai_enhancement())