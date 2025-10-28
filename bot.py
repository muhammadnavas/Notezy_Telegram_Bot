from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from database import NotesDatabase

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    
    print("🤖 Notezy Bot is running...")
    app.run_polling()
