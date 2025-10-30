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

    - If RENDER_EXTERNAL_HOSTNAME is set -> run webhook bot (aiohttp server)
    - Otherwise -> run polling bot by executing bot.py as __main__
    """
    render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")

    if render_hostname:
        print("🚀 Starting bot in WEBHOOK mode (Production)")
        # For webhook deployment with aiohttp, import and run directly
        # web.run_app() handles the event loop internally
        import webhook_bot
        asyncio.run(webhook_bot.main())
    else:
        print("🧪 Starting bot in POLLING mode (Development)")
        # Execute bot.py as a script (runs its __main__ block)
        script_path = os.path.join(os.path.dirname(__file__), "bot.py")
        runpy.run_path(script_path, run_name="__main__")


if __name__ == "__main__":
    main()