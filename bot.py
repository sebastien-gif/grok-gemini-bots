import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# === TOKENS (à mettre dans les variables d'environnement sur Render) ===
XAI_TOKEN = os.getenv("XAI_TOKEN")
GEMINI_TOKEN = os.getenv("GEMINI_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# === Configuration Gemini ===
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# === Personnalités des bots ===
SYSTEM_PROMPT_GROK = "Tu es Grok, construit par xAI. Tu es utile, direct, un peu sarcastique et toujours honnête."
SYSTEM_PROMPT_GEMINI = "Tu es Gemini, un assistant IA utile et précis de Google."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text
    from_user = message.from_user

    # Anti-boucle : ignorer les messages envoyés par les bots
    if from_user.is_bot:
        return

    bot_username = context.bot.username.lower()

    # Répondre seulement si on est mentionné ou si on répond à un message du bot
    if f"@{bot_username}" in text.lower() or (message.reply_to_message and message.reply_to_message.from_user.username.lower() == bot_username):
        
        if "xai" in bot_username:
            prompt = f"{SYSTEM_PROMPT_GROK}\n\nQuestion: {text}"
        else:
            prompt = f"{SYSTEM_PROMPT_GEMINI}\n\nQuestion: {text}"

        response = gemini_model.generate_content(prompt).text
        await message.reply_text(response)

async def main():
    # Bot XAI (style Grok)
    app_xai = Application.builder().token(XAI_TOKEN).build()
    app_xai.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Bot Gemini
    app_gemini = Application.builder().token(GEMINI_TOKEN).build()
    app_gemini.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Les deux bots sont lancés et prêts à discuter !")
    await asyncio.gather(
        app_xai.initialize(),
        app_gemini.initialize(),
        app_xai.start(),
        app_gemini.start()
    )

if __name__ == "__main__":
    asyncio.run(main())
