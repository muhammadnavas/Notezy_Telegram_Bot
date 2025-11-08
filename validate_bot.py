#!/usr/bin/env python3
"""
Quick bot validation for group usage
"""

import os
from dotenv import load_dotenv

load_dotenv()

def validate_bot_for_groups():
    """Validate that bot is ready for group usage"""
    
    print("🔍 Bot Group Readiness Check")
    print("="*40)
    
    # Check 1: Environment
    required_vars = ["BOT_TOKEN", "MONGODB_URI"]
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} configured")
        else:
            print(f"❌ {var} missing")
            return False
    
    # Check 2: Database
    try:
        from database import NotesDatabase
        db = NotesDatabase()
        count = db.count_notes()
        print(f"✅ Database: {count} notes available")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    # Check 3: Search functionality
    try:
        # Test the exact query from the screenshot
        result = db.search_notes("bcs301")
        if result['results']:
            print(f"✅ Search 'bcs301': {len(result['results'])} results")
        else:
            print("❌ Search 'bcs301': No results")
            return False
    except Exception as e:
        print(f"❌ Search error: {e}")
        return False
    
    # Check 4: Bot module
    try:
        import bot
        print("✅ Bot module loads correctly")
    except Exception as e:
        print(f"❌ Bot module error: {e}")
        return False
    
    print("\n🎉 Bot is ready for group usage!")
    print("\n📝 Group Setup Instructions:")
    print("1. Add bot to your group")
    print("2. Make bot an admin (or disable privacy mode)")
    print("3. Test with: /search bcs301")
    print("4. Or just type: bcs301")
    
    print(f"\n🤖 Bot Username: Check @BotFather for your bot's username")
    print("💡 In groups, commands can be used as /search@yourbotname")
    
    return True

if __name__ == "__main__":
    validate_bot_for_groups()