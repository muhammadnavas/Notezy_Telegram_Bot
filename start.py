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

    - If WEBHOOK_URL is set -> run webhook bot (async) via asyncio.run
    - Otherwise -> run polling bot by executing bot.py as __main__
    """
    webhook_url = os.getenv("WEBHOOK_URL")

    if webhook_url:
        print("🚀 Starting bot in WEBHOOK mode (Production)")
        # import here so module imports happen after env is loaded
        import webhook_bot
        # webhook_bot.main is an async coroutine; run it properly
        asyncio.run(webhook_bot.main())
    else:
        print("🧪 Starting bot in POLLING mode (Development)")
        # Execute bot.py as a script (runs its __main__ block)
        script_path = os.path.join(os.path.dirname(__file__), "bot.py")
        runpy.run_path(script_path, run_name="__main__")


if __name__ == "__main__":
    main()