#!/usr/bin/env python3
"""
Test bot functionality for group chats
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_group_chat_functionality():
    """Test bot handlers for group chat scenarios"""
    
    # Test search with different formats
    test_cases = [
        "bcs301",           # Direct search
        "/search bcs301",   # Command search
        "/search@notezy_bot bcs301",  # Group format (if needed)
        "data structures",  # Subject name
        "mathematics",      # Partial match
        "hello",           # Greeting
        "3rd sem"          # Semester query
    ]
    
    try:
        from database import NotesDatabase
        from bot import search, greeting
        
        print("🔍 Testing group chat compatibility...")
        
        # Mock classes for testing
        class MockMessage:
            def __init__(self, text):
                self.text = text
                self._reply_count = 0
            
            async def reply_text(self, text, **kwargs):
                self._reply_count += 1
                print(f"  📤 Bot reply #{self._reply_count}: {text[:80]}...")
                # Return a mock message object that has edit_text
                return MockEditableMessage(text)
        
        class MockEditableMessage:
            def __init__(self, text):
                self.text = text
            
            async def edit_text(self, text, **kwargs):
                print(f"  ✏️  Edited message: {text[:80]}...")
        
        class MockUser:
            def __init__(self):
                self.first_name = "TestUser"
                self.id = 123456
        
        class MockChat:
            def __init__(self, chat_type="group"):
                self.type = chat_type
                self.id = -123456789  # Negative for groups
                self.title = "Test Group"
        
        class MockUpdate:
            def __init__(self, text, chat_type="group"):
                self.message = MockMessage(text)
                self.effective_user = MockUser()
                self.effective_chat = MockChat(chat_type)
        
        class MockContext:
            def __init__(self, args=None):
                self.args = args or []
        
        # Test each case
        for i, test_text in enumerate(test_cases, 1):
            print(f"\n{i}. Testing: '{test_text}'")
            
            # Determine if it's a command or regular message
            if test_text.startswith('/search'):
                # Extract args for search command
                args = test_text.split()[1:] if len(test_text.split()) > 1 else []
                update = MockUpdate(test_text, "group")
                context = MockContext(args)
                print("  🤖 Calling search handler...")
                await search(update, context)
            else:
                # Regular message - goes to greeting handler
                update = MockUpdate(test_text, "group")
                context = MockContext()
                print("  🤖 Calling greeting handler...")
                await greeting(update, context)
            
            print("  ✅ Handler completed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Group chat test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_bot_configuration():
    """Check bot configuration for group compatibility"""
    print("⚙️  Checking bot configuration...")
    
    # Check if bot token exists
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("  ❌ BOT_TOKEN not found")
        return False
    
    print("  ✅ BOT_TOKEN found")
    
    # Check database connection
    try:
        from database import NotesDatabase
        db = NotesDatabase()
        count = db.count_notes()
        print(f"  ✅ Database connected ({count} notes)")
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        return False
    
    return True

async def main():
    """Run all group chat tests"""
    print("🏢 Group Chat Compatibility Tests\n")
    
    # Test 1: Configuration
    config_ok = check_bot_configuration()
    if not config_ok:
        print("❌ Configuration check failed!")
        return
    
    # Test 2: Group functionality
    group_ok = await test_group_chat_functionality()
    if not group_ok:
        print("❌ Group chat tests failed!")
        return
    
    print("\n" + "="*60)
    print("🎉 Group Chat Tests Completed!")
    print("✅ Bot should work properly in groups")
    
    print("\n📋 For groups, make sure:")
    print("1. Bot has 'Send Messages' permission")
    print("2. Bot has 'Read Messages' permission")
    print("3. Bot can see all messages (disable privacy mode)")
    print("4. Commands work with /search format")
    print("5. Direct messages to bot work for search")
    
    print("\n🧪 Test in your group:")
    print("• /search bcs301")
    print("• /start")
    print("• mathematics")
    print("• data structures")

if __name__ == "__main__":
    asyncio.run(main())