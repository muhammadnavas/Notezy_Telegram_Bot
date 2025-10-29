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

    - If WEBHOOK_URL is set -> run webhook bot directly (don't use asyncio.run)
    - Otherwise -> run polling bot by executing bot.py as __main__
    """
    webhook_url = os.getenv("WEBHOOK_URL")

    if webhook_url:
        print("🚀 Starting bot in WEBHOOK mode (Production)")
        # For webhook deployment, import and run directly
        # This avoids asyncio.run() which can cause event loop issues
        import webhook_bot

        # Create a new event loop and run the webhook
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(webhook_bot.main())
        except KeyboardInterrupt:
            print("🛑 Received interrupt signal")
        finally:
            try:
                loop.close()
            except:
                pass
    else:
        print("🧪 Starting bot in POLLING mode (Development)")
        # Execute bot.py as a script (runs its __main__ block)
        script_path = os.path.join(os.path.dirname(__file__), "bot.py")
        runpy.run_path(script_path, run_name="__main__")


if __name__ == "__main__":
    main()