import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai

TOKEN = os.getenv("GEMINI_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text
        prompt = f"Tu es Gemini, un assistant IA utile et précis.\n\n{text}"
        response = model.generate_content(prompt).text
        await update.message.reply_text(response)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("✅ Bot Gemini lancé !")
    app.run_polling()

if __name__ == "__main__":
    main()
