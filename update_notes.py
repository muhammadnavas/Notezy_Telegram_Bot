"""
Manual script to update notes_data.json with your Google Drive links
Run this script whenever you add new notes to update the bot's database
"""

import json

def update_notes():
    """
    Add or update notes manually
    Format: "Subject Code - Subject Name": "Google Drive Link"
    """
    
    notes = {
        # Semester 5 - Computer Science
        "18CS51 - Data Structures": "https://drive.google.com/your-link-here",
        "18CS52 - Operating Systems": "https://drive.google.com/your-link-here",
        "18CS53 - Database Management": "https://drive.google.com/your-link-here",
        "18CS54 - Computer Networks": "https://drive.google.com/your-link-here",
        "18CS55 - Python Programming": "https://drive.google.com/your-link-here",
        
        # Add more subjects here
        # "Subject Code - Name": "Google Drive Link",
    }
    
    # Save to JSON file
    with open("notes_data.json", "w") as f:
        json.dump(notes, f, indent=4)
    
    print(f"✅ Updated {len(notes)} subjects in notes_data.json")
    print("\n📚 Current subjects:")
    for subject in notes.keys():
        print(f"  - {subject}")

if __name__ == "__main__":
    update_notes()
