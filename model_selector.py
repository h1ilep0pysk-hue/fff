
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from config import user_models

async def model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    saved_chat_id = context.bot_data.get('chat_id_bot', 0)

    currentmodel = "kwaipilot" if chat_id == saved_chat_id else user_models.get(user_id, "gpt-4")
    keyboard = [
        [
            InlineKeyboardButton("🤖 GPT-3.5", callback_data="model_gpt3"),
            InlineKeyboardButton("🚀 GPT-4", callback_data="model_gpt4")
        ],
        [
            InlineKeyboardButton("🧠 Claude 3", callback_data="model_claude"),
            InlineKeyboardButton("⭐ Kwaipilot", callback_data="model_kwai")
        ],
        [
            InlineKeyboardButton("📊 Текущая", callback_data="show_current"),
            InlineKeyboardButton("⚙️ Настройки", callback_data="settings")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🔧 *Управление моделями ИИ*\n\n"
        f"Ваш Chat ID: `{chat_id}`\n"
        f"Текущая модель: `{currentmodel}`",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def model_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на кнопки выбора модели"""
    query = update.callback_query
    if query is None:
        print("Ошибка: query is None")
        return
    
    await query.answer()
    
    user_id = query.from_user.id
    callback_data = query.data
    if callback_data == "model_gpt3":
        user_models[user_id] = "gpt-3.5-turbo"
        model_name = "GPT-3.5 Turbo"
    elif callback_data == "model_gpt4":
        user_models[user_id] = "gpt-4"
        model_name = "GPT-4"
    elif callback_data == "model_claude":
        user_models[user_id] = "claude-3"
        model_name = "Claude 3"
    elif callback_data == "model_kwai":
        user_models[user_id] = "kwaipilot"
        model_name = "Kwaipilot"
    elif callback_data == "show_current":
        current_model = user_models.get(user_id, "gpt-4")
        await query.edit_message_text(
            text=f"📋 *Ваша текущая модель:*\n`{current_model}`",
            parse_mode='Markdown'
        )
        return
    keyboard = [
        [InlineKeyboardButton("✅ Использовать", callback_data="use_model")],
        [InlineKeyboardButton("🔄 Выбрать другую", callback_data="choose_another")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=f"✅ *Модель изменена!*\n\n"
             f"Новая модель: `{user_models[user_id]}`\n"
             f"Название: {model_name}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def use_model_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопки использования модели"""
    query = update.callback_query
    await query.answer("Модель активирована! Теперь отправьте сообщение.")
    
    await query.edit_message_text(
        text="✅ *Модель активирована!*\n\nОтправьте мне сообщение для обработки.",
        parse_mode='Markdown'
    )

async def choose_another_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат к выбору модели"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    current_model = user_models.get(user_id, "gpt-4")
    
    keyboard = [
        [
            InlineKeyboardButton("🤖 GPT-3.5", callback_data="model_gpt3"),
            InlineKeyboardButton("🚀 GPT-4", callback_data="model_gpt4")
        ],
    ]
    [InlineKeyboardButton(f"Текущая: {current_model}", callback_data="show_current")]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🔄 *Выберите модель:*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Настройки"""
    query = update.callback_query
    await query.answer("Настройки")
    
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_model")],
        [InlineKeyboardButton("🗑️ Сбросить", callback_data="reset_model")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="⚙️ *Настройки модели*\n\n"
             "Здесь можно настроить параметры модели.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def back_to_model_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат к меню выбора модели"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    current_model = user_models.get(user_id, "gpt-4")
    
    keyboard = [
        [
            InlineKeyboardButton("🤖 GPT-3.5", callback_data="model_gpt3"),
            InlineKeyboardButton("🚀 GPT-4", callback_data="model_gpt4")
        ],
        [InlineKeyboardButton(f"Текущая: {current_model}", callback_data="show_current")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🔧 *Выбор модели ИИ*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )