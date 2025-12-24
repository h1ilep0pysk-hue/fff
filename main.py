from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import Token
from handlers.basic_commands import start, info
from handlers.ai_commands import idea, title, hashtag, image
from handlers.chat_handler import chat
from handlers.ai_switch import return_bot, change_bot
from handlers.model_selector import (
    model, model_callback, use_model_callback, 
    choose_another_callback, settings_callback, 
    back_to_model_callback
)

def main():
    app = ApplicationBuilder().token(Token).build()
    app.add_handler(CommandHandler('start', start)) 
    app.add_handler(CommandHandler('help', info))
    app.add_handler(CommandHandler('idea', idea))
    app.add_handler(CommandHandler('title', title))
    app.add_handler(CommandHandler('hashtag', hashtag))
    app.add_handler(CommandHandler('image', image))
    app.add_handler(CommandHandler('change_ai', change_bot))
    app.add_handler(CommandHandler('return_ai', return_bot)) 
    app.add_handler(CommandHandler('model', model))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.add_handler(CallbackQueryHandler(model_callback, pattern="^model_"))
    app.add_handler(CallbackQueryHandler(use_model_callback, pattern="^use_model$"))
    app.add_handler(CallbackQueryHandler(choose_another_callback, pattern="^choose_another$"))
    app.add_handler(CallbackQueryHandler(settings_callback, pattern="^settings$"))
    app.add_handler(CallbackQueryHandler(back_to_model_callback, pattern="^back_to_model$"))
    app.add_handler(CallbackQueryHandler(model_callback, pattern="^show_current$"))
    app.add_handler(CallbackQueryHandler(model_callback, pattern="^reset_model$"))
    
    app.run_polling()

if __name__ == "__main__":
    main()