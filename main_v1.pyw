#This bot helps you to control your pc from anywhere through telegram
#You can modify anything but please give cradit if any use.
#Author - Rajkishor Patra
#Version - 1.0
#-----------------------------------------------------------------
#feactures
'''
it send a welcome message when it connected to internet for the first time it run.
/start-start the bot
/shutdown - shutdown the system
1.it can open any url in your defult browser by sending it a url it automatically dectate and open.
2.copy text to clipboard when you send it any text except text start with / like 
/hello world ❌
hello world ✅
'''
#-----------------------------------------------------------------
import telebot
import os
import webbrowser
import random
import time
import pyperclip
from telebot import types

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
bot = telebot.TeleBot(BOT_TOKEN)

def handle_exception(e):
    time.sleep(5)
    main()

def setup_error_handlers():
    for attr in dir(telebot.apihelper):
        if attr.endswith('_handler'):
            getattr(telebot.apihelper, attr)(handle_exception)

def main():
    setup_error_handlers()
    send_welcome_message()
    bot.polling()
    
def send_welcome_message():
    # Add your welcome message here
    welcome_message = "🐈Hello Bot is now online🌐 and connected✅🚀"
    bot.send_message(CHAT_ID, welcome_message)

@bot.message_handler(commands=['start'])
def handle_start_command(message):
    if str(message.chat.id) == CHAT_ID:
        bot.send_message(CHAT_ID, random.choice(["Access Granted..✅", "Connection build successfully..✅","Connected...✅"]))
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")

@bot.message_handler(commands=['shutdown'])
def handle_shutdown_command(message):
    if str(message.chat.id) == CHAT_ID:
        bot.send_message(CHAT_ID, "⚠️ Are you sure you want to shut down the PC? (yes/no)")
        bot.register_next_step_handler(message, handle_shutdown_confirmation)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")

def shutdown_pc():
    os.system("shutdown /s /t 5")

def handle_shutdown_confirmation(message):
    if str(message.chat.id) == CHAT_ID:
        confirmation = message.text.strip().lower()
        if confirmation == "yes":
            bot.send_message(CHAT_ID, "⚠️ Shutting down the PC in 5 seconds...")
            shutdown_pc()
        else:
            bot.send_message(CHAT_ID, "⛔️ Shutdown cancelled.")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")

@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    if str(message.chat.id) == CHAT_ID:
        # Remove blank lines from the message text
        cleaned_text = "\n".join(line for line in message.text.splitlines() if line.strip())

        if cleaned_text.startswith("http://") or cleaned_text.startswith("https://"):
            # If the cleaned text is a URL, ask the user if they want to open it
            url = cleaned_text
            markup = types.ReplyKeyboardMarkup(row_width=2)
            item_yes = types.KeyboardButton('Yes')
            item_no = types.KeyboardButton('No')
            markup.add(item_yes, item_no)
            bot.send_message(message.chat.id, f"Do you want to open the URL:\n{url}?", reply_markup=markup)
            bot.register_next_step_handler(message, handle_url_decision, url)

        elif cleaned_text.startswith("/"):
            pass

        else:
            # Copy the cleaned text to clipboard
            pyperclip.copy(cleaned_text)
            bot.send_message(CHAT_ID, "✅Text copied to clipboard.📋")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")

def handle_url_decision(message, url):
    if message.text.lower() == 'yes':
        webbrowser.open(url)
        bot.send_message(message.chat.id, "Url Opened 🌐✅")
    elif message.text.lower() == 'no':
        bot.send_message(message.chat.id, "URL not opened.")
    else:
        bot.send_message(message.chat.id, "Invalid response. Please type 'Yes' or 'No'.")

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            time.sleep(2)
