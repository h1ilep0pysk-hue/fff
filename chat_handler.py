import asyncio
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from telegram import Update
from telegram.ext import ContextTypes

from config import OPENROUTER_API_KEY, user_models

async def chat(update: Update,context: ContextTypes.DEFAULT_TYPE): 
        saved_chat_id = context.bot_data.get('chat_id_bot', 0)
        user_text = update.message.text
        print(user_text)
        client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        )
        msg = await update.message.reply_text("⏳обрабатываю сообщение...")
        msg_id = msg.message_id
        chat_id= msg.chat_id
        def get_competion():
            user_text = update.message.text
            completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",  
                "X-Title": "guest",
            },
            extra_body={},
            model="tngtech/deepseek-r1t2-chimera:free",
            messages=[
                {
                "role": "user",
                "content": f"{user_text}"
                }
            ]
            )
            return completion
        def get_competion1():
                client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
                )
                completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "<YOUR_SITE_URL>", 
                    "X-Title": "<YOUR_SITE_NAME>", 
                },
                extra_body={},
                model="kwaipilot/kat-coder-pro:free",
                messages=[
                    {
                    "role": "user",
                    "content":f" {user_text}"
                    }
                ]
                )
                
                print("kat")
                return completion
        
        dots = ["⏳", "⌛", "⏳", "⌛"]
        loading_task = None
        async def loading_animation():
            for i in range(120):
                await asyncio.sleep(0.5)
                await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=msg.message_id,
                        text=f"💡обрабатываю ответ {dots[i % len(dots)]}"
                    )
        loading_task = asyncio.create_task(loading_animation())
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            if chat_id == saved_chat_id:
                completion = await loop.run_in_executor(executor, get_competion1)
            else:
                completion = await loop.run_in_executor(executor, get_competion)
        if loading_task:
            loading_task.cancel()
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=msg.message_id,
            text="📝 Обрабатываю результат..."
        )
        
        text1= completion.choices[0].message.content
        symbols_to_remove = ['*', '-', '#']   
        translation_table = str.maketrans('', '', ''.join(symbols_to_remove))  
        cleaned_text = text1.translate(translation_table)
        if len(cleaned_text) > 4000:
            cleaned_text = cleaned_text[:4000] + "\n\n... (текст сокращен)"
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            text=cleaned_text,
            message_id=msg.id)