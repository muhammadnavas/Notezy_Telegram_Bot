# Notezy Telegram Bot 📚

A Telegram bot for searching and accessing course notes by subject name or code from Notezy.online.

## Features
- 🔍 **Advanced Search** - Smart search with scoring and fuzzy matching
- 🤖 **AI-Powered Enhancement** - Grok AI integration for intelligent responses
- 📘 Quick access to study materials via branch page links
- 👋 **Smart Greetings** - Recognizes 40+ greeting patterns in multiple languages
- 📚 **Semester Queries** - Direct links to semester pages (e.g., "4th sem", "for 3rd sem")
- 🔄 **Auto-Sync** - Automatically sync new notes from MongoDB
- 🚀 **Fast and responsive** with MongoDB backend
- 🌐 Integration with Notezy.online
- ☁️ **Render Deployment** - Ready for cloud deployment

### 🤖 AI Features
- **Query Enhancement** - AI analyzes and improves search queries for better results
- **Personalized Greetings** - Context-aware greetings based on time and user
- **Smart Suggestions** - AI-generated alternatives when searches return no results
- **Study Tips** - Personalized study advice for engineering students
- **Feedback Prompts** - AI-generated specific questions to improve the bot

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Copy `.env.example` to `.env` and add your credentials
   - Set `BOT_TOKEN` and `MONGODB_URI`
   - Optional: Set `GROK_API_KEY` for AI features (get from https://console.groq.com)

3. **Import notes from MongoDB:**
   ```bash
   python import_notes.py
   # Choose option 6 (MongoDB import)
   ```

4. **Test AI integration (optional):**
   ```bash
   python test_ai.py
   ```

5. **Run the bot:**
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
   - `GROK_API_KEY` - Optional: Groq API key for AI features
5. **Deploy** - The `render.yaml` file handles the webhook setup automatically!

### Option 2: Polling Deployment (Development/Testing)
For development or testing, use polling mode:

### Manual Setup
- **Service Type**: Web Service
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python start.py`
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

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Required
BOT_TOKEN=your_telegram_bot_token
MONGODB_URI=your_mongodb_connection_string

# Optional - for AI features (Groq)
GROK_API_KEY=your_groq_api_key

# For webhook deployment (Render)
RENDER_EXTERNAL_HOSTNAME=your-app.render.com
PORT=8080

# For admin features
ADMIN_USER_ID=your_telegram_user_id
```

### Getting API Keys

- **BOT_TOKEN**: Create a bot via [@BotFather](https://t.me/botfather) on Telegram
- **MONGODB_URI**: Get from [MongoDB Atlas](https://cloud.mongodb.com) (free tier available)
- **GROK_API_KEY**: Get from [Groq Console](https://console.groq.com) (optional, for AI features)

## Tips

- Search is case-insensitive
- Partial matches work great (e.g., "math" finds all math subjects)
- Branch links keep users on your website for page views
- Sync automatically handles new notes without downtime
- Bot responds to greetings in multiple languages
- Semester queries provide direct access to branch pages
- AI features enhance user experience but bot works without them

## Future Enhancements
- Webhook-based auto-sync
- User feedback collection
- Download statistics tracking
- Admin panel for note management
- Multi-language support expansion