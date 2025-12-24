import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from telegram import Update
from telegram.ext import ContextTypes

from config import OPENROUTER_API_KEY, user_models

async def idea(update: Update,context: ContextTypes.DEFAULT_TYPE):
    saved_chat_id = context.bot_data.get('chat_id_bot', 0)
    print(saved_chat_id)
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )
    usertext= "".join(context.args)
    print(usertext)
    if usertext == "":
        await update.message.reply_text("введите тему")
        return()
    else:
        msg = await update.message.reply_text("⏳ Генерирую идею...")
        msg_id = msg.message_id
        chat_id= msg.chat_id
        base=[usertext,msg_id,chat_id]
        with open("base.json", "w", encoding="utf-8") as file:
            json.dump(base, file, ensure_ascii=False, indent=4)
        print(chat_id)
        def get_competion():
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
                    "content":f"сделай идею для видео связанная с {usertext}?"
                    }
                ]
                )
                
                print("kat")
                return completion.choices[0].message.content
        def get_competion1():
                client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
                )
                completion1 = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "<YOUR_SITE_URL>",  
                    "X-Title": "guest",
                },
                extra_body={},
                model="tngtech/deepseek-r1t2-chimera:free",
                messages=[
                    {
                    "role": "user",
                    "content": f"сделай идею для видео связанная с {usertext}?"
                    }
                ]
                )
                print("deepseek")
                return completion1.choices[0].message.content
        dots = ["⏳", "⌛", "⏳", "⌛"]
        loading_task = None
        async def loading_animation():
            for i in range(120):
                await asyncio.sleep(0.5)
                await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=msg.message_id,
                        text=f"💡 Генерирую идеи {dots[i % len(dots)]}"
                    )
        loading_task = asyncio.create_task(loading_animation())
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            if chat_id == saved_chat_id:
                completion = await loop.run_in_executor(executor, get_competion)
                response = get_competion()
            else:
                completion = await loop.run_in_executor(executor, get_competion1)
                completion1= get_competion1()
        if loading_task:
            loading_task.cancel()
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=msg.message_id,
            text="📝 Обрабатываю результат..."
        )
        if chat_id == saved_chat_id:
            text1=response
        else:
            text1=completion1
        symbols_to_remove = ['*', '-', '#']   
        translation_table = str.maketrans('', '', ''.join(symbols_to_remove))  
        cleaned_text = text1.translate(translation_table)
        if len(cleaned_text) > 4000:
            cleaned_text = cleaned_text[:4000] + "\n\n... (текст сокращен)"
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            text=cleaned_text,
            message_id=msg.id)

async def title(update: Update,context: ContextTypes.DEFAULT_TYPE):
    saved_chat_id = context.bot_data.get('chat_id_bot', 0)
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )
    msg = await update.message.reply_text("загрузка")
    msg_id = msg.message_id
    chat_id= msg.chat_id
    usertext= "".join(context.args)
    print(usertext)
    if usertext == "":
        await update.message.reply_text("введите тему")
        return()
    else:
        msg = await update.message.reply_text("⏳ Генерирую заголовки..")
        msg_id = msg.message_id
        chat_id= msg.chat_id
        print(chat_id)
        def get_competion():
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
                    "content":f"придумай цепляющий заголовок связанный с {usertext}?"
                    }
                ]
                )
                
                print("kat")
                return completion.choices[0].message.content
        def get_competion1():
                client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
                )
                completion1 = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "<YOUR_SITE_URL>",  
                    "X-Title": "guest",
                },
                extra_body={},
                model="tngtech/deepseek-r1t2-chimera:free",
                messages=[
                    {
                    "role": "user",
                    "content": f"придумай цепляющий заголовок связанный с {usertext}?"
                    }
                ]
                )
                print("deepseek")
                return completion1.choices[0].message.content
        dots = ["⏳", "⌛", "⏳", "⌛"]
        loading_task = None
        async def loading_animation():
            for i in range(120):
                await asyncio.sleep(0.5)
                await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=msg.message_id,
                        text=f"💡 Генерирую заголовок {dots[i % len(dots)]}"
                    )
        loading_task = asyncio.create_task(loading_animation())
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            if chat_id == saved_chat_id:
                completion = await loop.run_in_executor(executor, get_competion)
                response = get_competion()
            else:
                completion = await loop.run_in_executor(executor, get_competion1)
                completion1= get_competion1()
        if loading_task:
            loading_task.cancel()
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=msg.message_id,
            text="📝 Обрабатываю результат..."
        )
        if chat_id == saved_chat_id:
            text1=response
        else:
            text1=completion1
        symbols_to_remove = ['*', '-', '#']   
        translation_table = str.maketrans('', '', ''.join(symbols_to_remove))  
        cleaned_text = text1.translate(translation_table)
        if len(cleaned_text) > 4000:
            cleaned_text = cleaned_text[:4000] + "\n\n... (текст сокращен)"
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            text=cleaned_text,
            message_id=msg.id)

async def hashtag(update: Update,context: ContextTypes.DEFAULT_TYPE):
    saved_chat_id = context.bot_data.get('chat_id_bot', 0)
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )
    usertext= "".join(context.args)
    print(usertext)
    if usertext == "":
        await update.message.reply_text("введите тему")
        return()
    else:
        msg = await update.message.reply_text("⏳ Генерирую хэштеги..")
        msg_id = msg.message_id
        chat_id= msg.chat_id
        print(chat_id)
        def get_competion():
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
                    "content":f"покажи самые популярные хэштеги связанные с {usertext}?"
                    }
                ]
                )
                
                print("kat")
                return completion.choices[0].message.content
        def get_competion1():
                client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
                )
                completion1 = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "<YOUR_SITE_URL>",  
                    "X-Title": "guest",
                },
                extra_body={},
                model="tngtech/deepseek-r1t2-chimera:free",
                messages=[
                    {
                    "role": "user",
                    "content": f"покажи самые популярные хэштеги связанные с  {usertext}?"
                    }
                ]
                )
                print("deepseek")
                return completion1.choices[0].message.content
        dots = ["⏳", "⌛", "⏳", "⌛"]
        loading_task = None
        async def loading_animation():
            for i in range(120):
                await asyncio.sleep(0.5)
                await context.bot.edit_message_text(
                        chat_id=update.effective_chat.id,
                        message_id=msg.message_id,
                        text=f"💡 Генерирую хэштеги {dots[i % len(dots)]}"
                    )
        loading_task = asyncio.create_task(loading_animation())
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            if chat_id == saved_chat_id:
                completion = await loop.run_in_executor(executor, get_competion)
                response = get_competion()
            else:
                completion = await loop.run_in_executor(executor, get_competion1)
                completion1= get_competion1()
        if loading_task:
            loading_task.cancel()
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=msg.message_id,
            text="📝 Обрабатываю результат..."
        )
        if chat_id == saved_chat_id:
            text1=response
        else:
            text1=completion1
        symbols_to_remove = ['*', '-', '#']   
        translation_table = str.maketrans('', '', ''.join(symbols_to_remove))  
        cleaned_text = text1.translate(translation_table)
        if len(cleaned_text) > 4000:
            cleaned_text = cleaned_text[:4000] + "\n\n... (текст сокращен)"
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            text=cleaned_text,
            message_id=msg.id)

async def image(update: Update,context: ContextTypes.DEFAULT_TYPE):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        )
    msg = await update.message.reply_text("⏳обрабатываю фото...")
    msg_id = msg.message_id
    chat_id= msg.chat_id
    usertext= "".join(context.args)
    
    def get_completion():
        completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>", 
        },
        extra_body={},
        model="google/gemma-3-27b-it:free",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "что изображено на картине"
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"{usertext}" 
                }
                }
            ]
            }
        ]
        )
        return completion.choices[0].message.content
     
 
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
        completion = await loop.run_in_executor(executor, get_completion)
        completion=get_completion()
    if loading_task:
            loading_task.cancel()
    await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=msg.message_id,
            text="📝 Обрабатываю результат..."
        )
    text1= completion
    symbols_to_remove = ['*', '-', '#']   
    translation_table = str.maketrans('', '', ''.join(symbols_to_remove))  
    cleaned_text = text1.translate(translation_table)
    if len(cleaned_text) > 4000:
            cleaned_text = cleaned_text[:4000] + "\n\n... (текст сокращен)"
    await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            text=cleaned_text,
            message_id=msg.id)