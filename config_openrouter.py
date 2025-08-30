import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# OpenRouter API Key
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# Настройки сообщений
MAX_MESSAGE_LENGTH = 4096

# Команды бота
COMMANDS = {
    'start': 'Запуск бота',
    'help': 'Справка по командам',
    'code': 'Генерация кода',
    'solve': 'Решение задач',
    'search': 'Поиск информации',
    'chat': 'Чат с ИИ',
    'models': 'Выбор модели ИИ',
    'stats': 'Статистика использования'
}

# Модели OpenRouter
OPENROUTER_MODELS = {
    'deepseek': 'deepseek-ai/deepseek-coder-6.7b-instruct',
    'deepseek_large': 'deepseek-ai/deepseek-coder-33b-instruct',
    'codellama': 'meta-llama/codellama-7b-instruct',
    'wizardcoder': 'wizardlm/wizardcoder-15b-v1.0',
    'phind': 'phind/phind-codellama-34b-v2',
    'claude': 'anthropic/claude-3-haiku',
    'gpt': 'openai/gpt-3.5-turbo',
    'gemini': 'google/gemini-pro'
}

# Лимиты OpenRouter
DAILY_LIMITS = {
    'free_models': 100,    # 100 запросов в день бесплатно
    'paid_models': 1000    # 1000 запросов в день для платных
}

# Проверка обязательных переменных
def validate_config():
    """Проверка конфигурации"""
    errors = []
    
    if not TELEGRAM_TOKEN:
        errors.append("TELEGRAM_TOKEN не найден в .env файле")
    
    if not OPENROUTER_API_KEY:
        errors.append("OPENROUTER_API_KEY не найден в .env файле")
    
    return errors

# Получение информации о конфигурации
def get_config_info():
    """Получение информации о конфигурации"""
    return {
        'telegram_token': '✅ Настроен' if TELEGRAM_TOKEN else '❌ Не настроен',
        'openrouter_api_key': '✅ Настроен' if OPENROUTER_API_KEY else '❌ Не настроен',
        'max_message_length': MAX_MESSAGE_LENGTH,
        'available_models': len(OPENROUTER_MODELS),
        'daily_limits': DAILY_LIMITS
    }
