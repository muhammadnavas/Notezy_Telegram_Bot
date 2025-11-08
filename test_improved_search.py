#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv()

from database import NotesDatabase

def test_improved_search():
    db = NotesDatabase()
    
    # Test problematic queries
    test_queries = ['math', 'OS', '3rd sem', 'DBMS', 'CN', '18CS51', 'BCS', '301']
    
    print("Testing improved search functionality:")
    print("=" * 50)
    
    for q in test_queries:
        result = db.search_notes(q, limit=3)
        print(f'Query: "{q}"')
        print(f'  Type: {result["type"]}, Results: {len(result["results"])}')
        
        if result['results']:
            if result['type'] == 'exact':
                print(f'  Sample: {result["results"][0]["full_name"]}')
            elif result['type'] == 'partial':
                if result["results"]:
                    sample = result["results"][0]
                    print(f'  Sample: {sample["semester"]} - {sample["branch"]}')
        print()

if __name__ == "__main__":
    test_improved_search()