#!/usr/bin/env python3
"""
Test script to check bot handlers and search command flow
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Load environment variables  
load_dotenv()

async def test_search_handler():
    """Test the search handler directly"""
    try:
        from bot import search
        from database import NotesDatabase
        
        # Mock update and context objects
        class MockMessage:
            def __init__(self, text):
                self.text = text
            
            async def reply_text(self, text, **kwargs):
                print(f"Bot would reply: {text[:100]}...")
        
        class MockUser:
            def __init__(self):
                self.first_name = "TestUser"
                self.id = 123456
        
        class MockUpdate:
            def __init__(self, text):
                self.message = MockMessage(text)
                self.effective_user = MockUser()
        
        class MockContext:
            def __init__(self, args=None):
                self.args = args or []
        
        print("🔍 Testing search handler...")
        
        # Test 1: Direct search command
        print("\n📝 Testing: /search data structures")
        update = MockUpdate("/search data structures")
        context = MockContext(["data", "structures"])
        await search(update, context)
        
        # Test 2: Text message as search
        print("\n📝 Testing: BCS301")
        update = MockUpdate("BCS301")
        context = MockContext()
        await search(update, context)
        
        # Test 3: Empty query
        print("\n📝 Testing: empty query")
        update = MockUpdate("")
        context = MockContext()
        await search(update, context)
        
        return True
        
    except Exception as e:
        print(f"❌ Search handler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_greeting_handler():
    """Test the greeting handler"""
    try:
        from bot import greeting
        
        # Mock objects (same as above)
        class MockMessage:
            def __init__(self, text):
                self.text = text
            
            async def reply_text(self, text, **kwargs):
                print(f"Bot would reply: {text[:100]}...")
        
        class MockUser:
            def __init__(self):
                self.first_name = "TestUser"
                self.id = 123456
        
        class MockUpdate:
            def __init__(self, text):
                self.message = MockMessage(text)
                self.effective_user = MockUser()
        
        class MockContext:
            def __init__(self):
                self.args = []
        
        print("🤖 Testing greeting handler...")
        
        # Test greeting
        print("\n📝 Testing: hello")
        update = MockUpdate("hello")
        context = MockContext()
        await greeting(update, context)
        
        # Test search through greeting
        print("\n📝 Testing: mathematics")
        update = MockUpdate("mathematics")
        context = MockContext()
        await greeting(update, context)
        
        return True
        
    except Exception as e:
        print(f"❌ Greeting handler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_import_all_modules():
    """Test if all modules can be imported without errors"""
    try:
        print("📦 Testing module imports...")
        
        # Test bot module
        print("   Importing bot...")
        import bot
        print("   ✅ bot imported")
        
        # Test database module  
        print("   Importing database...")
        from database import NotesDatabase
        print("   ✅ database imported")
        
        # Test database connection
        print("   Testing database...")
        db = NotesDatabase()
        count = db.count_notes()
        print(f"   ✅ database connected ({count} notes)")
        
        return True
        
    except Exception as e:
        print(f"❌ Module import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting Bot Handler Tests\n")
    
    # Test 1: Module imports
    imports_ok = test_import_all_modules()
    
    if not imports_ok:
        print("\n❌ Module import tests failed!")
        return
    
    # Test 2: Search handler
    search_ok = await test_search_handler()
    
    if not search_ok:
        print("\n❌ Search handler tests failed!")
        return
    
    # Test 3: Greeting handler  
    greeting_ok = await test_greeting_handler()
    
    if not greeting_ok:
        print("\n❌ Greeting handler tests failed!")
        return
    
    print("\n" + "="*50)
    print("🎉 All handler tests passed!")
    print("✅ Bot search functionality should be working")
    
    print("\nIf search is still not working:")
    print("1. Check bot permissions in Telegram")
    print("2. Verify bot is running properly")
    print("3. Check for any runtime errors in logs")
    print("4. Test with simple commands like /start")

if __name__ == "__main__":
    asyncio.run(main())