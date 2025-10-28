# Notezy Bot - Database Setup Guide 🗄️

## Database Options for 300+ Notes

You have **multiple ways** to import your notes into the SQLite database:

---

## Option 1: Import from MySQL/PostgreSQL (Your Existing DB) ⭐ RECOMMENDED

If you already have notes in MySQL or PostgreSQL:

### Step 1: Configure Connection
Edit `import_notes.py` and update the database credentials:

**For MySQL:**
```python
mysql_config = {
    'host': 'your_host',           # e.g., 'localhost' or 'db.notezy.online'
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}
```

**For PostgreSQL:**
```python
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_username",
    password="your_password"
)
```

### Step 2: Update SQL Query
Modify the SELECT query to match your table structure and generate branch URLs:
```python
cursor.execute('''
    SELECT 
        subject_code,    -- Your column name for subject code
        subject_name,    -- Your column name for subject name
        CONCAT('/Sem', semester_number, '/', LOWER(branch_name)) as branch_url,
        CONCAT('Sem', semester_number) as semester,
        branch_name as branch
    FROM your_table_name
''')
```

This generates URLs like:
- `/Sem5/computerscience` → `https://www.notezy.online/Sem5/computerscience`
- `/Sem6/mechanical` → `https://www.notezy.online/Sem6/mechanical`

### Step 3: Install Database Driver
```bash
# For MySQL
pip install mysql-connector-python

# For PostgreSQL
pip install psycopg2-binary
```

### Step 4: Run Import
```bash
python import_notes.py
# Choose option 3 (MySQL) or 4 (PostgreSQL)
```

---

## Option 2: Import from CSV File 📊

### Step 1: Create CSV Template
```bash
python import_notes.py
# Choose option 5 to create template
```

This creates `notes_template.csv` with this format:
```csv
subject_code,subject_name,branch_url,semester,branch
18CS51,Data Structures,/Sem5/computerscience,Sem5,Computer Science
18CS52,Operating Systems,/Sem5/computerscience,Sem5,Computer Science
18ME51,Thermodynamics,/Sem5/mechanical,Sem5,Mechanical
```

### Step 2: Fill Your Data
- Open `notes_template.csv` in Excel or Google Sheets
- Add all 300+ notes
- Save as CSV

### Step 3: Import
```bash
python import_notes.py
# Choose option 2 and provide CSV file path
```

---

## Option 3: Import from JSON File 📄

### Step 1: Create JSON File
Create `my_notes.json`:
```json
{
    "18CS51 - Data Structures": "/Sem5/computerscience",
    "18CS52 - Operating Systems": "/Sem5/computerscience",
    "18ME51 - Thermodynamics": "/Sem5/mechanical"
}
```

Or use array format:
```json
[
    {
        "subject_code": "18CS51",
        "subject_name": "Data Structures",
        "branch_url": "/Sem5/computerscience",
        "semester": "Sem5",
        "branch": "Computer Science"
    }
]
```

### Step 2: Import
```bash
python import_notes.py
# Choose option 1
```

---

## Option 4: Use Python Script (Programmatic)

Create a script to fetch from your database and import:

```python
from database import NotesDatabase

db = NotesDatabase()

# Your notes data
```python
notes_list = [
    {
        'subject_code': '18CS51',
        'subject_name': 'Data Structures',
        'branch_url': '/Sem5/computerscience',  # Branch page URL
        'semester': 'Sem5',
        'branch': 'Computer Science'
    },
    # ... 300+ more notes
]
```

db.bulk_insert(notes_list)
print(f"✅ Imported {len(notes_list)} notes")
```

---

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Import your notes (interactive menu)
python import_notes.py

# Check database stats
python database.py

# Start the bot
python bot.py
```

---

## Database Schema

```sql
notes (
    id              INTEGER PRIMARY KEY,
    subject_code    TEXT,           -- e.g., "18CS51"
    subject_name    TEXT,           -- e.g., "Data Structures"
    full_name       TEXT,           -- e.g., "18CS51 - Data Structures"
    branch_url      TEXT NOT NULL,  -- Branch page URL (e.g., "/Sem5/computerscience")
    semester        TEXT,           -- e.g., "Sem5"
    branch          TEXT,           -- e.g., "Computer Science"
    created_at      TIMESTAMP,
    updated_at      TIMESTAMP
)
```

---

## Example: MySQL to SQLite Migration

```bash
# 1. Install MySQL connector
pip install mysql-connector-python

# 2. Edit import_notes.py with your MySQL credentials
# 3. Run import
python import_notes.py
# Choose option 3

# 4. Verify
python database.py
# Should show: "Total notes in database: 300+"

# 5. Start bot
python bot.py
```

---

## How It Works Now

1. **User searches:** "18CS51" or "Data Structures"
2. **Bot finds:** All matching subjects in that branch
3. **Bot responds:** Links to branch pages (e.g., `https://www.notezy.online/Sem5/computerscience`)
4. **User clicks:** Goes to your website branch page (keeps page views!)
5. **User browses:** Finds the specific note they want on your site

## Benefits

✅ **Keeps page views** on your website  
✅ **No direct external links** to Google Drive  
✅ **Users stay on your site** to browse notes  
✅ **Easy to manage** 300+ notes  
✅ **Fast search** with database  

## Example Bot Response

When user searches "18CS51":
```
🏫 Sem5 - Computer Science
📚 Subjects: 18CS51 - Data Structures, 18CS52 - Operating Systems
🔗 View Notes (https://www.notezy.online/Sem5/computerscience)
```  

---

## What Database Do You Have?

Please tell me:
1. **Database type?** (MySQL, PostgreSQL, MongoDB, etc.)
2. **Table/Collection name?**
3. **Column names?** (for subject code, name, drive link, etc.)

I can help you write the exact import script! 🚀
