from config import API_TOKEN
from neko_best_requests import *
import telebot

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, f"""Данный бот предоставляет возможность получить аниме гиф на определённую тему
Доступные темы: """)

@bot.message_handler(commands=['help'])
def help_command(message):
    ...
    
bot.infinity_polling()