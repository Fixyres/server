import telebot
import paramiko
from telebot import types
import os

TOKEN = '7288710360:AAEZvqspDc56f2J9HiOSa6nB-_lLuD7zGcg'
SSH_HOST = 's2.serv00.com'
SSH_PORT = 22
SSH_USER = 'Foxy437'
SSH_PASSWORD = '*P9*gNrMDWAL#1a1c9xb'

AUTHORIZED_USERS = {1335063985}

bot = telebot.TeleBot(TOKEN)

def get_ssh_client():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    return ssh_client

@bot.message_handler(func=lambda m: True)
def execute_command(message, command):
    ssh_client = get_ssh_client()
    try:
        full_command = f'clear; {command}'
        stdin, stdout, stderr = ssh_client.exec_command(full_command)
        pidoras = stdout.read().decode() + stderr.read().decode()

        if len(pidoras) > 4000:
            output = '😿 *Хозяин, из-за дурацких лимитов тг я не смогу отправить тебе ответ, извини(((*'
            bot.reply_to(message, output, parse_mode='Markdown')
            return

        elif not pidoras.strip():
            output = '✅'
            bot.reply_to(message, output, parse_mode='Markdown')
        else:
            output = f'🐱 *Котик тебе ответил:*\n{pidoras}'
            bot.reply_to(message, output, parse_mode='Markdown')
        return
    
    finally:
        ssh_client.close()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        return

    photo_path = 'cat.png'

    if os.path.exists(photo_path):
        with open(photo_path, 'rb') as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption='*Приветиккк мой хозяин* `/⁠ᐠ⁠｡⁠ꞈ⁠｡⁠ᐟ⁠\ `',
                parse_mode='Markdown'
            )
    else:
        bot.send_message(message.chat.id, '*Приветиккк мой хозяин* `/⁠ᐠ⁠｡⁠ꞈ⁠｡⁠ᐟ⁠\ `', parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        return

    command = message.text
    output = execute_command(command)

@bot.inline_handler(lambda query: True)
def handle_inline_query(inline_query):
    user_id = inline_query.from_user.id
    if user_id not in AUTHORIZED_USERS:
        bot.answer_inline_query(inline_query.id, [])
        return

    query_text = inline_query.query
    results = []

    if len(AUTHORIZED_USERS) == 1:
        if query_text:
            output = execute_command(query_text)
            results.append(types.InlineQueryResultArticle(
                id='1',
                title='🐱 Отправить команду ฅ⁠^⁠•⁠ﻌ⁠•⁠^⁠ฅ',
                input_message_content=types.InputTextMessageContent(output),
                description='😽 Отправить команду котику.',
                thumbnail_url='https://i.imgur.com/bTky2NE.jpeg'
            ))

    bot.answer_inline_query(inline_query.id, results)
    
bot.polling(none_stop=True)
