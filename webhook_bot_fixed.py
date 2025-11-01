#!/usr/bin/env python3
"""
Fixed Webhook Bot for Render Deployment
Resolves asyncio event loop issues
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.error import Conflict
import os
from dotenv import load_dotenv
from aiohttp import web
import re

# Load environment variables
load_dotenv()

# Global variables
db = None
application = None

# AI integration
try:
    from openai import OpenAI
    grok_available = True
    print("✅ OpenAI library loaded successfully")
except ImportError:
    grok_available = False
    OpenAI = None
    print("⚠️ OpenAI library not available. Advanced AI features will be disabled.")

# Import all the handler functions from webhook_bot
# (We'll use them as they are already implemented correctly)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message with main menu buttons"""
    welcome_text = (
        "👋 Hello! I am Notezy Bot ☘️\n\n"
        "Your quick and chat-responsive study companion!\n"
        "Choose an option below to get started:"
    )

    keyboard = [
        [InlineKeyboardButton("📚 Semesters", callback_data="semesters")],
        [InlineKeyboardButton("🏫 Branches", callback_data="branches")],
        [InlineKeyboardButton("🔍 Search Notes", callback_data="search")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📝 Feedback", callback_data="feedback")],
        [InlineKeyboardButton("🆘 Help", callback_data="help")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def simple_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple message handler for basic functionality"""
    if not db:
        await update.message.reply_text(
            "🤖 Notezy Bot is starting up... Please try again in a moment!"
        )
        return
    
    # Basic search functionality
    query = update.message.text.strip()
    
    # Simple greeting check
    if query.lower() in ['hi', 'hello', 'hey', 'start']:
        await update.message.reply_text(
            f"👋 Hello {update.effective_user.first_name or 'there'}!\n\n"
            "I'm your Notezy assistant for VTU engineering notes!\n\n"
            "💡 Try searching for subjects like 'Data Structures' or '18CS51'\n"
            "🔍 What notes are you looking for today?"
        )
        return
    
    # Basic search
    try:
        search_result = db.search_notes(query, limit=10)
        
        if search_result["type"] == "exact" and search_result["results"]:
            results = search_result["results"]
            branch_groups = {}
            
            for note in results:
                url = note['branch_url']
                if url not in branch_groups:
                    branch_groups[url] = {
                        'subjects': [],
                        'semester': note['semester'],
                        'branch': note['branch']
                    }
                branch_groups[url]['subjects'].append(note['full_name'])
            
            formatted_results = []
            for branch_url, data in list(branch_groups.items())[:3]:  # Max 3 results
                full_url = f"https://www.notezy.online{branch_url}"
                subjects_text = ", ".join(data['subjects'][:3])  # Max 3 subjects
                if len(data['subjects']) > 3:
                    subjects_text += f" +{len(data['subjects']) - 3} more"
                
                formatted_results.append(
                    f"🎯 *Found: {query}*\n"
                    f"🏫 *{data['semester']} - {data['branch']}*\n"
                    f"📚 Subjects: {subjects_text}\n"
                    f"🔗 [View Notes]({full_url})"
                )
            
            response_text = "\n\n".join(formatted_results)
            await update.message.reply_text(
                response_text,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        else:
            await update.message.reply_text(
                f"❌ *{query}* not found in our database.\n\n"
                f"💡 Try searching for subject codes (e.g., 18CS51) or names (e.g., Data Structures)\n"
                f"🔍 Or use /help for more options!",
                parse_mode='Markdown'
            )
    except Exception as e:
        print(f"Search error: {e}")
        await update.message.reply_text(
            "⚠️ Search temporarily unavailable. Please try again later."
        )

async def simple_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple help command"""
    help_text = (
        "🆘 *Notezy Bot Help*\n\n"
        "🔍 *How to search:*\n"
        "• Type subject codes: `18CS51`\n"
        "• Type subject names: `Data Structures`\n"
        "• Type semester queries: `4th sem`\n\n"
        "📚 *Quick Links:*\n"
        "• 1st Sem: https://www.notezy.online/Chemistrycycle\n"
        "• 2nd Sem: https://www.notezy.online/Physicscycle\n"
        "• 3rd Sem: https://www.notezy.online/Sem3\n"
        "• 4th Sem: https://www.notezy.online/Sem4\n"
        "• 5th Sem: https://www.notezy.online/Sem5\n"
        "• 6th Sem: https://www.notezy.online/Sem6\n\n"
        "🌐 Website: https://www.notezy.online\n"
        "💬 Support: notezyhelp@gmail.com"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def webhook_handler(request):
    """Handle incoming webhook updates from Telegram"""
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return web.Response(text="OK")
    except Exception as e:
        print(f"Webhook error: {e}")
        return web.Response(text="ERROR", status=500)

async def health_check(request):
    """Health check endpoint"""
    return web.Response(text="OK - Notezy Bot Running")

def main():
    """Main function for fixed webhook bot"""
    global db, application
    
    print("🚀 Starting FIXED webhook bot...")
    
    # Initialize database
    print("📊 Initializing database...")
    try:
        from database import NotesDatabase
        db = NotesDatabase()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
        db = None
    
    # Get environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    PORT = int(os.getenv("PORT", 8080))
    RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    
    if not BOT_TOKEN:
        raise Exception("❌ BOT_TOKEN missing from environment!")
    if not RENDER_EXTERNAL_HOSTNAME:
        raise Exception("❌ RENDER_EXTERNAL_HOSTNAME missing from environment!")
    
    WEBHOOK_URL = f"https://{RENDER_EXTERNAL_HOSTNAME}"
    
    print(f"🔧 Configuration:")
    print(f"  - BOT_TOKEN: ***{BOT_TOKEN[-10:]}")
    print(f"  - PORT: {PORT}")
    print(f"  - WEBHOOK_URL: {WEBHOOK_URL}")
    
    # Create Telegram application
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", simple_help))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, simple_message_handler))
    
    print("✅ Bot configured with basic handlers")
    
    # Create web application
    app = web.Application()
    app.router.add_post('/webhook', webhook_handler)
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    # Simple startup function
    async def setup_webhook(app):
        try:
            await application.initialize()
            
            webhook_url = f"{WEBHOOK_URL}/webhook"
            await application.bot.set_webhook(webhook_url)
            print(f"✅ Webhook set to: {webhook_url}")
            
            # Set basic commands
            commands = [
                BotCommand("start", "Start the bot"),
                BotCommand("help", "Get help")
            ]
            await application.bot.set_my_commands(commands)
            print("✅ Bot commands set")
            
        except Exception as e:
            print(f"⚠️ Setup failed: {e}")
    
    app.on_startup.append(setup_webhook)
    
    print("🚀 Starting web server...")
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()