#!/usr/bin/env python3
"""
Simple test to verify search is working and identify specific issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_specific_search_cases():
    """Test specific search cases that users might be trying"""
    try:
        from database import NotesDatabase
        
        print("🔍 Testing specific search cases that users might try...")
        db = NotesDatabase()
        
        # Common user queries
        test_cases = [
            # Subject codes
            "BCS301", "18CS51", "18CS52", "BCS401", 
            # Subject names
            "Data Structures", "Mathematics", "Physics", "Chemistry",
            "Operating Systems", "Computer Networks", "DBMS",
            # Common short terms
            "math", "data", "OS", "CN", "java", "python", "C++",
            # Semester queries
            "3rd sem", "4th sem", "sem3", "sem4",
            # Partial codes
            "BCS", "18CS", "301", "401"
        ]
        
        working_queries = []
        not_working_queries = []
        
        for query in test_cases:
            print(f"\n🔍 Testing: '{query}'")
            results = db.search_notes(query, limit=5)
            
            if results['results']:
                print(f"   ✅ Found {len(results['results'])} results ({results['type']})")
                working_queries.append(query)
                
                # Show some results
                if results['type'] == 'exact':
                    for result in results['results'][:2]:
                        print(f"      - {result['full_name']}")
                elif results['type'] == 'partial':
                    for result in results['results'][:2]:
                        print(f"      - {result['semester']} - {result['branch']}")
            else:
                print(f"   ❌ No results found")
                not_working_queries.append(query)
        
        print("\n" + "="*60)
        print(f"✅ Working queries ({len(working_queries)}): {', '.join(working_queries)}")
        print(f"❌ Not working queries ({len(not_working_queries)}): {', '.join(not_working_queries)}")
        
        success_rate = len(working_queries) / len(test_cases) * 100
        print(f"📊 Success rate: {success_rate:.1f}%")
        
        return success_rate > 50  # Consider it working if >50% of queries work
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_database_content():
    """Check what's actually in the database"""
    try:
        from database import NotesDatabase
        
        print("📊 Checking database content...")
        db = NotesDatabase()
        
        # Get some sample notes
        sample_notes = list(db.collection.find({}).limit(10))
        
        print(f"Total notes: {db.count_notes()}")
        print("\nSample notes:")
        for note in sample_notes[:5]:
            print(f"  - {note.get('full_name', 'N/A')} ({note.get('semester', 'N/A')})")
        
        # Check semesters
        semesters = db.collection.distinct("semester")
        print(f"\nAvailable semesters: {semesters}")
        
        # Check branches  
        branches = db.collection.distinct("branch")
        print(f"Available branches: {branches}")
        
        # Check subject codes
        codes = list(db.collection.distinct("subject_code"))
        non_empty_codes = [code for code in codes if code.strip()]
        print(f"Sample subject codes: {non_empty_codes[:10]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database content check failed: {e}")
        return False

def main():
    """Run diagnostic tests"""
    print("🔧 Diagnostic Tests for Search Functionality\n")
    
    # Check database content
    print("1️⃣ Database Content Check")
    db_ok = check_database_content()
    
    if not db_ok:
        print("❌ Database content check failed")
        return
    
    print("\n" + "="*60)
    
    # Test specific search cases
    print("2️⃣ Search Query Tests")
    search_ok = test_specific_search_cases()
    
    if search_ok:
        print("\n✅ Search functionality appears to be working!")
        print("\nPossible reasons users might think it's not working:")
        print("1. They're using queries that don't match any data")
        print("2. Bot response is slow (database search takes time)")
        print("3. Bot permissions or network issues")
        print("4. Users expecting different search behavior")
    else:
        print("\n❌ Search functionality has issues!")
        print("Many common queries are not returning results.")
    
    print("\n💡 Recommendations:")
    print("- Test the bot with queries like 'BCS301' or 'data'")
    print("- Check bot logs for any runtime errors")
    print("- Ensure bot has proper message permissions")
    print("- Consider syncing more data to the database")

if __name__ == "__main__":
    main()