#!/usr/bin/env python3
"""
Test the bot search command directly to simulate the /search bcs301 command
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
    def __init__(self):
        pass

async def test_bot_search():
    """Test the bot's search function directly"""
    
    # Import the search function 
    from bot import search
    
    # Create mock objects
    update = MockUpdate("bcs301")  # Simulate just the query (without /search prefix)
    context = MockContext()
    
    print("🤖 Testing bot search command: '/search bcs301'")
    print("🔌 This will test the actual bot search logic...")
    
    try:
        await search(update, context)
    except Exception as e:
        print(f"❌ Error in bot search: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_bot_search())