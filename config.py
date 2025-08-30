import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# OpenAI API Key (для GPT и DALL-E)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Hugging Face API Token
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

# Настройки моделей
GPT_MODEL = "gpt-3.5-turbo"
DALLE_MODEL = "dall-e-3"
IMAGE_MODEL = "stabilityai/stable-diffusion-2-1"

# Лимиты
MAX_MESSAGE_LENGTH = 4096
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

# Команды бота
COMMANDS = {
    'start': 'Запустить бота',
    'help': 'Показать справку',
    'code': 'Написать код по описанию',
    'solve': 'Решить задачу',
    'image': 'Сгенерировать изображение',
    'search': 'Найти информацию',
    'chat': 'Общий чат с ИИ'
}
