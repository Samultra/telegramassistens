#!/usr/bin/env python3
"""
Главный файл приложения для деплоя DeepSeek бота на Railway
"""

import os
import sys
from bot_deepseek import DeepSeekBot

if __name__ == "__main__":
    # Проверяем наличие токена
    if not os.getenv('TELEGRAM_TOKEN'):
        print("❌ Ошибка: TELEGRAM_TOKEN не найден в переменных окружения!")
        print("Пожалуйста, установите переменную TELEGRAM_TOKEN в настройках Railway")
        sys.exit(1)
    
    # Проверяем наличие OpenRouter API ключа
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ Ошибка: OPENROUTER_API_KEY не найден в переменных окружения!")
        print("Пожалуйста, установите переменную OPENROUTER_API_KEY в настройках Railway")
        sys.exit(1)
    
    print("🚀 Запуск DeepSeek бота с философскими матами и черным юмором...")
    print("🌟 Используется OpenRouter API")
    print("🤖 DeepSeek Coder доступен!")
    print("💀 Циничные приветствия с философскими матами активированы!")
    print("🖕 Подъебы с философским подтекстом включены!")
    print("🧠 Черный юмор с ноткой философии активирован!")
    print("🎭 ЙОУ! Бот готов к работе, философ-неудачник!")
    
    # Запускаем бота
    bot = DeepSeekBot()
    bot.run()
