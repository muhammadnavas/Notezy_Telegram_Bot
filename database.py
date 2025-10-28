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
        """Advanced search with multiple strategies"""
        query_lower = query.lower().strip()
        
        # Strategy 1: Exact subject code match (highest priority)
        exact_code_match = list(self.collection.find({
            "subject_code": {"$regex": f"^{query_lower}$", "$options": "i"}
        }).limit(limit))
        
        if exact_code_match:
            results = []
            for note in exact_code_match:
                results.append({
                    'full_name': note['full_name'],
                    'branch_url': note['branch_url'],
                    'semester': note['semester'],
                    'branch': note['branch'],
                    'exact_match': True,
                    'match_type': 'exact_code'
                })
            return {"type": "exact", "results": results, "query": query}
        
        # Strategy 2: Exact subject name match
        exact_name_match = list(self.collection.find({
            "subject_name": {"$regex": f"^{query_lower}$", "$options": "i"}
        }).limit(limit))
        
        if exact_name_match:
            results = []
            for note in exact_name_match:
                results.append({
                    'full_name': note['full_name'],
                    'branch_url': note['branch_url'],
                    'semester': note['semester'],
                    'branch': note['branch'],
                    'exact_match': True,
                    'match_type': 'exact_name'
                })
            return {"type": "exact", "results": results, "query": query}
        
        # Strategy 3: Partial matches with scoring
        partial_matches = []
        
        # Search in multiple fields with different weights
        search_fields = [
            ("subject_code", 10),    # Highest weight
            ("subject_name", 8),     # High weight
            ("full_name", 6),        # Medium weight
            ("semester", 3),         # Lower weight
            ("branch", 2)            # Lowest weight
        ]
        
        for field, weight in search_fields:
            matches = list(self.collection.find({
                field: {"$regex": query_lower, "$options": "i"}
            }).limit(limit * 2))  # Get more for scoring
            
            for match in matches:
                # Calculate relevance score
                score = weight
                field_value = match[field].lower()
                
                # Bonus for exact word matches
                if query_lower in field_value.split():
                    score += 5
                
                # Bonus for starting with query
                if field_value.startswith(query_lower):
                    score += 3
                
                # Bonus for shorter matches (more specific)
                score += max(0, 10 - len(field_value))
                
                partial_matches.append({
                    **match,
                    'score': score,
                    'matched_field': field
                })
        
        # Remove duplicates and sort by score
        seen = set()
        unique_matches = []
        for match in partial_matches:
            key = (match['subject_code'], match['subject_name'], match['semester'], match['branch'])
            if key not in seen:
                seen.add(key)
                unique_matches.append(match)
        
        # Sort by score (highest first)
        unique_matches.sort(key=lambda x: x['score'], reverse=True)
        top_matches = unique_matches[:limit]
        
        if top_matches:
            # Group by branch for better display
            branch_groups = {}
            for match in top_matches:
                url = match['branch_url']
                if url not in branch_groups:
                    branch_groups[url] = {
                        'subjects': [],
                        'semester': match['semester'],
                        'branch': match['branch'],
                        'max_score': 0
                    }
                branch_groups[url]['subjects'].append({
                    'full_name': match['full_name'],
                    'score': match['score'],
                    'matched_field': match['matched_field']
                })
                branch_groups[url]['max_score'] = max(branch_groups[url]['max_score'], match['score'])
            
            # Sort branches by best score
            sorted_branches = sorted(branch_groups.items(), 
                                   key=lambda x: x[1]['max_score'], reverse=True)
            
            results = []
            for branch_url, data in sorted_branches:
                results.append({
                    'branch_url': branch_url,
                    'semester': data['semester'],
                    'branch': data['branch'],
                    'subjects': data['subjects'][:5],  # Top 5 subjects per branch
                    'total_subjects': len(data['subjects'])
                })
            
            return {
                "type": "partial", 
                "results": results, 
                "query": query,
                "total_matches": len(unique_matches)
            }
        
        return {"type": "none", "results": [], "query": query}
    
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
    
    def sync_from_source(self, source_db_name="test", source_collection="notes"):
        """Sync new notes from source MongoDB database"""
        try:
            # Connect to source database
            source_db = self.client[source_db_name]
            source_coll = source_db[source_collection]
            
            # Get all source documents
            source_docs = list(source_coll.find({}))
            print(f"📡 Found {len(source_docs)} documents in source")
            
            # Transform and prepare for bulk insert
            notes_list = []
            existing_count = 0
            
            for doc in source_docs:
                subject_full = doc.get('subject', '')
                sem = doc.get('sem', '')
                departments = doc.get('department', [])
                
                # Extract subject code and name
                if '(' in subject_full and ')' in subject_full:
                    subject_name = subject_full.split('(')[0].strip()
                    codes_part = subject_full.split('(')[1].split(')')[0]
                    subject_code = codes_part.split('/')[0].strip()
                else:
                    subject_name = subject_full
                    subject_code = ''
                
                # Create entries for each department
                for dept in departments:
                    branch_url = f"/{sem}/{dept}"
                    
                    # Check if this combination already exists
                    existing = self.collection.find_one({
                        "subject_code": subject_code,
                        "subject_name": subject_name,
                        "semester": sem,
                        "branch": dept
                    })
                    
                    if existing:
                        existing_count += 1
                    else:
                        notes_list.append({
                            'subject_code': subject_code,
                            'subject_name': subject_name,
                            'branch_url': branch_url,
                            'semester': sem,
                            'branch': dept
                        })
            
            # Insert new notes
            if notes_list:
                self.bulk_insert(notes_list)
                print(f"✅ Synced {len(notes_list)} new notes")
            else:
                print("✅ No new notes to sync")
            
            print(f"📊 Skipped {existing_count} existing notes")
            
            return {
                "new_notes": len(notes_list),
                "existing_notes": existing_count,
                "total_source": len(source_docs)
            }
            
        except Exception as e:
            print(f"❌ Sync failed: {e}")
            return None


if __name__ == "__main__":
    # Example usage
    db = NotesDatabase()
    
    print(f"📊 Total notes in database: {db.count_notes()}")
    
    # Example: Search for notes
    results = db.search_notes("data")
    print(f"\n🔍 Search results for 'data': {len(results)} found")
    for note in results[:3]:
        print(f"  - {note['full_name']}")
