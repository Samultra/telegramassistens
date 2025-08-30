#!/usr/bin/env python3
"""
Скрипт для проверки готовности проекта к деплою
"""

import os
import sys

def check_file_exists(filename, description):
    """Проверка существования файла"""
    if os.path.exists(filename):
        print(f"✅ {filename} - {description}")
        return True
    else:
        print(f"❌ {filename} - {description} (НЕ НАЙДЕН)")
        return False

def main():
    print("🔍 Проверка готовности к деплою...")
    print("=" * 50)
    
    required_files = [
        ("Procfile", "Конфигурация для Railway"),
        ("runtime.txt", "Версия Python"),
        ("requirements_deploy.txt", "Зависимости для деплоя"),
        ("app.py", "Точка входа приложения"),
        ("bot.py", "Основной код бота"),
        ("config.py", "Конфигурация"),
        ("free_ai_services.py", "AI сервисы")
    ]
    
    all_files_exist = True
    for filename, description in required_files:
        if not check_file_exists(filename, description):
            all_files_exist = False
    
    print("=" * 50)
    
    if all_files_exist:
        print("🎉 Все файлы готовы к деплою!")
        print("\n📋 Следующие шаги:")
        print("1. Загрузите код в GitHub репозиторий")
        print("2. Получите токен бота у @BotFather")
        print("3. Зайдите на railway.app")
        print("4. Создайте новый проект из GitHub")
        print("5. Добавьте переменную TELEGRAM_TOKEN")
        print("6. Дождитесь автоматического деплоя")
    else:
        print("❌ Некоторые файлы отсутствуют!")
        print("Пожалуйста, создайте недостающие файлы перед деплоем.")
        sys.exit(1)

if __name__ == "__main__":
    main()
