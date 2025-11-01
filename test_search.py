#!/usr/bin/env python3
"""
Test script to debug the search functionality for BCS301
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import NotesDatabase

def test_search():
    """Test the search functionality"""
    try:
        # Initialize database
        print("🔌 Connecting to database...")
        db = NotesDatabase()
        
        # Test the total count first
        total_notes = db.count_notes()
        print(f"📊 Total notes in database: {total_notes}")
        
        if total_notes == 0:
            print("❌ No notes found in database! Need to import data first.")
            return
        
        # Test search for "bcs301"
        print("\n🔍 Testing search for 'bcs301'...")
        results = db.search_notes("bcs301")
        
        print(f"📋 Search results type: {results['type']}")
        print(f"📋 Number of results: {len(results['results'])}")
        
        if results['results']:
            print("\n✅ Found results:")
            if results['type'] == 'exact':
                for i, result in enumerate(results['results'], 1):
                    print(f"  {i}. {result['full_name']}")
                    print(f"     URL: {result['branch_url']}")
                    print(f"     Semester: {result['semester']}, Branch: {result['branch']}")
                    print(f"     Match type: {result['match_type']}")
                    print()
            elif results['type'] == 'partial':
                for i, branch in enumerate(results['results'], 1):
                    print(f"  Branch {i}: {branch['branch_url']}")
                    print(f"     Semester: {branch['semester']}, Branch: {branch['branch']}")
                    for subject in branch['subjects']:
                        print(f"       - {subject['full_name']} (score: {subject['score']})")
                    print()
        else:
            print("❌ No results found for 'bcs301'")
            
            # Let's check what's actually in the database
            print("\n🔍 Checking what subject codes exist...")
            pipeline = [
                {"$group": {"_id": "$subject_code", "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}},
                {"$limit": 20}
            ]
            
            subject_codes = list(db.collection.aggregate(pipeline))
            print("📋 Sample subject codes in database:")
            for code in subject_codes:
                if code['_id']:  # Only show non-empty codes
                    print(f"  - {code['_id']} ({code['count']} entries)")
            
            # Let's also check for anything containing "301"
            print("\n🔍 Searching for anything containing '301'...")
            results_301 = db.search_notes("301")
            print(f"📋 Results for '301': {len(results_301['results'])}")
            
            if results_301['results']:
                print("✅ Found matches for '301':")
                if results_301['type'] == 'partial':
                    for branch in results_301['results'][:3]:  # Show first 3
                        for subject in branch['subjects'][:3]:  # Show first 3 subjects
                            print(f"  - {subject['full_name']}")
            
            # Check for BCS specifically
            print("\n🔍 Searching for 'BCS'...")
            results_bcs = db.search_notes("BCS")
            print(f"📋 Results for 'BCS': {len(results_bcs['results'])}")
            
            if results_bcs['results']:
                print("✅ Found matches for 'BCS':")
                if results_bcs['type'] == 'partial':
                    for branch in results_bcs['results'][:3]:
                        for subject in branch['subjects'][:3]:
                            print(f"  - {subject['full_name']}")
        
    except Exception as e:
        print(f"❌ Error during search test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_search()