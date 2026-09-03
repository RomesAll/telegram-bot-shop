from dotenv import load_dotenv
from pathlib import Path
import os

APP_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent

load_dotenv(dotenv_path=f'{APP_DIR}/.env')


class Settings:
    """Базовые настройки для проекта"""
    admin_id = os.getenv('ADMIN_ID')
    bot_token = os.getenv('BOT_TOKEN')


settings = Settings()