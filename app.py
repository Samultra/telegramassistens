#!/usr/bin/env python3
"""
Главный файл приложения для деплоя на хостинг
"""

import os
import sys
from bot import main

if __name__ == "__main__":
    # Проверяем наличие токена
    if not os.getenv('TELEGRAM_TOKEN'):
        print("❌ Ошибка: TELEGRAM_TOKEN не найден в переменных окружения!")
        print("Пожалуйста, установите переменную TELEGRAM_TOKEN в настройках хостинга")
        sys.exit(1)
    
    print("🚀 Запуск Telegram бота...")
    main()
