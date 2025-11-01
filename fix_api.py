#!/usr/bin/env python3
"""
Fix API endpoints in bot.py to use Groq instead of xAI
"""

import os

def fix_api_endpoints():
    files_to_fix = ['bot.py', 'webhook_bot.py', 'test_ai.py']
    
    for bot_file in files_to_fix:
        print(f"🔧 Fixing {bot_file}...")
    
    # Read the file
    with open(bot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count replacements
    xai_count = content.count('https://api.x.ai/v1')
    grok_count = content.count('grok-2-latest')
    
    # Count model replacements
    old_model_count = content.count('llama-3.1-70b-versatile')
    
    # Replace all instances
    content = content.replace('https://api.x.ai/v1', 'https://api.groq.com/openai/v1')
    content = content.replace('grok-2-latest', 'llama-3.1-8b-instant')
    content = content.replace('llama-3.1-70b-versatile', 'llama-3.1-8b-instant')
    
    # Write back
    with open(bot_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
        print(f'  ✅ Fixed {xai_count} API endpoints')
        print(f'  ✅ Fixed {grok_count} model names') 
        print(f'  ✅ Fixed {old_model_count} deprecated models')
        print(f'  ✅ {bot_file} updated')
    
    print('\n🎉 All files updated to use Groq API with supported model!')

if __name__ == "__main__":
    fix_api_endpoints()