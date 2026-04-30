import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env en el mismo directorio que este archivo
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    def __init__(self, dux_username, dux_password, djve_xml_path="", db_url="", db_name="",
                db_username="", db_password="", db_port="", dux_url="" ,
                email_host="", email_port="", email_user="", email_password="", download_path="",
                dux_txt_to_sim="", dux_factura_pdf="", telegram_bot_token="", telegram_chat_id=""):
        self.dux_username = dux_username
        self.dux_password = dux_password
        self.djve_xml_path = djve_xml_path
        self.db_url = db_url
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.db_port = db_port
        self.dux_url = dux_url
        self.email_host = email_host
        self.email_port = email_port
        self.email_user = email_user
        self.email_password = email_password
        self.download_path = download_path
        self.dux_txt_to_sim = dux_txt_to_sim
        self.dux_factura_pdf = dux_factura_pdf
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id

# Validar variables de entorno requeridas
def validate_env_variables():
    """Valida que todas las variables de entorno requeridas estén presentes"""
    required_vars = [
        'DUX_USERNAME', 'DUX_PASSWORD', 'DUX_URL',
        'DB_URL', 'DB_NAME', 'DB_USERNAME', 'DB_PASSWORD', 'DB_PORT',
        'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USER', 'EMAIL_PASSWORD',
        'DOWNLOAD_PATH', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"ERROR: Faltan las siguientes variables de entorno en el archivo .env:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPor favor, configura el archivo .env usando .env.example como referencia.")
        sys.exit(1)

validate_env_variables()

config = Config(
    dux_username=os.getenv('DUX_USERNAME'),
    dux_password=os.getenv('DUX_PASSWORD'),
    djve_xml_path=os.getenv('DJVE_XML_PATH'),
    db_url=os.getenv('DB_URL'),
    db_name=os.getenv('DB_NAME'),
    db_username=os.getenv('DB_USERNAME'),
    db_password=os.getenv('DB_PASSWORD'),
    db_port=int(os.getenv('DB_PORT', 3306)),
    dux_url=os.getenv('DUX_URL'),
    email_host=os.getenv('EMAIL_HOST'),
    email_port=int(os.getenv('EMAIL_PORT', 465)),
    email_user=os.getenv('EMAIL_USER'),
    email_password=os.getenv('EMAIL_PASSWORD'),
    download_path=os.getenv('DOWNLOAD_PATH'),
    dux_txt_to_sim=os.getenv('DUX_TXT_TO_SIM'),
    dux_factura_pdf=os.getenv('DUX_FACTURA_PDF'),
    telegram_bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
    telegram_chat_id=os.getenv('TELEGRAM_CHAT_ID')
)




