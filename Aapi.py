from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import re

BOT_TOKEN = "7654306077:AAHi4ttdqVSNq1VCbwGQ1a1-IVDLiQ_rLJY"

API_ENDPOINT = "https://mundo.bienvenido.top/api/activate"

def extract_api_key(text):
    # Sirf uppercase alphanumeric 20-char key extract karo
    match = re.search(r'\b[A-Z0-9]{20}\b', text)
    return match.group(0) if match else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /getkey <license> to get your API key.")

async def get_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide your license key.\nExample: /getkey YOUR_LICENSE_KEY")
        return

    license_key = context.args[0]
    try:
        response = requests.post(API_ENDPOINT, json={"key": license_key})
        data = response.text

        key = extract_api_key(data)
        if key:
            await update.message.reply_text(f"Your API key: `{key}`", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"Could not find a valid API key in response:\n{data}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("getkey", get_key))

app.run_polling()