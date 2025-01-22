import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from cryptography.fernet import Fernet
from moviepy.editor import *

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Encryption/Decryption key
KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send me an encrypted text file to convert to a video!')

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = await file.download()

    # Decrypt the file
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    # Create a video from the decrypted text
    video = TextClip(decrypted_data.decode('utf-8'), fontsize=30, color='white')
    video = video.set_duration(5) # Set video duration
    video.write_videofile("output.mp4", fps=24)

    # Send the video back to the user
    await update.message.reply_video(open("output.mp4", 'rb'))

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    application.run_polling()

if __name__ == '__main__':
    main()
