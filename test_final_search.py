#!/usr/bin/env python3
"""
Final test to verify /search bcs301 works correctly
"""
import os
import sys
import asyncio
from unittest.mock import MagicMock

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import NotesDatabase

# Mock telegram objects exactly as Telegram API would send them
class MockMessage:
    def __init__(self, text):
        self.text = text
    
    async def reply_text(self, text, parse_mode=None, disable_web_page_preview=None):
        print("🤖 BOT RESPONSE:")
        print("-" * 50)
        print(text)
        print("-" * 50)

class MockUpdate:
    def __init__(self, text):
        self.message = MockMessage(text)

class MockContext:
    def __init__(self, args=None):
        self.args = args or []

async def test_telegram_search():
    """Test exactly how Telegram would call the search"""
    
    from bot import search
    
    print("🔍 TESTING: User sends '/search bcs301' in Telegram")
    print("=" * 60)
    
    # This is exactly how telegram-python-bot passes the data:
    # - update.message.text contains the full message: "/search bcs301"  
    # - context.args contains the arguments: ["bcs301"]
    update = MockUpdate("/search bcs301")
    context = MockContext(args=["bcs301"])
    
    try:
        await search(update, context)
        print("✅ SUCCESS: /search bcs301 works correctly!")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_telegram_search())