# Notezy Telegram Bot 📚

A Telegram bot for searching and accessing course notes by subject name or code from Notezy.online.

## Features
- 🔍 **Advanced Search** - Smart search with scoring and fuzzy matching
- 📘 Quick access to study materials via branch page links
- 👋 **Smart Greetings** - Recognizes 40+ greeting patterns in multiple languages
- 📚 **Semester Queries** - Direct links to semester pages (e.g., "4th sem", "for 3rd sem")
- 🔄 **Auto-Sync** - Automatically sync new notes from MongoDB
- 🚀 **Fast and responsive** with MongoDB backend
- 🌐 Integration with Notezy.online
- ☁️ **Render Deployment** - Ready for cloud deployment

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Copy `.env.example` to `.env` and add your credentials
   - Set `BOT_TOKEN` and `MONGODB_URI`

3. **Import notes from MongoDB:**
   ```bash
   python import_notes.py
   # Choose option 6 (MongoDB import)
   ```

4. **Run the bot:**
   ```bash
   python bot.py
   ```

## Usage

### Basic Commands
- `/start` - Welcome message with usage instructions
- `/sync` - Manually sync new notes from database (admin only)

### Search Features
- **Subject Search**: Send any subject name or code (e.g., "18CS51" or "Data Structures")
- **Semester Links**: Send "4th sem", "for 4th sem", "chemistry cycle", etc.
- **Greetings**: Send "hi", "hello", "namaste", "good morning", etc.

### Search Examples
- `18CS51` → Direct match for Data Structures
- `biology` → All biology-related subjects
- `machine learning` → AI/ML subjects
- `4th sem` → Direct links to all 4th semester branches
- `chemistry cycle` → 1st semester (Chemistry Cycle) branches

## Smart Features

### 🤖 Greeting Recognition
Recognizes greetings in multiple languages:
- **Basic**: hi, hello, hey, hai, hii, helo
- **Time-based**: good morning, good afternoon, good evening, good night
- **Cultural**: namaste, namaskar, vanakkam, salaam, assalamualaikum
- **Casual**: howdy, sup, yo, wassup, what's up
- **International**: greetings, welcome, bonjour, hola, ciao, aloha

### 📚 Semester Queries
Direct access to semester pages:
- `4th sem` → 4th Semester branches
- `for 3rd sem` → 3rd Semester branches
- `chemistry cycle` → 1st Semester (Chemistry Cycle)
- `physics cycle` → 2nd Semester (Physics Cycle)

### 🔍 Advanced Search
**Search Strategies:**
1. **Exact Code Match** - "18CS51" finds exact subject
2. **Exact Name Match** - "Data Structures" finds exact subject
3. **Partial Matches** - "data" finds all data-related subjects
4. **Smart Scoring** - Results ranked by relevance

## Syncing New Notes

### Automatic Sync:
```bash
# Run periodically to sync new notes
python auto_sync.py
```

### Manual Sync (In Telegram):
Send `/sync` command to the bot (admin only)

### What Sync Does:
- ✅ Checks for new notes in source MongoDB
- ✅ Adds only new notes (no duplicates)
- ✅ Updates bot database instantly
- ✅ Logs sync results

## Deployment to Render ☁️

### Option 1: Webhook Deployment (Recommended for Production)
Webhook deployment prevents multiple instance conflicts and is more reliable for production.

1. **Push code to GitHub/GitLab**
2. **Go to [render.com](https://render.com)**
3. **New** → **Blueprint** → Connect your repo
4. **Set environment variables:**
   - `BOT_TOKEN` - Your Telegram bot token
   - `MONGODB_URI` - MongoDB connection string
   - `WEBHOOK_URL` - Your Render service URL (will be auto-generated)
5. **Deploy** - The `render.yaml` file handles the webhook setup automatically!

### Option 2: Polling Deployment (Development/Testing)
For development or testing, use polling mode:

1. **Service Type**: Background Worker
2. **Runtime**: Python 3
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python bot.py`
5. **Environment Variables**: `BOT_TOKEN`, `MONGODB_URI` (no WEBHOOK_URL needed)

### Deployment Modes
The bot automatically chooses the deployment mode:
- **Webhook Mode**: When `WEBHOOK_URL` is set (Production)
- **Polling Mode**: When `WEBHOOK_URL` is not set (Development)

### Files for Deployment
- `start.py` - Auto-detects deployment mode
- `webhook_bot.py` - Webhook implementation
- `bot.py` - Polling implementation
- `render.yaml` - Render webhook configuration

## Database Schema

**Source MongoDB** (`test.notes`):
```json
{
  "subject": "Biology for Engineers (BBOK407/BBOC407)",
  "sem": "Sem4",
  "department": ["computerscience", "electronics", ...],
  "fileUrl": "https://drive.google.com/...",
  "title": "Module 1"
}
```

**Bot Database** (processed):
```json
{
  "subject_code": "BBOK407",
  "subject_name": "Biology for Engineers",
  "branch_url": "/Sem4/computerscience",
  "semester": "Sem4",
  "branch": "Computer Science"
}
```

## Files Structure

- `bot.py` - Main bot with polling mode (development)
- `webhook_bot.py` - Webhook-based bot (production)
- `start.py` - Auto-deployment mode selector
- `database.py` - MongoDB handler with sync functionality
- `auto_sync.py` - Automatic sync script
- `import_notes.py` - Import tools for MongoDB
- `render.yaml` - Render webhook deployment configuration
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (not in repo)

## API Integration

The bot uses these branch URLs:
- `https://www.notezy.online/Sem4/computerscience`
- `https://www.notezy.online/Sem5/mechanical`
- etc.

## Tips

- Search is case-insensitive
- Partial matches work great (e.g., "math" finds all math subjects)
- Branch links keep users on your website for page views
- Sync automatically handles new notes without downtime
- Bot responds to greetings in multiple languages
- Semester queries provide direct access to branch pages

## Future Enhancements
- Webhook-based auto-sync
- User feedback collection
- Download statistics tracking
- Admin panel for note management
- Multi-language support expansion