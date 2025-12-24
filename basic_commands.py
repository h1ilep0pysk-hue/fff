from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes):
    await update.message.reply_text(f"бот работающий на основе ии для помощи с креативными идеями")

async def info(update: Update, context: ContextTypes):
    await update.message.reply_text(f"/idea-/idea[тема] идея для поста\n/title[тема]-генерация цепляющих заголовку\n/hashtag[тема]-подбор популярных хештега")