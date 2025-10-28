import requests
from bs4 import BeautifulSoup
import json

def scrape_notezy_notes(branch="computerscience", semester="Sem5"):
    """
    Scrape notes from Notezy website
    """
    url = f"https://www.notezy.online/{semester}/{branch}"
    
    try:
        print(f"📡 Fetching notes from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        notes_data = {}
        
        # Find all note cards/links on the page
        # Adjust the selectors based on your website's HTML structure
        note_elements = soup.find_all(['a', 'div'], class_=['note-card', 'subject-card', 'note-link'])
        
        for element in note_elements:
            # Extract subject name and link
            subject_name = element.get_text(strip=True)
            link = element.get('href', '')
            
            if subject_name and link:
                notes_data[subject_name] = link
        
        print(f"✅ Found {len(notes_data)} subjects")
        return notes_data
        
    except Exception as e:
        print(f"❌ Error scraping: {e}")
        return {}

def save_notes_data(notes_data, filename="notes_data.json"):
    """Save notes data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(notes_data, f, indent=4)
    print(f"💾 Saved to {filename}")

if __name__ == "__main__":
    # Scrape notes for different semesters/branches
    branches = {
        "Sem5": ["computerscience", "electronics", "mechanical"],
        "Sem6": ["computerscience", "electronics", "mechanical"],
    }
    
    all_notes = {}
    
    # Example: Scrape Computer Science Sem 5
    notes = scrape_notezy_notes("computerscience", "Sem5")
    all_notes.update(notes)
    
    if all_notes:
        save_notes_data(all_notes)
    else:
        print("⚠️  No notes found. Please check the website structure.")
