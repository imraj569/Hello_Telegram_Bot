#This bot helps you to control your pc from anywhere through telegram
#You can modify anything but please give cradit if any use.
#Author - Rajkishor Patra
#Version - 2.0
'''
------------------------------------------------------------------
                *Feactures*
------------------------------------------------------------------
/screenshot - take screenshot
/record - record audio in a given time limit 
/lock - lock pc screen
/shutdown - shutdown the pc
------------------------------------------------------------------
            *additional feactures*
------------------------------------------------------------------
>it can copy any text that you directly sended to it 
except the texts start with /
ex-
/hello ❌
hello ✅

>it can detect urls and open ask before open a url on your defult pc 
browser.
'''
#-----------------------------------------------------------------
import pyaudio 
import wave
import telebot
import os,subprocess
import webbrowser
import random
import pyautogui
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

# Define constants
username = os.getlogin()
RECORDED_AUDIO_PATH = 'audio.wav'
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Define a handler for the /record command
@bot.message_handler(commands=['record'])
def handle_record_command(message):
    if str(message.chat.id) == CHAT_ID:
        bot.send_message(CHAT_ID, "Please enter the duration of the audio recording in seconds:")
        bot.register_next_step_handler(message, start_audio_recording)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")

def start_audio_recording(message):
    duration = int(message.text)
    if duration <= 0:
        bot.send_message(CHAT_ID, "Invalid duration. Please enter a positive number.")
        return

    # Send initial process update
    bot.send_message(CHAT_ID, "Recording started...")

    # Record audio
    try:
        record_audio(duration)
    except OSError:
        # Handling interruption when PC wakes up from sleep mode
        bot.send_message(CHAT_ID, "Recording interrupted.")

    # Send process update
    bot.send_message(CHAT_ID, "Recording finished.")

    # Send recorded audio to a specific chat ID
    send_audio(CHAT_ID)

    # Send final process update
    bot.send_message(CHAT_ID, "Audio sent successfully.")

def record_audio(duration):
    RECORD_SECONDS = duration
    frames = []

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(RECORDED_AUDIO_PATH, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

# Implement the send_audio() function to send the recorded audio file through the Telegram bot
def send_audio(chat_id):
    with open(RECORDED_AUDIO_PATH, 'rb') as audio_file:
        bot.send_audio(chat_id, audio_file)
    # Delete the wave file after sending
    os.remove(RECORDED_AUDIO_PATH)
     
@bot.message_handler(commands=['screenshot'])
def handle_screenshot_command(message):
    if str(message.chat.id) == CHAT_ID:
        try:
            bot.send_message(CHAT_ID, "Taking screenshot...")
            screenshot = capture_screenshot()
            send_screenshot(CHAT_ID, screenshot)
            bot.send_message(CHAT_ID, "Screenshot sent successfully.")
        except Exception as e:
            bot.send_message(CHAT_ID, "An error occurred during screenshot capture.")
            raise e
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")

def capture_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot

def send_screenshot(chat_id, screenshot):
    username = os.getlogin()
    screenshot_path = 'screenshot.png'
    screenshot.save(screenshot_path)
    screenshot_file = open(screenshot_path, 'rb')
    bot.send_photo(chat_id, screenshot_file)
    screenshot_file.close()
    os.remove(screenshot_path)

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

@bot.message_handler(commands=['lock'])
def handle_lock_command(message):
    if str(message.chat.id) == CHAT_ID:
        bot.send_message(CHAT_ID, "Pc is Locked🔐")
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])

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
