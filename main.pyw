import telebot
import pyaudio 
import wave
import os
import random
import pyautogui
from dotenv import load_dotenv
import time  

# Load environment variables from .env file
load_dotenv()

# Retrieve bot token and chat ID from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Set up your Telegram bot using the API token
bot = telebot.TeleBot(BOT_TOKEN)

# Handler for unhandled exceptions
def handle_exception(e):
    time.sleep(5)
    main()  

# Set up error handling
def setup_error_handlers():
    for attr in dir(telebot.apihelper):
        if attr.endswith('_handler'):
            getattr(telebot.apihelper, attr)(handle_exception)

# Main function
def main():
    setup_error_handlers()
    bot.polling()

@bot.message_handler(commands=['start'])
def handle_start_command(message):
    if str(message.chat.id) == CHAT_ID:
        bot.send_message(CHAT_ID, random.choice(["access granted..✅", "connection build successfully..✅","connected...✅"]))
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")

# Define constants
RECORDED_AUDIO_PATH = 'D:\\Hello_Telegram_Bot\\recorded_audio.wav'
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

# Implement the capture_screenshot() function to capture the screen
def capture_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot

# Implement the send_screenshot() function to send the screenshot through the Telegram bot
def send_screenshot(chat_id, screenshot):
    screenshot_path = 'D:\\Hello_Telegram_Bot\\screenshot.png'
    screenshot.save(screenshot_path)
    screenshot_file = open(screenshot_path, 'rb')
    bot.send_photo(chat_id, screenshot_file)
    screenshot_file.close()
    os.remove(screenshot_path)

def shutdown_pc():
    os.system("shutdown /s /t 5")

@bot.message_handler(commands=['shutdown'])
def handle_shutdown_command(message):
    if str(message.chat.id) == CHAT_ID:
        bot.send_message(CHAT_ID, "⚠️ Are you sure you want to shut down the PC? (yes/no)")
        bot.register_next_step_handler(message, handle_shutdown_confirmation)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")

def handle_shutdown_confirmation(message):
    if str(message.chat.id) == CHAT_ID:
        confirmation = message.text.strip().lower()
        if confirmation == "yes":
            bot.send_message(CHAT_ID, "⚠️ Shutting down the PC in 5 second...")
            shutdown_pc()
        else:
            bot.send_message(CHAT_ID, "⛔️ Shutdown cancelled.")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            time.sleep(5)
