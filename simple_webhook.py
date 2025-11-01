#!/usr/bin/env python3
"""
Simple webhook bot for production deployment
Fixes event loop issues on Render
"""

import os
import asyncio
from aiohttp import web
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
from database import NotesDatabase

# Import handlers from the main webhook bot
from webhook_bot import (
    start, handle_callback, greeting, sync_notes, semesters_command,
    branches_command, about_command, feedback_command, help_command,
    grok_available
)

# Load environment variables
load_dotenv()

# Global variables
db = None
application = None
BOT_TOKEN = None
WEBHOOK_URL = None

async def simple_webhook_handler(request):
    """Simple webhook handler with minimal initialization checks"""
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        
        # Process update without complex initialization checks
        await application.process_update(update)
        return web.Response(text="OK")
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return web.Response(text="ERROR", status=500)

async def simple_health_check(request):
    """Simple health check"""
    return web.Response(text="OK")

async def initialize_bot():
    """Initialize bot in a simple way"""
    global application, db, BOT_TOKEN, WEBHOOK_URL
    
    print("🚀 Initializing simple webhook bot...")
    
    # Get environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    
    if not BOT_TOKEN:
        raise Exception("BOT_TOKEN missing!")
    if not RENDER_EXTERNAL_HOSTNAME:
        raise Exception("RENDER_EXTERNAL_HOSTNAME missing!")
    
    WEBHOOK_URL = f"https://{RENDER_EXTERNAL_HOSTNAME}"
    
    # Initialize database
    try:
        db = NotesDatabase()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️ Database error: {e}")
        # Continue without database for basic functionality
    
    # Create application
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add handlers
    from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("semesters", semesters_command))
    application.add_handler(CommandHandler("branches", branches_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("feedback", feedback_command))
    application.add_handler(CommandHandler("sync", sync_notes))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greeting))
    
    print("✅ Handlers added")
    
    # Initialize application
    await application.initialize()
    print("✅ Application initialized")
    
    # Set webhook
    webhook_url = f"{WEBHOOK_URL}/webhook"
    await application.bot.set_webhook(webhook_url)
    print(f"✅ Webhook set to: {webhook_url}")
    
    return application

def create_app():
    """Create aiohttp application"""
    app = web.Application()
    
    # Add routes
    app.router.add_post('/webhook', simple_webhook_handler)
    app.router.add_get('/', simple_health_check)
    app.router.add_get('/health', simple_health_check)
    
    return app

async def startup_handler(app):
    """Startup handler that initializes the bot"""
    try:
        await initialize_bot()
        print("🎉 Startup completed!")
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        import traceback
        traceback.print_exc()
        # Don't raise to allow server to start

def main():
    """Main function"""
    print("🚀 Starting simple webhook bot...")
    
    # Create app
    app = create_app()
    app.on_startup.append(startup_handler)
    
    # Get port
    PORT = int(os.getenv("PORT", 8080))
    
    # Run app
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()