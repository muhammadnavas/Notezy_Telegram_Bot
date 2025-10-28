import os
from typing import List, Dict, Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import json

class NotesDatabase:
    def __init__(self, db_name="notezy_bot"):
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            raise ValueError("MONGODB_URI not found in environment variables")
        
        try:
            self.client = MongoClient(mongodb_uri)
            self.db = self.client[db_name]
            self.collection = self.db.notes
            
            # Test connection
            self.client.admin.command('ping')
            print("✅ Connected to MongoDB successfully")
            
            # Create indexes for better performance
            self.collection.create_index([("subject_code", 1)])
            self.collection.create_index([("subject_name", 1)])
            self.collection.create_index([("full_name", 1)])
            self.collection.create_index([("semester", 1), ("branch", 1)])
            
        except ConnectionFailure:
            print("❌ Failed to connect to MongoDB")
            raise
    
    def add_note(self, subject_code: str, subject_name: str, branch_url: str, 
                 semester: str = None, branch: str = None):
        """Add a single note to database"""
        full_name = f"{subject_code} - {subject_name}" if subject_code else subject_name
        
        note_doc = {
            "subject_code": subject_code,
            "subject_name": subject_name,
            "full_name": full_name,
            "branch_url": branch_url,
            "semester": semester,
            "branch": branch
        }
        
        result = self.collection.insert_one(note_doc)
        return result.inserted_id
    
    def bulk_insert(self, notes_list: List[Dict]):
        """Bulk insert notes from a list of dictionaries"""
        documents = []
        
        for note in notes_list:
            subject_code = note.get('subject_code', '')
            subject_name = note.get('subject_name', '')
            full_name = f"{subject_code} - {subject_name}" if subject_code else subject_name
            
            doc = {
                "subject_code": subject_code,
                "subject_name": subject_name,
                "full_name": full_name,
                "branch_url": note['branch_url'],
                "semester": note.get('semester'),
                "branch": note.get('branch')
            }
            documents.append(doc)
        
        if documents:
            result = self.collection.insert_many(documents)
            print(f"✅ Inserted {len(result.inserted_ids)} notes successfully")
            return result.inserted_ids
        return []
    
    def search_notes(self, query: str, limit: int = 10) -> Dict:
        """Search notes by subject code or name"""
        # First, try to find exact matches
        exact_matches = list(self.collection.find({
            "$or": [
                {"subject_code": {"$regex": f"^{query}$", "$options": "i"}},
                {"full_name": {"$regex": f"^{query}$", "$options": "i"}}
            ]
        }).limit(limit))
        
        if exact_matches:
            # Return exact matches
            results = []
            for note in exact_matches:
                results.append({
                    'full_name': note['full_name'],
                    'branch_url': note['branch_url'],
                    'semester': note['semester'],
                    'branch': note['branch'],
                    'exact_match': True
                })
            return {"type": "exact", "results": results}
        
        # If no exact matches, find related subjects in same semester/branch
        # First, find what semester/branch the query might belong to
        related_subjects = list(self.collection.find({
            "$or": [
                {"subject_code": {"$regex": query, "$options": "i"}},
                {"subject_name": {"$regex": query, "$options": "i"}},
                {"full_name": {"$regex": query, "$options": "i"}}
            ]
        }).limit(5))
        
        if related_subjects:
            # Get semester and branch from first match
            semester = related_subjects[0]['semester']
            branch = related_subjects[0]['branch']
            
            # Find all subjects in this semester and branch
            all_subjects = list(self.collection.find({
                "semester": semester,
                "branch": branch
            }).limit(20))
            
            results = []
            for note in all_subjects:
                results.append({
                    'full_name': note['full_name'],
                    'branch_url': note['branch_url'],
                    'semester': note['semester'],
                    'branch': note['branch'],
                    'exact_match': False
                })
            
            return {
                "type": "related", 
                "results": results, 
                "searched_semester": semester,
                "searched_branch": branch
            }
        
        return {"type": "none", "results": []}
    
    def get_all_notes(self) -> List[Dict]:
        """Get all notes from database"""
        notes = list(self.collection.find({}, {"_id": 0, "full_name": 1, "branch_url": 1}))
        return notes
    
    def import_from_json(self, json_file: str):
        """Import notes from JSON file"""
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        notes_list = []
        for full_name, branch_url in data.items():
            # Try to extract subject code and name
            parts = full_name.split(' - ', 1)
            if len(parts) == 2:
                subject_code = parts[0].strip()
                subject_name = parts[1].strip()
            else:
                subject_code = ''
                subject_name = full_name
            
            notes_list.append({
                'subject_code': subject_code,
                'subject_name': subject_name,
                'branch_url': branch_url
            })
        
        self.bulk_insert(notes_list)
    
    def export_to_json(self, json_file: str):
        """Export notes to JSON file"""
        notes = self.get_all_notes()
        data = {note['full_name']: note['branch_url'] for note in notes}
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"✅ Exported {len(data)} notes to {json_file}")
    
    def count_notes(self) -> int:
        """Get total count of notes"""
        return self.collection.count_documents({})
    
    def clear_all(self):
        """Clear all notes (use with caution!)"""
        result = self.collection.delete_many({})
        print(f"⚠️  Cleared {result.deleted_count} notes from database")


if __name__ == "__main__":
    # Example usage
    db = NotesDatabase()
    
    print(f"📊 Total notes in database: {db.count_notes()}")
    
    # Example: Search for notes
    results = db.search_notes("data")
    print(f"\n🔍 Search results for 'data': {len(results)} found")
    for note in results[:3]:
        print(f"  - {note['full_name']}")
