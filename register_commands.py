#!/usr/bin/env python3
"""
Test script to manually register bot commands
"""

import os
import asyncio
from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import ApplicationBuilder

# Load environment variables
load_dotenv()

async def register_commands():
    """Manually register bot commands"""
    
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found!")
        return
    
    print("🤖 Registering bot commands...")
    
    # Create bot application
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Define commands (including search)
    commands = [
        BotCommand("start", "Welcome message & semester links"),
        BotCommand("search", "Search for notes by subject code or name"),
        BotCommand("help", "Show help message"),
        BotCommand("semesters", "List all semesters with links"),
        BotCommand("branches", "List all VTU branches"), 
        BotCommand("about", "Info about Notezy Bot"),
        BotCommand("feedback", "Send feedback"),
    ]
    
    try:
        # Register commands
        await app.bot.set_my_commands(commands)
        print("✅ Commands registered successfully!")
        
        # Verify commands
        current_commands = await app.bot.get_my_commands()
        print(f"\n📋 Registered commands:")
        for cmd in current_commands:
            print(f"  /{cmd.command} - {cmd.description}")
            
    except Exception as e:
        print(f"❌ Failed to register commands: {e}")
    
    finally:
        # Clean up
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(register_commands())