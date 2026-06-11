import telebot
from dotenv import load_dotenv
from datetime import datetime
import psycopg2
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if not TOKEN:
    print("BOT_TOKEN not found")
    exit()

bot = telebot.TeleBot(TOKEN)

def save_mentioned_message(message):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    group_id = message.chat.id if message.chat.type in ["group", "supergroup"] else None
    group_name = message.chat.title if message.chat.type in ["group", "supergroup"] else None

    cur.execute("""
        INSERT INTO mentioned_messages (
            message_id,
            message_text,
            user_id,
            username,
            first_name,
            group_id,
            group_name,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        message.message_id,
        message.text,
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        group_id,
        group_name,
        datetime.now()
    ))

    conn.commit()
    cur.close()
    conn.close()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Hello! Welcome. I am your Telegram group assistant bot."
    )


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:

        if member.id == bot.get_me().id:
            bot.send_message(
                message.chat.id,
                "Hello everyone 👋\nI am your group assistant bot."
            )
        else:
            bot.send_message(
                message.chat.id,
                f"Welcome {member.first_name} 👋\n"
                "Nice to meet you!\n"
                "We look forward to having you in our group."
            )


@bot.message_handler(content_types=['left_chat_member'])
def goodbye_member(message):
    user = message.left_chat_member

    bot.send_message(
        message.chat.id,
        f"{user.first_name} has left the group. Goodbye 👋"
    )


@bot.message_handler(content_types=["text"])
def handle_text_messages(message):
    mention = "@pytutorbackendbot"

    if mention in message.text.lower():
        save_mentioned_message(message)

        bot.send_message(
            message.chat.id,
            "I saw my mention and saved the message details. \n I'm Feeling helpful! 😊"
        )
    else:
        bot.send_message(
            message.chat.id,
            "I received your message."
        )


print("Bot is running...")
bot.infinity_polling(skip_pending=True)