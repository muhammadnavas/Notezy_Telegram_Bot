#!/usr/bin/env python3
"""
Test the search command with proper command args handling
"""
import os
import sys
import asyncio
from unittest.mock import MagicMock

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import NotesDatabase

# Mock telegram objects
class MockMessage:
    def __init__(self, text):
        self.text = text
    
    async def reply_text(self, text, parse_mode=None, disable_web_page_preview=None):
        print("=" * 50)
        print("BOT RESPONSE:")
        print("=" * 50)
        print(text)
        print("=" * 50)

class MockUpdate:
    def __init__(self, text):
        self.message = MockMessage(text)

class MockContext:
    def __init__(self, args=None):
        self.args = args or []

async def test_search_command():
    """Test the /search command with args"""
    
    # Import the search function 
    from bot import search
    
    # Test 1: Search with args (how CommandHandler passes it)
    print("🤖 Test 1: Command with args '/search bcs301'")
    update = MockUpdate("/search bcs301")  # Full command text
    context = MockContext(args=["bcs301"])  # Args extracted by CommandHandler
    
    try:
        await search(update, context)
    except Exception as e:
        print(f"❌ Error in search: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: Direct message (how MessageHandler passes it) 
    print("\n" + "="*50)
    print("🤖 Test 2: Direct message 'bcs301'")
    update = MockUpdate("bcs301")  # Just the query
    context = MockContext(args=[])  # No args
    
    try:
        await search(update, context)
    except Exception as e:
        print(f"❌ Error in search: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_search_command())