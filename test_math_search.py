#!/usr/bin/env python3
"""
Test script for checking mathematics search results
"""
from database import NotesDatabase

def test_mathematics_search():
    try:
        print("🔍 Testing mathematics search...")
        db = NotesDatabase()
        result = db.search_notes('mathematics', limit=100)
        
        print(f'Search type: {result["type"]}')
        print(f'Results count: {len(result["results"])}')
        
        if result['results']:
            print('\n📚 All mathematics subjects found:')
            
            # Deduplicate by subject name
            seen_subjects = set()
            unique_subjects = []
            
            for note in result['results']:
                subject_name = note['full_name']
                if subject_name not in seen_subjects:
                    seen_subjects.add(subject_name)
                    unique_subjects.append(note)
            
            print(f'📊 Unique subjects: {len(unique_subjects)}')
            print(f'📊 Total matches (with duplicates): {len(result["results"])}')
            
            for i, note in enumerate(unique_subjects, 1):
                print(f'{i}. {note["full_name"]} - {note["semester"]} - {note["branch"]}')
                
        print("\n✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mathematics_search()