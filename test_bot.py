#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from free_ai_services import FreeAIServices
from huggingface_client import HuggingFaceClient

load_dotenv()

async def test_ai_services():
    """Тестирование бесплатных ИИ сервисов"""
    print("🤖 Тестирование бесплатных ИИ сервисов...")
    
    try:
        ai = FreeAIServices()
        
        # Тест генерации текста
        print("📝 Тест генерации текста...")
        response = await ai.generate_text_response("Привет! Как дела?")
        print(f"✅ Ответ: {response[:100]}...")
        
        # Тест генерации кода
        print("💻 Тест генерации кода...")
        code = await ai.generate_code("функция для сортировки списка")
        print(f"✅ Код: {code[:100]}...")
        
        # Тест статистики
        print("📊 Тест статистики...")
        stats = ai.get_usage_stats()
        print(f"✅ Статистика: {stats}")
        
        print("🎉 Все тесты ИИ сервисов прошли успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка в ИИ сервисах: {e}")

def test_huggingface_client():
    """Тестирование Hugging Face клиента"""
    print("🤗 Тестирование Hugging Face клиента...")
    
    try:
        client = HuggingFaceClient()
        
        # Тест подключения
        print("🔗 Тест подключения...")
        if client.test_connection():
            print("✅ Подключение к Hugging Face успешно!")
        else:
            print("⚠️ Проблемы с подключением к Hugging Face")
        
        # Тест доступных моделей
        print("📋 Тест доступных моделей...")
        models = client.get_available_models()
        print(f"✅ Доступно моделей: {len(models)}")
        
        print("🎉 Все тесты Hugging Face клиента прошли успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка в Hugging Face клиенте: {e}")

def test_config():
    """Тестирование конфигурации"""
    print("⚙️ Тестирование конфигурации...")
    
    try:
        # Проверяем наличие токенов
        telegram_token = os.getenv('TELEGRAM_TOKEN')
        huggingface_token = os.getenv('HUGGINGFACE_TOKEN')
        
        if telegram_token:
            print(f"✅ Telegram токен: {telegram_token[:20]}...")
        else:
            print("❌ Telegram токен не найден!")
        
        if huggingface_token:
            print(f"✅ Hugging Face токен: {huggingface_token[:20]}...")
        else:
            print("❌ Hugging Face токен не найден!")
        
        print("🎉 Конфигурация проверена!")
        
    except Exception as e:
        print(f"❌ Ошибка в конфигурации: {e}")

def main():
    print("🚀 Запуск тестирования Telegram ИИ бота...")
    print("=" * 50)
    
    test_config()
    print()
    
    test_huggingface_client()
    print()
    
    asyncio.run(test_ai_services())
    print()
    
    print("✨ Тестирование завершено!")
    print("\n📋 Рекомендации:")
    print("1. ✅ Убедитесь, что все API ключи настроены в файле .env")
    print("2. ✅ Проверьте подключение к интернету")
    print("3. ✅ Установите все зависимости: pip install -r requirements.txt")
    print("4. 🚀 Запустите бота: python bot.py")
    print("\n🎯 Ваш бот готов к работе с DeepSeek!")

if __name__ == "__main__":
    main()
