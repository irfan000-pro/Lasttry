# bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests, os

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
    payload = {"contents": [{"parts": [{"text": user_message}]}]}

    try:
        response = requests.post(gemini_url, headers=headers, json=payload)
        result = response.json()
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        reply = f"⚠️ Gemini Error: {str(e)}"

    await update.message.reply_text(reply)

# Run the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()