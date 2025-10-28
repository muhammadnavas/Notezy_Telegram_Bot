"""
Import notes from various sources into the database
"""

from database import NotesDatabase
import json
import csv
import os

def import_from_csv(csv_file: str):
    """
    Import notes from CSV file
    CSV format: subject_code, subject_name, branch_url, semester, branch
    """
    db = NotesDatabase()
    notes_list = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            notes_list.append({
                'subject_code': row.get('subject_code', ''),
                'subject_name': row.get('subject_name', ''),
                'branch_url': row['branch_url'],  # Changed from drive_link
                'semester': row.get('semester', ''),
                'branch': row.get('branch', '')
            })
    
    db.bulk_insert(notes_list)
    print(f"✅ Imported {len(notes_list)} notes from CSV")

def import_from_json(json_file: str):
    """
    Import notes from JSON file
    Format 1: {"Subject Code - Name": "link"}
    Format 2: [{"subject_code": "", "subject_name": "", "drive_link": ""}]
    """
    db = NotesDatabase()
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, dict):
        # Format 1: Simple dict
        notes_list = []
        for full_name, drive_link in data.items():
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
                'drive_link': drive_link
            })
        
        db.bulk_insert(notes_list)
        print(f"✅ Imported {len(notes_list)} notes from JSON")
    
    elif isinstance(data, list):
        # Format 2: List of dicts
        db.bulk_insert(data)
        print(f"✅ Imported {len(data)} notes from JSON")

def import_from_mongodb():
    """
    Import notes from existing MongoDB collection
    Based on your schema: title, subject, fileUrl, sem, department[]
    """
    try:
        from pymongo import MongoClient
        
        # Source MongoDB connection (your existing database)
        source_uri = os.getenv("MONGODB_URI")
        source_client = MongoClient(source_uri)
        source_db = source_client["notezy"]  # Your database name
        source_collection = source_db["notes"]  # Your collection name
        
        # Get all notes from source
        source_notes = list(source_collection.find({}))
        
        if not source_notes:
            print("❌ No notes found in source MongoDB collection")
            return
        
        # Transform and import to our database
        notes_list = []
        
        for note in source_notes:
            subject_full = note.get('subject', '')
            sem = note.get('sem', '')
            departments = note.get('department', [])
            
            # Extract subject code and name from subject field
            # Format: "Subject Name (CODE1/CODE2)"
            if '(' in subject_full and ')' in subject_full:
                subject_name = subject_full.split('(')[0].strip()
                codes_part = subject_full.split('(')[1].split(')')[0]
                # Take first code as subject_code
                subject_code = codes_part.split('/')[0].strip()
            else:
                subject_name = subject_full
                subject_code = ''
            
            # Create entries for each department
            for dept in departments:
                branch_url = f"/{sem}/{dept}"
                
                notes_list.append({
                    'subject_code': subject_code,
                    'subject_name': subject_name,
                    'branch_url': branch_url,
                    'semester': sem,
                    'branch': dept
                })
        
        # Remove duplicates (same subject in same semester/branch)
        unique_notes = []
        seen = set()
        for note in notes_list:
            key = (note['subject_code'], note['subject_name'], note['semester'], note['branch'])
            if key not in seen:
                seen.add(key)
                unique_notes.append(note)
        
        # Import to our database
        db = NotesDatabase()
        db.bulk_insert(unique_notes)
        
        print(f"✅ Imported {len(unique_notes)} unique notes from MongoDB")
        print(f"📊 Processed {len(source_notes)} source documents")
        
        source_client.close()
    
    except Exception as e:
        print(f"❌ Error importing from MongoDB: {e}")
        import traceback
        traceback.print_exc()

def import_from_postgresql():
    """
    Import notes from PostgreSQL database
    """
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        # PostgreSQL connection configuration
        conn = psycopg2.connect(
            host="your_host",
            database="your_database",
            user="your_username",
            password="your_password"
        )
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Adjust this query based on your PostgreSQL table structure
        cursor.execute('''
            SELECT 
                subject_code,
                subject_name,
                CONCAT('/Sem', semester_number, '/', LOWER(branch_name)) as branch_url,
                CONCAT('Sem', semester_number) as semester,
                branch_name as branch
            FROM notes_table
        ''')
        
        notes_list = cursor.fetchall()
        
        conn.close()
        
        # Import to SQLite
        db = NotesDatabase()
        db.bulk_insert([dict(row) for row in notes_list])
        
        print(f"✅ Imported {len(notes_list)} notes from PostgreSQL")
    
    except ImportError:
        print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
    except Exception as e:
        print(f"❌ Error importing from PostgreSQL: {e}")

def create_sample_csv():
    """Create a sample CSV template"""
    with open('notes_template.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['subject_code', 'subject_name', 'branch_url', 'semester', 'branch'])
        writer.writerow(['18CS51', 'Data Structures', '/Sem5/computerscience', 'Sem5', 'Computer Science'])
        writer.writerow(['18CS52', 'Operating Systems', '/Sem5/computerscience', 'Sem5', 'Computer Science'])
        writer.writerow(['18ME51', 'Thermodynamics', '/Sem5/mechanical', 'Sem5', 'Mechanical'])
    
    print("✅ Created notes_template.csv - Fill this with your data")

if __name__ == "__main__":
    print("=" * 50)
    print("📥 Notes Import Tool")
    print("=" * 50)
    print("\nChoose import method:")
    print("1. Import from JSON file")
    print("2. Import from CSV file")
    print("3. Import from MySQL database")
    print("4. Import from PostgreSQL database")
    print("5. Create CSV template")
    print("6. Import from MongoDB")  # Added MongoDB option
    print()
    
    choice = input("Enter your choice (1-6): ").strip()
    
    if choice == '1':
        file = input("Enter JSON file path (default: notes_data.json): ").strip() or "notes_data.json"
        import_from_json(file)
    
    elif choice == '2':
        file = input("Enter CSV file path: ").strip()
        if file:
            import_from_csv(file)
        else:
            print("❌ CSV file path required")
    
    elif choice == '3':
        print("\n⚠️  Configure MySQL connection in import_notes.py first")
        confirm = input("Have you configured MySQL connection? (yes/no): ").strip().lower()
        if confirm == 'yes':
            import_from_mysql()
    
    elif choice == '4':
        print("\n⚠️  Configure PostgreSQL connection in import_notes.py first")
        confirm = input("Have you configured PostgreSQL connection? (yes/no): ").strip().lower()
        if confirm == 'yes':
            import_from_postgresql()
    
    elif choice == '5':
        create_sample_csv()
    
    elif choice == '6':
        print("\n⚠️  Configure MongoDB source in import_notes.py first")
        confirm = input("Have you configured MongoDB source? (yes/no): ").strip().lower()
        if confirm == 'yes':
            import_from_mongodb()
    
    # Show stats
    db = NotesDatabase()
    print(f"\n📊 Total notes in database: {db.count_notes()}")
