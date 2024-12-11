import telegram
bot_token = '6884941709:AAFedvLx2DxTRtuQJ59BIO3AoB00VJVDE6E'
chat_id = '4008612871'  # Replace with the actual chat ID where you want to receive notifications

# Initialize bot
bot = telegram.Bot(token=bot_token)


bot.send_message(chat_id, text='HOLA')#, parse_mode=ParseMode.MARKDOWN)
    