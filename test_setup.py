import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

# Check if BOT_TOKEN exists
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print('❌ BOT_TOKEN not found in .env file')
    exit(1)

# Test the setup_commands function
async def setup_commands():
    from telegram.ext import ApplicationBuilder
    from telegram import BotCommand

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    commands = [
        BotCommand('start', 'Welcome message & semester links'),
        BotCommand('help', 'Show help message'),
    ]

    try:
        await app.bot.set_my_commands(commands)
        print('✅ Bot commands registered successfully')
        current_commands = await app.bot.get_my_commands()
        print(f'📋 Current commands: {[cmd.command for cmd in current_commands]}')
        print('✅ Command setup test passed!')
        return True
    except Exception as e:
        print(f'❌ Command setup test failed: {e}')
        return False

# Run the test
result = asyncio.run(setup_commands())