import os
import datetime
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

WORK_HOURS = (10, 20)  # Рабочее время

def is_off_hours():
    now = datetime.datetime.now()
    return now.hour < WORK_HOURS[0] or now.hour >= WORK_HOURS[1]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if is_off_hours():
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты дружелюбный представитель цветочной мастерской Flower Craft. Пиши кратко и с заботой."},
                {"role": "user", "content": user_message}
            ]
        )
        await update.message.reply_text(response['choices'][0]['message']['content'])
    else:
        await update.message.reply_text("Спасибо за сообщение! Наши флористы на месте и скоро с вами свяжутся 🌸")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
