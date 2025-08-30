#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from friendli_services import FriendliServices

load_dotenv()

async def test_friendli_services():
    """Тестирование Friendli.ai сервисов"""
    print("🧪 Тестирование Friendli.ai сервисов...")
    print("-" * 50)
    
    # Тест подключения
    print("🔌 Тест подключения к Friendli.ai...")
    if friendli_services.test_connection():
        print("✅ Подключение к Friendli.ai успешно!")
    else:
        print("❌ Не удалось подключиться к Friendli.ai")
        return
    
    print()
    
    # Тест генерации текста
    print("📝 Тест генерации текста (основной чат)...")
    try:
        response = await friendli_services.generate_text_response(
            "Привет! Расскажи кратко о том, что такое искусственный интеллект.",
            max_tokens=500,
            model='qwen3_highlights'
        )
        print(f"✅ Ответ получен! Длина: {len(response)} символов")
        print(f"📄 Первые 200 символов: {response[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print()
    
    # Тест генерации кода
    print("💻 Тест генерации кода...")
    try:
        response = await friendli_services.generate_code(
            "создай функцию для сортировки списка чисел",
            model='qwen3_highlights'
        )
        print(f"✅ Код сгенерирован! Длина: {len(response)} символов")
        print(f"📄 Первые 300 символов: {response[:300]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print()
    
    # Тест решения задач
    print("🧮 Тест решения задач...")
    try:
        response = await friendli_services.solve_problem(
            "вычисли факториал числа 5",
            model='qwen3_highlights'
        )
        print(f"✅ Задача решена! Длина: {len(response)} символов")
        print(f"📄 Первые 300 символов: {response[:300]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print()
    
    # Тест поиска информации
    print("🔍 Тест поиска информации...")
    try:
        response = await friendli_services.search_information(
            "что такое машинное обучение",
            model='qwen3_highlights'
        )
        print(f"✅ Информация найдена! Длина: {len(response)} символов")
        print(f"📄 Первые 300 символов: {response[:300]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print()
    
    # Тест чата
    print("💬 Тест обычного общения...")
    try:
        response = await friendli_services.chat_response(
            "расскажи анекдот про программистов",
            model='qwen3_highlights'
        )
        print(f"✅ Чат работает! Длина: {len(response)} символов")
        print(f"📄 Первые 300 символов: {response[:300]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print()
    
    # Получение статистики
    print("📊 Получение статистики...")
    try:
        stats = friendli_services.get_usage_stats()
        print("✅ Статистика получена!")
        print(f"🚀 Qwen3 Highlights: {stats['qwen3_highlights_used']}/{stats['qwen3_highlights_limit']}")
        print(f"📊 Всего запросов: {stats['total_requests_used']}/{stats['total_requests_limit']}")
        print(f"🔄 Сброс: {stats['reset_time']}")
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")

def test_config():
    """Тест конфигурации"""
    print("🔧 Проверка конфигурации...")
    print("-" * 30)
    
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    friendli_api_key = os.getenv('FRIENDLI_API_KEY')
    
    if telegram_token:
        print("📱 Telegram Token: ✅ Настроен")
    else:
        print("📱 Telegram Token: ❌ Не настроен")
    
    if friendli_api_key:
        print("🚀 Friendli.ai API: ✅ Настроен")
    else:
        print("🚀 Friendli.ai API: ❌ Не настроен")
    
    if telegram_token and friendli_api_key:
        print("\n✅ Конфигурация корректна!")
        return True
    else:
        print("\n❌ Конфигурация неполная!")
        return False

def main():
    print("🚀 Запуск тестирования Telegram ИИ бота с Friendli.ai...")
    print("🚀 Qwen3 Highlights - лучшая модель для кода!")
    print("=" * 60)
    
    if not test_config():
        print("\n❌ Проверьте настройки в файле .env")
        print("📝 Создайте файл .env на основе env_friendli.txt")
        return
    
    print()
    asyncio.run(test_friendli_services())
    
    print("\n" + "=" * 60)
    print("✨ Тестирование завершено!")
    print("\n📋 Рекомендации:")
    print("1. ✅ Убедитесь, что все API ключи настроены в файле .env")
    print("2. ✅ Проверьте подключение к интернету")
    print("3. ✅ Установите все зависимости: pip install -r requirements_clean.txt")
    print("4. 🚀 Запустите гибридного бота: python bot_hybrid.py")
    print("\n🎯 Ваш бот готов к работе с Qwen3 Highlights!")
    print("💬 Просто напишите сообщение - бот сам поймет, что вам нужно!")
    print("🚀 Высокие лимиты запросов через Friendli.ai!")

if __name__ == "__main__":
    # Инициализируем сервисы для тестирования
    friendli_services = FriendliServices()
    main()
