import os
from pytube import YouTube
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Define your bot token
BOT_TOKEN = '7445057320:AAjksidFQiXfmAWfibOX3f7UZXzERQUCyXFh35ug'

# Function to get the audio stream URL
def get_audio_stream_url(youtube_url):
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    return audio_stream.url

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Play", callback_data='play'),
            InlineKeyboardButton("Stop", callback_data='stop'),
        ],
        [InlineKeyboardButton("Help", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hello! I am your music bot. Choose an option:', reply_markup=reply_markup)

# Help command handler
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('You can control me by using the buttons:\n'
                              'Play - Play a song from YouTube\n'
                              'Stop - Stop the music\n'
                              'Help - Get help information')

# Callback handler for button presses
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'play':
        query.edit_message_text(text="Send me a YouTube URL using the /play <youtube_url> command.")
    elif query.data == 'stop':
        query.edit_message_text(text="Stopping music... (Note: Implement stop functionality if streaming)")
    elif query.data == 'help':
        help_command(update, context)

# Play music from YouTube command handler
def play_music(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text('Please provide a YouTube URL. Usage: /play <youtube_url>')
        return

    youtube_url = context.args[0]
    update.message.reply_text(f'Playing music from: {youtube_url}')

    try:
        audio_url = get_audio_stream_url(youtube_url)
        update.message.reply_audio(audio=audio_url)
    except Exception as e:
        update.message.reply_text(f'An error occurred: {e}')

# Main function to set up the bot
def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("play", play_music))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
