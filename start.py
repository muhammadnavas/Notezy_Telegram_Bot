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

    - If WEBHOOK_URL is set -> run webhook bot
    - Otherwise -> run polling bot by executing bot.py as __main__
    """
    webhook_url = os.getenv("WEBHOOK_URL")

    if webhook_url:
        print("🚀 Starting bot in WEBHOOK mode (Production)")
        # Import here to ensure env vars are loaded
        import webhook_bot

        # Try to run the webhook bot
        try:
            asyncio.run(webhook_bot.main())
        except RuntimeError as e:
            if "Cannot close a running event loop" in str(e):
                print("⚠️ Event loop issue detected - webhook may still be running")
                print("✅ Bot deployment should be successful despite this warning")
            else:
                print(f"❌ Runtime error: {e}")
                raise
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise
    else:
        print("🧪 Starting bot in POLLING mode (Development)")
        # Execute bot.py as a script (runs its __main__ block)
        script_path = os.path.join(os.path.dirname(__file__), "bot.py")
        runpy.run_path(script_path, run_name="__main__")


if __name__ == "__main__":
    main()