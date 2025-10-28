from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from database import NotesDatabase
import re

# Load environment variables
load_dotenv()

# Initialize database
db = NotesDatabase()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Notezy Bot!\n"
        "Search notes by *subject name* or *code* (e.g., 18CS51 or Data Structures).",
        parse_mode='Markdown'
    )

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
            
            # Time-based greeting
            import datetime
            current_hour = datetime.datetime.now().hour
            
            if 5 <= current_hour < 12:
                time_greeting = "Good morning"
            elif 12 <= current_hour < 17:
                time_greeting = "Good afternoon"
            elif 17 <= current_hour < 22:
                time_greeting = "Good evening"
            else:
                time_greeting = "Hello"
            
            await update.message.reply_text(
                f"👋 {time_greeting}, {user_name}!\n\n"
                "I'm your Notezy assistant. I can help you find study notes!\n\n"
                "💡 *Try searching for:*\n"
                "• Subject codes (e.g., `18CS51`)\n"
                "• Subject names (e.g., `Data Structures`)\n"
                "• Semester queries (e.g., `4th sem`, `for 3rd sem`)\n\n"
                "What notes are you looking for today?",
                parse_mode='Markdown'
            )
            return
    
    # If not a greeting or semester query, let it fall through to search handler
    await search(update, context)

async def sync_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to sync notes from source database"""
    try:
        # Check if user is admin (you can add user ID check here)
        user_id = update.effective_user.id
        
        await update.message.reply_text("🔄 Starting sync process...")
        
        # Perform sync
        sync_result = db.sync_from_source()
        
        if sync_result["success"]:
            await update.message.reply_text(
                f"✅ Sync completed successfully!\n\n"
                f"📊 *Sync Summary:*\n"
                f"• New notes: {sync_result['new_notes']}\n"
                f"• Updated: {sync_result['updated_notes']}\n"
                f"• Skipped: {sync_result['skipped_notes']}\n"
                f"• Total in bot DB: {sync_result['total_notes']}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                f"❌ Sync failed: {sync_result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error during sync: {str(e)}")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    
    # Search in database
    search_result = db.search_notes(query, limit=15)
    
    if search_result["type"] == "exact":
        # Found exact matches
        results = search_result["results"]
        
        # Group results by branch URL to avoid duplicates
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
        
        # Format results
        formatted_results = []
        for branch_url, data in branch_groups.items():
            full_url = f"https://www.notezy.online{branch_url}"
            subjects_text = ", ".join(data['subjects'][:5])  # Show max 5 subjects
            if len(data['subjects']) > 5:
                subjects_text += f" +{len(data['subjects']) - 5} more"
            
            formatted_results.append(
                f"🎯 *Found: {query}*\n"
                f"🏫 *{data['semester']} - {data['branch']}*\n"
                f"� Subjects: {subjects_text}\n"
                f"�🔗 [View Notes]({full_url})"
            )
        
        response_text = "\n\n".join(formatted_results[:3])  # Max 3 branch links
        
        await update.message.reply_text(
            response_text,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    
    elif search_result["type"] == "partial":
        # Found partial matches with scoring
        results = search_result["results"]
        
        # Format response for partial matches
        response_parts = [
            f"🔍 *Partial matches for '{query}':*\n"
        ]
        
        for branch_data in results[:3]:  # Max 3 branches
            full_url = f"https://www.notezy.online{branch_data['branch_url']}"
            subjects_text = ", ".join([subj['full_name'] for subj in branch_data['subjects'][:3]])
            if branch_data['total_subjects'] > 3:
                subjects_text += f" +{branch_data['total_subjects'] - 3} more"
            
            response_parts.append(
                f"🏫 *{branch_data['semester']} - {branch_data['branch']}*\n"
                f"📚 Found: {subjects_text}\n"
                f"🔗 [View Notes]({full_url})"
            )
        
        response_text = "\n\n".join(response_parts)
        
        await update.message.reply_text(
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
        
        await update.message.reply_text(
            response_text,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    
    else:
        # No matches at all
        total_notes = db.count_notes()
        await update.message.reply_text(
            f"❌ *{query}* not found in our database.\n\n"
            f"💡 *Tip:* Search by subject code (e.g., 18CS51) or name (e.g., Data Structures)\n"
            f"📚 Total notes available: {total_notes}\n\n"
            f"🔍 Try searching for a different subject or semester!",
            parse_mode='Markdown'
        )

if __name__ == "__main__":
    # Get bot token from environment variable
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    if not BOT_TOKEN:
        print("❌ Error: BOT_TOKEN not found in .env file")
        exit(1)
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sync", sync_notes))  # Admin sync command
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greeting))  # Handle greetings and search
    
    print("🤖 Notezy Bot is running...")
    print("💡 Use /sync command to update notes from database")
    app.run_polling()
