from telegram import Update
from telegram.ext import ContextTypes

async def return_bot(update: Update,context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("возращаю нейросеть")
    msg_id = msg.message_id
    context.bot_data['0'] = msg.chat_id
    return msg.chat_id

async def change_bot(update: Update,context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("меняю нейросеть")
    msg_id = msg.message_id
    context.bot_data['chat_id_bot'] = msg.chat_id
    return msg.chat_id