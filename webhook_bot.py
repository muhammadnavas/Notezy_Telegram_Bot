from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.error import Conflict
import os
from dotenv import load_dotenv
from aiohttp import web
import re
from database import NotesDatabase

# Load environment variables
load_dotenv()

# Database will be initialized in main() to avoid import-time connections
db = None

# Sync functionality removed - bot now focused on search and help only

# AI features removed - keeping bot lightweight and focused

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message with main menu buttons"""
    welcome_text = (
        "👋 Hello! I am Notezy Bot ☘️\n\n"
        "Your quick and chat-responsive study companion!\n"
        "Choose an option below to get started:"
    )

    # Create main menu buttons
    keyboard = [
        [InlineKeyboardButton("📚 Semesters", callback_data="semesters")],
        [InlineKeyboardButton("🏫 Branches", callback_data="branches")],
        [InlineKeyboardButton("🔍 Search Notes", callback_data="search")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📝 Feedback", callback_data="feedback")],
        [InlineKeyboardButton("🆘 Help", callback_data="help")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboard buttons"""
    query = update.callback_query
    await query.answer()

    callback_data = query.data

    if callback_data == "semesters":
        # Show semester selection
        text = "📚 Choose your semester to view notes:"
        
        semesters = {
            "1st Semester": "https://www.notezy.online/Chemistrycycle",
            "2nd Semester": "https://www.notezy.online/Physicscycle", 
            "3rd Semester": "https://www.notezy.online/Sem3",
            "4th Semester": "https://www.notezy.online/Sem4",
            "5th Semester": "https://www.notezy.online/Sem5",
            "6th Semester": "https://www.notezy.online/Sem6"
        }
        
        keyboard = []
        for sem, link in semesters.items():
            keyboard.append([InlineKeyboardButton(sem, url=link)])
        
        # Add back button
        keyboard.append([InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif callback_data == "branches":
        # Show branches info
        text = (
            "🏫 Available Engineering Branches:\n\n"
            "• Computer Science & Engineering (CSE)\n"
            "• Information Science & Engineering (ISE)\n"
            "• Electronics & Communication (ECE)\n"
            "• AI & ML (AIML)\n"
            "• AI & DS (AIDS)\n\n"
            "📖 Notes are available for all branches across all semesters!"
        )
        
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif callback_data == "search":
        search_text = (
            "🔍 *Search for Notes*\n\n"
            "You can search by:\n"
            "• Subject codes (e.g., `18CS51`)\n"
            "• Subject names (e.g., `Data Structures`)\n"
            "• Semester queries (e.g., `4th sem`)\n\n"
            "Just type your search query below! 📝"
        )
        
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(search_text, reply_markup=reply_markup, parse_mode='Markdown')

    elif callback_data == "about":
        text = (
            "🤖 About Notezy Bot\n\n"
            "Notezy Bot is your study companion for VTU engineering students!\n\n"
            "✨ Features:\n"
            "• Instant search across all subjects\n"
            "• Access to comprehensive VTU notes\n"
            "• Organized by semester and branch\n"
            "• Quick and responsive chat interface\n\n"
            "📚 Supported:\n"
            "• All VTU engineering branches\n"
            "• 1st to 6th semester notes\n"
            "• Subject codes and names search\n\n"
            "🌐 Website: https://www.notezy.online\n"
            "💬 For support: notezyhelp@gmail.com"
        )
        
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif callback_data == "feedback":
        text = (
            "📝 We'd love to hear your feedback!\n\n"
            "Please share your thoughts, suggestions, or report any issues:\n\n"
            "💬 Send your feedback to: notezyhelp@gmail.com\n\n"
            "Your feedback helps us improve Notezy Bot for all students! 🙏"
        )
        
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif callback_data == "help":
        text = (
            "🆘 Help & Commands\n\n"
            "Available Commands:\n\n"
            "🚀 /start - Welcome message with menu\n"
            "📚 /semesters - View all semester options\n"
            "🏫 /branches - See available engineering branches\n"
            "🔍 /search <subject> - Search for notes by subject name or code\n"
            "ℹ️ /about - Learn more about Notezy Bot\n"
            "📝 /feedback - Share your feedback\n"
            "🆘 /help - Show this help message\n\n"
            "💡 Tips:\n"
            "• Search using subject codes (e.g., 18CS51)\n"
            "• Or use subject names (e.g., Data Structures)\n"
            "• Get instant access to VTU notes!\n\n"
            "🌐 Visit: https://www.notezy.online"
        )
        
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif callback_data == "main_menu":
        # Return to main menu
        welcome_text = (
            "👋 Hello! I am Notezy Bot ☘️\n\n"
            "Your quick and chat-responsive study companion!\n"
            "Choose an option below to get started:"
        )

        keyboard = [
            [InlineKeyboardButton("📚 Semesters", callback_data="semesters")],
            [InlineKeyboardButton("🏫 Branches", callback_data="branches")],
            [InlineKeyboardButton("🔍 Search Notes", callback_data="search")],
            [InlineKeyboardButton("ℹ️ About", callback_data="about")],
            [InlineKeyboardButton("📝 Feedback", callback_data="feedback")],
            [InlineKeyboardButton("🆘 Help", callback_data="help")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(welcome_text, reply_markup=reply_markup)

async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower().strip()

    # Define semester query patterns
    semester_patterns = [
        r'(?:for\s+)?(\d+)(?:st|nd|rd|th)?\s*sem(?:ester)?(?:\s+link)?',
        r'(?:for\s+)?sem(?:ester)?\s*(\d+)(?:\s+link)?',
        r'(?:for\s+)?(\w+)\s*cycle(?:\s+link)?'
    ]

    # Check if message matches any semester pattern
    for pattern in semester_patterns:
        match = re.search(pattern, message_text)
        if match:
            semester_num = match.group(1)

            # Map semester numbers/names to database semesters
            semester_mapping = {
                '1': 'Chemistrycycle', 'first': 'Chemistrycycle', '1st': 'Chemistrycycle',
                '2': 'Physicscycle', 'second': 'Physicscycle', '2nd': 'Physicscycle',
                '3': 'Sem3', 'third': 'Sem3', '3rd': 'Sem3',
                '4': 'Sem4', 'fourth': 'Sem4', '4th': 'Sem4',
                '5': 'Sem5', 'fifth': 'Sem5', '5th': 'Sem5',
                '6': 'Sem6', 'sixth': 'Sem6', '6th': 'Sem6',
                'chemistry': 'Chemistrycycle', 'physics': 'Physicscycle'
            }

            semester = semester_mapping.get(semester_num.lower())
            if semester:
                # Get all branches for this semester
                branches = db.collection.distinct("branch", {"semester": semester})

                if branches:
                    # Format semester name for display
                    display_names = {
                        'Chemistrycycle': '1st Semester (Chemistry Cycle)',
                        'Physicscycle': '2nd Semester (Physics Cycle)',
                        'Sem3': '3rd Semester',
                        'Sem4': '4th Semester',
                        'Sem5': '5th Semester',
                        'Sem6': '6th Semester'
                    }

                    semester_display = display_names.get(semester, semester)

                    # Create branch links
                    branch_links = []
                    branch_names = {
                        'computerscience': 'Computer Science',
                        'electronicsandcommunications': 'ECE',
                        'informationscience': 'Information Science',
                        'aiml': 'AI & ML',
                        'aids': 'AI & DS'
                    }

                    for branch in sorted(branches):
                        branch_url = f"https://www.notezy.online/{semester}/{branch}"
                        branch_display = branch_names.get(branch, branch.title())
                        branch_links.append(f"🔗 [{branch_display}]({branch_url})")

                    response_text = (
                        f"📚 *{semester_display} Notes*\n\n"
                        f"Choose your branch:\n" +
                        "\n".join(branch_links) +
                        f"\n\n💡 Or search for specific subjects like 'Data Structures' or '18CS51'"
                    )

                    await update.message.reply_text(
                        response_text,
                        parse_mode='Markdown',
                        disable_web_page_preview=True
                    )
                    return

    # Define greeting patterns
    greeting_patterns = [
        r'^(hi|hello|hey|hai|hii|helo)$',  # Basic greetings
        r'^(good\s*(morning|afternoon|evening|night|day))$',  # Good morning/afternoon etc.
        r'^(gm|gn|gd\s*mrng|gd\s*day|gd\s*evng|gd\s*night)$',  # Abbreviations
        r'^(namaste|namaskar|vanakkam|salaam|assalamualaikum)$',  # Cultural greetings
        r'^(howdy|sup|yo|wassup|what\'s\s*up)$',  # Casual greetings
        r'^(greetings|welcome|bonjour|hola|ciao|aloha)$'  # Other languages
    ]

    # Check if message matches any greeting pattern
    for pattern in greeting_patterns:
        if re.match(pattern, message_text):
            # Get user's first name if available
            user_name = update.effective_user.first_name or "there"

            # Simple greeting response
            await update.message.reply_text(
                f"👋 Hello {user_name}! I'm your Notezy assistant for VTU engineering notes! 📚\n\n"
                "💡 Try searching for subjects like 'Data Structures' or '18CS51'\n"
                "🔍 What notes are you looking for today?",
                parse_mode='Markdown'
            )

            return

    # If not a greeting or semester query, let it fall through to search handler
    await search(update, context)





async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get query from command args if available, otherwise from message text
    if context.args:
        # Called as /search query - use the args
        query = " ".join(context.args).strip()
    else:
        # Called as direct message - use full text but remove /search prefix if present
        query = update.message.text.strip()
        if query.lower().startswith('/search '):
            query = query[8:].strip()  # Remove '/search ' prefix

    if not query:
        await update.message.reply_text(
            "🔍 Please provide a search query!\n\n"
            "Examples:\n"
            "• `/search bcs301`\n"
            "• `/search data structures`\n"
            "• Just type: `mathematics`",
            parse_mode='Markdown'
        )
        return

    # Send searching message to user
    search_message = await update.message.reply_text(
        f"🔍 *Searching for '{query}'...*\n⏳ Please wait...",
        parse_mode='Markdown'
    )

    # Search in database
    search_result = db.search_notes(query, limit=100)

    if search_result["type"] == "exact":
        # Found exact matches
        results = search_result["results"]

        # Group results by subject to avoid duplicates, then organize by semester and branch
        subject_groups = {}
        for note in results:
            subject_key = note['full_name']  # Use subject name as key to deduplicate
            if subject_key not in subject_groups:
                subject_groups[subject_key] = {
                    'branches': [],
                    'semester': note['semester'],
                    'subject_code': note.get('subject_code', ''),
                    'subject_name': note.get('subject_name', '')
                }
            
            # Add branch info if not already present
            branch_info = {
                'branch': note['branch'],
                'branch_url': note['branch_url']
            }
            if branch_info not in subject_groups[subject_key]['branches']:
                subject_groups[subject_key]['branches'].append(branch_info)

        # Format exact match results - show all subjects found
        formatted_results = []
        total_subjects = len(subject_groups)
        
        for subject_name, data in subject_groups.items():
            # Create list of branches for this subject
            branch_names = [branch['branch'] for branch in data['branches']]
            branch_urls = [f"https://www.notezy.online{branch['branch_url']}" for branch in data['branches']]
            
            # Format branch list
            if len(branch_names) <= 3:
                branches_text = ", ".join(branch_names)
                # Use first branch URL for the link
                main_url = branch_urls[0]
            else:
                branches_text = ", ".join(branch_names[:3]) + f" +{len(branch_names)-3} more branches"
                main_url = branch_urls[0]

            formatted_results.append(
                f"📚 *{subject_name}*\n"
                f"📖 {data['semester']}\n" 
                f"🏫 Available in: {branches_text}\n"
                f"🔗 [View Notes]({main_url})"
            )

        response_text = f"🔍 *Found {total_subjects} subject(s) matching '{query}':*\n\n"
        response_text += "\n\n".join(formatted_results)

        await search_message.edit_text(
            response_text,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

    elif search_result["type"] == "partial":
        # Found partial matches with scoring
        results = search_result["results"]
        total_matches = search_result.get("total_matches", len(results))

        # Format response for partial matches - show more comprehensive results
        response_parts = [
            f"🔍 *Found {total_matches} matches for '{query}':*\n"
        ]

        # Show more branches (up to 8 instead of 5)
        for i, branch_data in enumerate(results[:8]):
            full_url = f"https://www.notezy.online{branch_data['branch_url']}"
            
            # Show more subjects per branch (up to 8 instead of 5)
            subjects_list = [subj['full_name'] for subj in branch_data['subjects'][:8]]
            subjects_text = ", ".join(subjects_list)
            
            remaining = branch_data['total_subjects'] - len(subjects_list)
            if remaining > 0:
                subjects_text += f" +{remaining} more"

            response_parts.append(
                f"🏫 *{branch_data['semester']} - {branch_data['branch']}*\n"
                f"📚 Subjects: {subjects_text}\n"
                f"🔗 [View Notes]({full_url})"
            )

        response_text = "\n\n".join(response_parts)
        
        # Add summary if there are more results
        if len(results) > 8:
            response_text += f"\n\n📊 *Showing top 8 of {len(results)} matching branches*"
        
        # Add search tips for better results
        if total_matches > 20:
            response_text += f"\n\n💡 *Tip: Try more specific terms like subject codes (e.g., BCS301) for exact matches*"

        await search_message.edit_text(
            response_text,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

    elif search_result["type"] == "related":
        # No exact match, but found related subjects in same semester/branch
        results = search_result["results"]
        semester = search_result["searched_semester"]
        branch = search_result["searched_branch"]

        # Group by branch URL
        branch_groups = {}
        for note in results:
            url = note['branch_url']
            if url not in branch_groups:
                branch_groups[url] = {
                    'subjects': [],
                    'semester': note['semester'],
                    'branch': note['branch']
                }
            branch_groups[url]['subjects'].append(note['full_name'])

        # Format response
        response_parts = [
            f"❌ *{query}* not found in our database.\n",
            f"📖 *Other notes in {semester} - {branch}:*\n"
        ]

        for branch_url, data in list(branch_groups.items())[:2]:  # Max 2 branches
            full_url = f"https://www.notezy.online{branch_url}"
            subjects_text = ", ".join(data['subjects'][:8])  # Show max 8 subjects
            if len(data['subjects']) > 8:
                subjects_text += f" +{len(data['subjects']) - 8} more"

            response_parts.append(
                f"🏫 *{data['semester']} - {data['branch']}*\n"
                f"📚 Available: {subjects_text}\n"
                f"🔗 [Browse All Notes]({full_url})"
            )

        response_text = "\n\n".join(response_parts)

        await search_message.edit_text(
            response_text,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )

    else:
        # No matches at all
        total_notes = db.count_notes()

        response_text = (
            f"❌ *{query}* not found in our database.\n\n"
            f"💡 *Tip:* Search by subject code (e.g., 18CS51) or name (e.g., Data Structures)\n"
            f"📚 Total notes available: {total_notes}\n\n"
            f"🔍 Try searching for a different subject or semester!"
        )

        await search_message.edit_text(
            response_text,
            parse_mode='Markdown'
        )

async def semesters_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all available semesters with links"""
    semesters = {
        "1st Semester (Chemistry Cycle)": "https://www.notezy.online/Chemistrycycle",
        "2nd Semester (Physics Cycle)": "https://www.notezy.online/Physicscycle", 
        "3rd Semester": "https://www.notezy.online/Sem3",
        "4th Semester": "https://www.notezy.online/Sem4",
        "5th Semester": "https://www.notezy.online/Sem5",
        "6th Semester": "https://www.notezy.online/Sem6"
    }

    keyboard = []
    for sem, link in semesters.items():
        keyboard.append([InlineKeyboardButton(sem, url=link)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "📚 *Available Semesters*\n\n"
        "Click on your semester to view notes:"
    )

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def branches_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all available VTU branches"""
    branches_info = {
        "Computer Science": "computerscience",
        "Information Science": "informationscience", 
        "Electronics & Communication": "electronicsandcommunications",
        "AI & Machine Learning": "aiml",
        "AI & Data Science": "aids"
    }

    text = "🏫 *VTU Branches Available:*\n\n"
    for display_name, branch_code in branches_info.items():
        text += f"• {display_name}\n"
    
    text += f"\n💡 Use semester commands or search for specific subjects!"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display information about the bot"""
    user_name = update.effective_user.first_name or "there"

    base_about = (
        "🤖 *About Notezy Bot*\n\n"
        "Notezy Bot is your study companion for VTU engineering students!\n\n"
        "✨ Features:\n"
        "• Instant search across all subjects\n"
        "• Access to comprehensive VTU notes\n"
        "• Organized by semester and branch\n"
        "• Quick and responsive chat interface\n"
        "\n\n"
        "📚 Supported:\n"
        "• All VTU engineering branches\n"
        "• 1st to 6th semester notes\n"
        "• Subject codes and names search\n\n"
        "🌐 Website: https://www.notezy.online\n"
        "� For support: notezyhelp@gmail.com"
    )

    await update.message.reply_text(base_about, parse_mode='Markdown')

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle feedback requests"""
    feedback_message = (
        "📝 *Send Feedback*\n\n"
        "We'd love to hear from you! 💬\n\n"
        "📧 *Contact us:*\n"
        "• Email: notezyhelp@gmail.com\n"
        "• Website: https://www.notezy.online\n\n"
        "Tell us:\n"
        "• How we can improve the bot\n"
        "• Missing subjects or notes\n"
        "• Any issues you encountered\n"
        "• Suggestions for new features\n\n"
        "Your feedback helps us make Notezy better! 🙏"
    )

    await update.message.reply_text(feedback_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display help information and available commands"""
    help_message = (
        "🆘 *Help - Available Commands*\n\n"
        "🤖 *Basic Commands:*\n"
        "/start - Welcome message & semester links\n"
        "/help - Show this help message\n\n"
        "📚 *Note Commands:*\n"
        "/semesters - List all semesters with links\n"
        "/branches - List all VTU branches\n"
        "/search <subject> - Search for notes\n\n"
        "ℹ️ *Info Commands:*\n"
        "/about - Info about Notezy Bot\n"
        "/feedback - Send feedback\n\n"
        " *Quick search examples:*\n"
        "• /search 18CS51\n"
        "• /search Data Structures\n"
        "• Just type: 4th sem\n\n"
        "🌐 Visit: https://www.notezy.online"
    )

    await update.message.reply_text(help_message, parse_mode='Markdown')

async def webhook_handler(request):
    """Handle incoming webhook updates from Telegram"""
    global processed_updates
    
    try:
        print("📨 Received webhook request")
        data = await request.json()
        print(f"📦 Update data keys: {list(data.keys()) if isinstance(data, dict) else 'not dict'}")
        update = Update.de_json(data, application.bot)
        
        # Check for duplicate updates to prevent recursive processing
        update_id = update.update_id
        if update_id in processed_updates:
            print(f"⚠️ Duplicate update {update_id} detected - skipping")
            return web.Response(text="DUPLICATE", status=200)
        
        # Add to processed updates (keep only last 100 to prevent memory issues)
        processed_updates.add(update_id)
        if len(processed_updates) > 100:
            # Remove oldest entries
            processed_updates = set(list(processed_updates)[-50:])
        
        print(f"🔄 Processing update {update_id}...")
        
        # Make sure application is initialized
        if not hasattr(application, '_initialized') or not application._initialized:
            print("⚠️ Application not initialized, skipping update...")
            return web.Response(text="INITIALIZING", status=503)
        
        await application.process_update(update)
        print(f"✅ Update {update_id} processed successfully")
        return web.Response(text="OK")
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        import traceback
        traceback.print_exc()
        return web.Response(text="ERROR", status=500)

async def health_check(request):
    """Health check endpoint for Render"""
    status = "OK"
    if hasattr(application, '_initialized') and application._initialized:
        status += " - Bot Ready"
    else:
        status += " - Bot Initializing"
    return web.Response(text=status)

async def on_startup(app):
    """Set up webhook on startup"""
    try:
        print("🔄 Initializing Telegram application...")
        
        # Initialize the application
        await application.initialize()
        print("✅ Telegram application initialized")
        
        # Set up bot commands in a simple way
        print("📝 Setting up bot commands...")
        commands = [
            BotCommand("start", "Welcome message & semester links"),
            BotCommand("help", "Show help message"),
            BotCommand("semesters", "List all semesters with links"),
            BotCommand("branches", "List all VTU branches"),
            BotCommand("about", "Info about Notezy Bot"),
            BotCommand("feedback", "Send feedback"),
            # BotCommand("sync", "Sync notes from database (Admin only)"),  # REMOVED
        ]
        
        try:
            await application.bot.set_my_commands(commands)
            print("✅ Bot commands registered successfully")
        except Exception as e:
            print(f"⚠️ Failed to register commands: {e}")
        
        # Set webhook
        webhook_url = f"{WEBHOOK_URL}/webhook"
        print(f"🔗 Setting webhook to: {webhook_url}")
        await application.bot.set_webhook(webhook_url)
        print(f"✅ Webhook set successfully to {webhook_url}")
        
        print("🎉 Startup completed successfully!")
        
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        import traceback
        traceback.print_exc()
        print("⚠️ Bot may not work correctly, but server will continue running...")

def main():
    """Main function for webhook bot"""
    global db, application, BOT_TOKEN, WEBHOOK_URL

    print("🚀 Starting webhook bot initialization...")

    # Initialize database here to avoid import-time connections
    print("📊 Initializing database...")
    try:
        db = NotesDatabase()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise

    # Get environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    PORT = int(os.getenv("PORT", 8080))
    RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

    print(f"🔧 Environment variables:")
    print(f"  - BOT_TOKEN: {'***' + BOT_TOKEN[-10:] if BOT_TOKEN else 'NOT SET'}")
    print(f"  - PORT: {PORT}")
    print(f"  - RENDER_EXTERNAL_HOSTNAME: {RENDER_EXTERNAL_HOSTNAME}")

    if not BOT_TOKEN:
        raise Exception("❌ BOT_TOKEN missing from environment!")

    if not RENDER_EXTERNAL_HOSTNAME:
        raise Exception("❌ RENDER_EXTERNAL_HOSTNAME missing from environment!")

    WEBHOOK_URL = f"https://{RENDER_EXTERNAL_HOSTNAME}"
    print(f"🌐 Webhook base URL: {WEBHOOK_URL}")

    # Create Telegram application
    print("🤖 Creating Telegram application...")
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    print("✅ Telegram application created")
    
    # Commands will be set up in the startup handler to avoid event loop conflicts

    # Add error handler for conflicts
    async def error_handler(update: Update, context):
        """Handle Telegram API errors"""
        if isinstance(context.error, Conflict):
            print("❌ Conflict error: Multiple bot instances detected")
            print("💡 Make sure only one bot instance is running")
        else:
            print(f"❌ Update error: {context.error}")

    application.add_error_handler(error_handler)

    # Add handlers
    print("📝 Adding command handlers...")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("semesters", semesters_command))
    application.add_handler(CommandHandler("branches", branches_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("feedback", feedback_command))
    # Sync functionality removed for stability
    application.add_handler(CallbackQueryHandler(handle_callback))  # Handle button callbacks
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greeting))  # Handle greetings and search
    print("✅ Handlers added (SYNC REMOVED)")

    # Create aiohttp web application
    print("🌐 Creating aiohttp web application...")
    app = web.Application()

    # Add routes
    app.router.add_post('/webhook', webhook_handler)
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    print("✅ Routes added")

    # Add startup handler
    app.on_startup.append(on_startup)
    print("✅ Startup handler added")

    print("🤖 Notezy Bot is starting with webhook...")
    print(f"🌐 Webhook URL: {WEBHOOK_URL}")
    print(f"🔌 Port: {PORT}")
    print("💡 Use /sync command to update notes from database")

    # Start the web server
    print("🚀 Starting web server...")
    web.run_app(app, host="0.0.0.0", port=PORT)
