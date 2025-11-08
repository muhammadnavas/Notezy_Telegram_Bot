#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv()

import bot
print('Bot imported successfully')

from database import NotesDatabase
db = NotesDatabase()
print(f'Database connected with {db.count_notes()} notes')

# Test search function
try:
    result = db.search_notes('math', limit=3)
    print(f'Search test: math -> {result["type"]} with {len(result["results"])} results')
except Exception as e:
    print(f'Search error: {e}')
    import traceback
    traceback.print_exc()