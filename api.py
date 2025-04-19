from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

BOT_TOKEN = "7654306077:AAFHFkpQX64nGXmApVXygoaE8TUljJ53yHA"  # <-- Yahan apna bot token daalo

API_ENDPOINT = "https://mundo.bienvenido.top/api/activate"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /getkey <license> to get your API key.")

async def get_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide your license key.\nExample: /getkey YOUR_LICENSE_KEY")
        return

    license_key = context.args[0]
    try:
        response = requests.post(API_ENDPOINT, json={"key": license_key})
        data = response.json()

        if "api_key" in data:
            await update.message.reply_text(f"Your API key: `{data['api_key']}`", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"Failed to get API key: {data}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("getkey", get_key))

app.run_polling()
