#!/usr/bin/env python3
"""
Notezy Telegram Bot - Deployment Script
Supports both polling (development) and webhook (production) modes
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Choose deployment mode based on environment"""
    webhook_url = os.getenv("WEBHOOK_URL")

    if webhook_url:
        print("🚀 Starting bot in WEBHOOK mode (Production)")
        import webhook_bot
        webhook_bot.main()
    else:
        print("🧪 Starting bot in POLLING mode (Development)")
        import bot
        bot.main()

if __name__ == "__main__":
    main()