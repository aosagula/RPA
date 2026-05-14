import telegram
import requests
#bot_token = '6884941709:AAFedvLx2DxTRtuQJ59BIO3AoB00VJVDE6E'
#chat_id = '4008612871'  # Replace with the actual chat ID where you want to receive notifications

# Initialize bot
#bot = telegram.Bot(token=bot_token)
bot_token=""

#bot.send_message(chat_id, text='HOLA')#, parse_mode=ParseMode.MARKDOWN)
    
error_description= "gola prueba"
me = requests.get(f'https://api.telegram.org/bot{bot_token}/getMe')
chat = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates')
chat_id = '6870674844'
base_url =  f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={error_description}"#'https://api.telegram.org/bot6884941709:AAFedvLx2DxTRtuQJ59BIO3AoB00VJVDE6E/sendMessage?chat_id=-4008612871&text="{}"'.format(error_description)
requests.get(base_url)
