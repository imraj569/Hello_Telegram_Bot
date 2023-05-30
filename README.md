# Hello_Telegram_Bot 💻📱

Hello_Telegram_Bot is a versatile Telegram bot that allows you to remotely control your PC using simple commands from your Telegram chat. With this bot, you can conveniently capture screenshots 🖼️, record audio 🎙️, and even shut down your PC remotely 🚀, all through the power of Telegram.

## Features 🚀

- **Screenshot:** Capture a screenshot of your PC remotely and receive it directly on your Telegram chat.
- **Audio Recording:** Initiate an audio recording on your PC and receive the recorded audio file on your Telegram chat.
- **Shutdown:** Safely shut down your PC from anywhere, using a command in your Telegram chat.

## Requirements 📋

To use Hello_Telegram_Bot, you will need:

- Python 3.6 or above installed on your PC.
- A Telegram account.
- A Telegram bot token. (You can obtain this by creating a new bot using the BotFather on Telegram)
- The chat ID of the user or group you want the bot to reply to.
- Modify the file paths in the `hellobot.pyw` and `main.pyw` scripts

## Installation ⚙️

1. Clone or download the source code from the [Hello_Telegram_Bot GitHub repository](https://github.com/imraj569/Hello_Telegram_Bot).

2. Install the required Python dependencies by running the following command in your terminal:

   ```shell
   pip install -r requirements.txt
   ```

3. Open the `.env` replacing the values with your own:

   ```plaintext
   BOT_TOKEN=your_bot_token
   CHAT_ID=your_chat_id
   ```

   Replace `your_bot_token` with your Telegram bot token and `your_chat_id` with the chat ID to which the bot should reply.

4. Open the `main.pyw` file and locate the following lines:

   ```python
   audio_file_path = "D:\\Automation Python\\recorded_audio.wav"
   screenshot_file_path = "D:\\Automation Python\\screenshot.png"
   ```

   Replace the file paths with the appropriate paths for your system. Make sure to escape any backslashes (`\`) in the path with an additional backslash (`\\`).

5. Save the changes to the `main.pyw` file.

6. Copy the `hellobot.pyw` file and paste it into the Windows startup folyou by type `win+r` in your pc it open run command type `shell:startup` and press enter now past the `hellobot.pyw` to here

## Usage 🚀

1. Run the bot by restart your pc the script automatically run after restart.

2. Start a conversation with your bot on Telegram chat by sending `/start` command.

3. Send commands to control your PC:

   - To capture a screenshot, send the command `/screenshot`.
   - To start an audio recording, send the command `/record`.
   - To shut down your PC, send the command `/shutdown`.

4. The bot will execute the requested action and send the result back to your Telegram bot.

## Security Considerations 🔒

Hello_Telegram_Bot is designed to reply only to the chat ID provided

 in the `.env` file. This helps minimize security risks. However, it is still important to take additional security measures:

- Keep your bot token and `.env` file secret and avoid sharing them with unauthorized individuals.

## Restart and Crash Recovery 🔄

Hello_Telegram_Bot is designed to automatically restart if it crashes. This ensures that the bot remains operational even in the event of unexpected failures.

## Disclaimer ⚠️

The Hello_Telegram_Bot project is provided as-is, without any warranty or liability. The authors are not responsible for any damage or misuse caused by the software. Use the bot responsibly and at your own risk.

## Contribution 🤝

Contributions to Hello_Telegram_Bot are welcome! If you encounter any issues or have ideas for new features, feel free to submit a pull request or open an issue on the [GitHub repository](https://github.com/imraj569/Hello_Telegram_Bot).

## License 📄

Hello_Telegram_Bot is released under the [MIT License](https://opensource.org/licenses/MIT). Please refer to the `LICENSE` file for more details.

---

Thank you for using Hello_Telegram_Bot! We hope this bot simplifies your remote PC control tasks. If you have any questions or need assistance, please don't hesitate to reach out on the GitHub repository or contact the bot's creator on [instagram](https://instagram.com/im.raj.569?igshid=ZGUzMzM3NWJiOQ==).
