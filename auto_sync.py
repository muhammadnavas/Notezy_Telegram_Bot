"""
Auto-sync script for Notezy Bot
Run this periodically to sync new notes from MongoDB
"""

import os
from dotenv import load_dotenv
load_dotenv()
from database import NotesDatabase

def auto_sync():
    """Automatically sync notes from source database"""
    print("🔄 Starting auto-sync...")
    
    db = NotesDatabase()
    result = db.sync_from_source()
    
    if result:
        print("✅ Auto-sync completed!")
        print(f"   New notes: {result['new_notes']}")
        print(f"   Existing: {result['existing_notes']}")
        print(f"   Total in bot DB: {db.count_notes()}")
        
        # Log sync result
        with open("sync_log.txt", "a") as f:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] Synced {result['new_notes']} new notes\n")
    
    return result

if __name__ == "__main__":
    auto_sync()