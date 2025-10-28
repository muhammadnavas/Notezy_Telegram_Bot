"""
Quick setup script for Notezy branch URLs
Run this to populate your database with branch page URLs
"""

from database import NotesDatabase

def setup_branch_urls():
    """
    Add notes with branch URLs instead of individual note links
    This keeps users on your website for page views
    """
    
    db = NotesDatabase()
    
    # Clear existing data if needed
    confirm = input("Clear existing notes? (yes/no): ").strip().lower()
    if confirm == 'yes':
        db.clear_all()
    
    # Sample notes data - replace with your actual data
    notes_data = [
        # Computer Science - Sem 5
        {
            'subject_code': '18CS51',
            'subject_name': 'Data Structures',
            'branch_url': '/Sem5/computerscience',
            'semester': 'Sem5',
            'branch': 'Computer Science'
        },
        {
            'subject_code': '18CS52',
            'subject_name': 'Operating Systems',
            'branch_url': '/Sem5/computerscience',
            'semester': 'Sem5',
            'branch': 'Computer Science'
        },
        {
            'subject_code': '18CS53',
            'subject_name': 'Database Management Systems',
            'branch_url': '/Sem5/computerscience',
            'semester': 'Sem5',
            'branch': 'Computer Science'
        },
        {
            'subject_code': '18CS54',
            'subject_name': 'Computer Networks',
            'branch_url': '/Sem5/computerscience',
            'semester': 'Sem5',
            'branch': 'Computer Science'
        },
        
        # Mechanical - Sem 5
        {
            'subject_code': '18ME51',
            'subject_name': 'Thermodynamics',
            'branch_url': '/Sem5/mechanical',
            'semester': 'Sem5',
            'branch': 'Mechanical'
        },
        {
            'subject_code': '18ME52',
            'subject_name': 'Fluid Mechanics',
            'branch_url': '/Sem5/mechanical',
            'semester': 'Sem5',
            'branch': 'Mechanical'
        },
        
        # Electronics - Sem 5
        {
            'subject_code': '18EC51',
            'subject_name': 'Digital Signal Processing',
            'branch_url': '/Sem5/electronics',
            'semester': 'Sem5',
            'branch': 'Electronics'
        },
        
        # Add more notes here...
        # Copy this pattern for all your 300+ notes
    ]
    
    db.bulk_insert(notes_data)
    print(f"✅ Added {len(notes_data)} sample notes")
    print("\n📝 To add all 300+ notes:")
    print("1. Edit this file and add all your notes to notes_data list")
    print("2. Or use import_notes.py for bulk import from CSV/JSON/database")
    print("3. Run: python bot.py")

if __name__ == "__main__":
    setup_branch_urls()
    
    # Show stats
    db = NotesDatabase()
    print(f"\n📊 Total notes in database: {db.count_notes()}")
