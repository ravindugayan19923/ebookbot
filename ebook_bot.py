import logging
import json
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)

# Load eBook data from JSON file
def load_ebook_links():
    with open('ebooks.json', 'r') as file:
        return json.load(file)

# Dictionary to store ISBN numbers and download links
ebook_links = load_ebook_links()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send me the Name or the ISBN number of the E-book you want to download.')

# Define the search function
async def search_ebook(update: Update, context: CallbackContext) -> None:
    query = update.message.text.strip()
    download_link = None

    # Check if the query is an ISBN number
    if query in ebook_links:
        download_link = ebook_links[query]
    else:
        # Search by name (case insensitive)
        for key, value in ebook_links.items():
            if query.lower() in key.lower():
                download_link = value
                break

    if download_link:
        await update.message.reply_text(f'Here is your E-book: {download_link}')
    else:
        await update.message.reply_text('Sorry, I could not find the E-book.')

def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your actual token
    application = Application.builder().token("6859509530:AAHNoMh5kdOIJoODOBBl9L_LPtObLnL3HhI").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_ebook))

    application.run_polling()

if __name__ == '__main__':
    main()

