from __future__ import annotations

from app.agent import AssistantAgent
from app.config import Settings


def run_telegram(agent: AssistantAgent, settings: Settings | None = None) -> None:
    settings = settings or Settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN first")

    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Neon Rubi Agent online ✨")

    async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = update.message.text or ""
        reply = agent.respond(text)
        await update.message.reply_text(reply)

    app = Application.builder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()


def run_discord(agent: AssistantAgent, settings: Settings | None = None) -> None:
    settings = settings or Settings()
    if not settings.discord_bot_token:
        raise RuntimeError("Set DISCORD_BOT_TOKEN first")

    import discord

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready() -> None:
        print(f"Logged in as {client.user}")

    @client.event
    async def on_message(message: discord.Message) -> None:
        if message.author == client.user:
            return
        if not message.content:
            return
        reply = agent.respond(message.content)
        await message.channel.send(reply)

    client.run(settings.discord_bot_token)
