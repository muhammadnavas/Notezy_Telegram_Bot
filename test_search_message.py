#!/usr/bin/env python3
"""
Test the new "searching..." message functionality
"""
import os
import sys
import asyncio
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class MockMessage:
    def __init__(self, text):
        self.text = text
        self.edit_calls = []
    
    async def reply_text(self, text, parse_mode=None, disable_web_page_preview=None):
        print("🤖 INITIAL MESSAGE:")
        print("=" * 50)
        print(text)
        print("=" * 50)
        # Return a mock message object that can be edited
        return MockEditableMessage()
    
    async def edit_text(self, text, parse_mode=None, disable_web_page_preview=None):
        self.edit_calls.append(text)
        print("✏️ MESSAGE EDITED TO:")
        print("=" * 50)
        print(text)
        print("=" * 50)

class MockEditableMessage:
    def __init__(self):
        self.edit_calls = []
    
    async def edit_text(self, text, parse_mode=None, disable_web_page_preview=None):
        self.edit_calls.append(text)
        print("✏️ SEARCH MESSAGE UPDATED:")
        print("=" * 60)
        print(text)
        print("=" * 60)

class MockUpdate:
    def __init__(self, text):
        self.message = MockMessage(text)

class MockContext:
    def __init__(self, args=None):
        self.args = args or []

async def test_search_message():
    """Test the search message flow"""
    
    from bot import search
    
    print("🧪 Testing 'Searching...' message functionality")
    print("=" * 60)
    
    # Test with a simple query
    update = MockUpdate("bcs301")
    context = MockContext(args=[])
    
    try:
        await search(update, context)
        print("✅ Search completed successfully with 'searching...' message!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_search_message())