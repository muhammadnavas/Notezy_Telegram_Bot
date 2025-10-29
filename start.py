#!/usr/bin/env python3
"""
Notezy Telegram Bot - Deployment Script
Supports both polling (development) and webhook (production) modes
"""

import os
import runpy
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Choose deployment mode based on environment.

    - If WEBHOOK_URL is set -> run webhook bot with proper async handling
    - Otherwise -> run polling bot by executing bot.py as __main__
    """
    webhook_url = os.getenv("WEBHOOK_URL")

    if webhook_url:
        print("🚀 Starting bot in WEBHOOK mode (Production)")
        # For webhook deployment, we need to handle the async event loop properly
        # Import here to ensure env vars are loaded
        import webhook_bot

        # Check if there's already an event loop running
        try:
            loop = asyncio.get_running_loop()
            print("⚠️ Event loop already running, creating task...")
            # If loop is already running, create a task
            loop.create_task(webhook_bot.main())
        except RuntimeError:
            # No event loop running, use asyncio.run()
            print("✅ Starting fresh event loop...")
            asyncio.run(webhook_bot.main())
    else:
        print("🧪 Starting bot in POLLING mode (Development)")
        # Execute bot.py as a script (runs its __main__ block)
        script_path = os.path.join(os.path.dirname(__file__), "bot.py")
        runpy.run_path(script_path, run_name="__main__")


if __name__ == "__main__":
    main()