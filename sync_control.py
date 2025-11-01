#!/usr/bin/env python3
"""
Emergency sync control script
Use this to re-enable sync if it gets disabled due to automatic triggering
"""

import os
from dotenv import load_dotenv

load_dotenv()

def enable_sync():
    """Enable sync command by modifying both bot files"""
    bot_files = ['bot.py', 'webhook_bot.py']
    
    for file_path in bot_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Replace sync_disabled = True with sync_disabled = False
            modified_content = content.replace('sync_disabled = True', 'sync_disabled = False')
            
            with open(file_path, 'w') as f:
                f.write(modified_content)
            
            print(f"✅ Updated {file_path}")
    
    print("🔄 Sync has been re-enabled. Restart the bot for changes to take effect.")

if __name__ == "__main__":
    enable_sync()