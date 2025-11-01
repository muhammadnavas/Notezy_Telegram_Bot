#!/usr/bin/env python3
"""
Test the improved search with more comprehensive results
"""
import os
import sys
import asyncio
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import NotesDatabase

class MockMessage:
    def __init__(self, text):
        self.text = text
    
    async def reply_text(self, text, parse_mode=None, disable_web_page_preview=None):
        print("🤖 BOT RESPONSE:")
        print("=" * 80)
        print(text)
        print("=" * 80)

class MockUpdate:
    def __init__(self, text):
        self.message = MockMessage(text)

class MockContext:
    def __init__(self, args=None):
        self.args = args or []

async def test_comprehensive_search():
    """Test search with different queries to see improved results"""
    
    from bot import search
    
    test_queries = [
        ("bcs301", "Exact match test"),
        ("mathematics", "Partial match test"),
        ("data", "Broad partial match test"),
        ("programming", "Subject search test")
    ]
    
    for query, description in test_queries:
        print(f"\n🔍 {description.upper()}: '{query}'")
        print("=" * 60)
        
        update = MockUpdate(query)
        context = MockContext(args=[])
        
        try:
            await search(update, context)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_comprehensive_search())