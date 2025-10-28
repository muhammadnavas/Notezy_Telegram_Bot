# Notezy Telegram Bot 📚

A Telegram bot for searching and accessing course notes by subject name or code from Notezy.online.

## Features
- 🔍 Search notes by subject name or code
- 📘 Quick access to study materials via Google Drive links
- 🚀 Fast and responsive
- 🌐 Integration with Notezy.online

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the bot token:**
   - Your bot token is already in `.env` file
   - The bot will automatically load it

3. **Update notes database:**
   
   **Option A: Manual Update (Recommended)**
   - Edit `update_notes.py` and add your Google Drive links
   - Run: `python update_notes.py`
   
   **Option B: Web Scraper (Advanced)**
   - Edit `scraper.py` to match your website's HTML structure
   - Run: `python scraper.py`

4. **Run the bot:**
   ```bash
   python bot.py
   ```

## Usage

- Send `/start` to see the welcome message
- Send any subject name or code (e.g., "18CS51" or "Data Structures") to search for notes

## Files Structure

- `bot.py` - Main bot script
- `notes_data.json` - Database of subjects and Google Drive links
- `update_notes.py` - Manual script to update notes database
- `scraper.py` - Web scraper for Notezy.online (if needed)
- `.env` - Bot token (keep secret!)

## Updating Notes

### Method 1: Manual Update
```bash
# Edit update_notes.py with your links, then run:
python update_notes.py
```

### Method 2: Direct JSON Edit
Edit `notes_data.json` directly:
```json
{
    "18CS51 - Data Structures": "https://drive.google.com/file/d/YOUR_FILE_ID/view",
    "18CS52 - Operating Systems": "https://drive.google.com/file/d/YOUR_FILE_ID/view"
}
```

## Example Workflow

1. Upload notes to Google Drive
2. Get shareable link (make sure it's set to "Anyone with the link can view")
3. Add to `update_notes.py`:
   ```python
   "18CS51 - Data Structures": "https://drive.google.com/file/d/1abc.../view"
   ```
4. Run `python update_notes.py`
5. Restart bot if it's running

## Tips

- Use descriptive subject names for better search results
- Include both subject code and name (e.g., "18CS51 - Data Structures")
- Keep Google Drive links public or accessible with the link
- Restart the bot after updating notes_data.json
