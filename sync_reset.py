#!/usr/bin/env python3
"""
Sync call count reset - run this if sync gets stuck
"""

import asyncio
import os
import time

# Simple function to reset sync call count after 60 seconds of no activity
async def reset_sync_count():
    """Reset sync call count periodically to prevent permanent locks"""
    global sync_call_count, last_sync_time
    
    while True:
        await asyncio.sleep(60)  # Check every minute
        
        current_time = time.time()
        if current_time - last_sync_time > 120:  # No sync activity for 2 minutes
            if sync_call_count > 0:
                print(f"🔄 Auto-resetting sync call count from {sync_call_count} to 0")
                sync_call_count = 0

if __name__ == "__main__":
    print("This is a utility script - functionality is built into the bot")