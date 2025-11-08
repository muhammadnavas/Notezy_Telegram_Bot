#!/usr/bin/env python3
"""
Test script to check if the search functionality is working properly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test if we can connect to the database"""
    try:
        from database import NotesDatabase
        
        print("🔍 Testing database connection...")
        db = NotesDatabase()
        print("✅ Database connection successful")
        
        # Test count
        count = db.count_notes()
        print(f"📊 Total notes in database: {count}")
        
        if count == 0:
            print("⚠️ Database is empty - this might be why search isn't working")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_search_functionality():
    """Test the search function directly"""
    try:
        from database import NotesDatabase
        
        print("\n🔍 Testing search functionality...")
        db = NotesDatabase()
        
        # Test searches with common terms
        test_queries = ["data", "math", "physics", "18CS51", "BCS301"]
        
        for query in test_queries:
            print(f"\n📝 Testing search for: '{query}'")
            results = db.search_notes(query, limit=5)
            
            print(f"   Result type: {results['type']}")
            if results['results']:
                print(f"   Found: {len(results['results'])} results")
                if results['type'] == 'exact':
                    for result in results['results'][:2]:
                        print(f"   - {result['full_name']} ({result['semester']})")
                elif results['type'] == 'partial':
                    for result in results['results'][:2]:
                        print(f"   - {result['semester']} - {result['branch']}")
            else:
                print("   No results found")
                
        return True
        
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False

def test_environment_variables():
    """Test if required environment variables are set"""
    print("🔑 Testing environment variables...")
    
    required_vars = ["MONGODB_URI", "BOT_TOKEN"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            print(f"   ✅ {var} is set")
    
    if missing_vars:
        print(f"   ❌ Missing variables: {', '.join(missing_vars)}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Search Functionality Tests\n")
    
    # Test 1: Environment variables
    env_ok = test_environment_variables()
    
    if not env_ok:
        print("\n❌ Environment variables test failed!")
        print("Please check your .env file")
        return
    
    # Test 2: Database connection
    db_ok = test_database_connection()
    
    if not db_ok:
        print("\n❌ Database connection test failed!")
        print("Please check your MongoDB connection")
        return
    
    # Test 3: Search functionality
    search_ok = test_search_functionality()
    
    if not search_ok:
        print("\n❌ Search functionality test failed!")
        return
    
    print("\n" + "="*50)
    print("🎉 All tests passed!")
    print("✅ Search functionality should be working")
    print("\nIf users are still having issues:")
    print("1. Check if the bot has the right permissions")
    print("2. Verify the database has been synced with notes")
    print("3. Test with simple queries like 'data' or 'math'")

if __name__ == "__main__":
    main()