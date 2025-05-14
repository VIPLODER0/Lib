import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("7917489800:AAGMsgg7pqeGvZekoL6w-0dWuvKJeba2kp0")
OPENAI_API_KEY = os.getenv("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")

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Namaste! Main ek AI-powered Telegram bot hoon. Mujhe koi bhi sawal pucho, haiku likhne ke liye kaho, ya koi script generate karne ke liye bol do, main ChatGPT ke through jawab dunga!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming text messages."""
    user_message = update.message.text
    chat_id = update.effective_chat.id

    try:
        # Call OpenAI API with gpt-4o-mini model and store=true
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system", "content": "You are a helpful assistant who can answer questions, write haikus, and generate scripts in any programming language."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response.choices[0].message['content']
        await context.bot.send_message(chat_id=chat_id, text=bot_response)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Kuch galat ho gaya. Kripya dobara try karein.")

def main():
    """Start the bot."""
    if not TELEGRAM_API_TOKEN or not OPENAI_API_KEY:
        print("Error: TELEGRAM_API_TOKEN or OPENAI_API_KEY not set in .env file")
        return

    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()