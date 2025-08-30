#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from openrouter_services import OpenRouterServices
from config_openrouter import validate_config, get_config_info

load_dotenv()

async def test_openrouter_services():
    """Тестирование OpenRouter сервисов"""
    print("🧪 Тестирование OpenRouter сервисов...")
    print("-" * 50)
    
    ai_services = OpenRouterServices()
    
    # Тест подключения
    print("🔌 Тест подключения к OpenRouter...")
    if ai_services.test_connection():
        print("✅ Подключение к OpenRouter успешно!")
    else:
        print("❌ Не удалось подключиться к OpenRouter")
        print("💡 Проверьте API ключ и интернет-соединение")
        return
    
    # Тест генерации текста (основной функционал чата)
    print("\n📝 Тест генерации текста (основной чат)...")
    try:
        response = await ai_services.generate_text_response(
            "Объясни принципы работы нейронных сетей простыми словами",
            max_tokens=500,
            model='deepseek'
        )
        if response.startswith("❌"):
            print(f"❌ Ошибка: {response}")
        else:
            print("✅ Генерация текста успешна!")
            print(f"📄 Ответ: {response[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка при генерации текста: {e}")
    
    # Тест генерации кода через обычный чат
    print("\n💻 Тест генерации кода через чат...")
    try:
        enhanced_prompt = """Напиши полноценный, рабочий код для следующей задачи: создай функцию для вычисления факториала числа

Требования:
1. Код должен быть полностью рабочим
2. Добавь подробные комментарии
3. Включи обработку ошибок
4. Добавь примеры использования
5. Объясни логику работы

Формат ответа:
```python
# Код здесь
```

## Объяснение:
Детальное объяснение решения"""
        
        response = await ai_services.generate_text_response(
            enhanced_prompt,
            max_tokens=1000,
            model='deepseek'
        )
        if response.startswith("❌"):
            print(f"❌ Ошибка: {response}")
        else:
            print("✅ Генерация кода через чат успешна!")
            print(f"💻 Ответ: {response[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка при генерации кода: {e}")
    
    # Тест решения задач через чат
    print("\n🧮 Тест решения задач через чат...")
    try:
        enhanced_prompt = """Реши следующую задачу: вычисли факториал числа 10

Требования к ответу:
1. Пошаговое решение
2. Объяснение каждого шага
3. Математические выкладки (если применимо)
4. Альтернативные способы решения
5. Практические примеры

Дай подробный, понятный ответ с примерами."""
        
        response = await ai_services.generate_text_response(
            enhanced_prompt,
            max_tokens=800,
            model='deepseek'
        )
        if response.startswith("❌"):
            print(f"❌ Ошибка: {response}")
        else:
            print("✅ Решение задачи через чат успешно!")
            print(f"🧮 Ответ: {response[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка при решении задачи: {e}")
    
    # Тест поиска информации через чат
    print("\n🔍 Тест поиска информации через чат...")
    try:
        enhanced_prompt = """Найди и проанализируй информацию по запросу: что такое машинное обучение

Требования к ответу:
1. Подробный анализ темы
2. Актуальная информация
3. Практические примеры
4. Связи с другими концепциями
5. Практическое применение

Предоставь глубокий, информативный ответ."""
        
        response = await ai_services.generate_text_response(
            enhanced_prompt,
            max_tokens=600,
            model='deepseek'
        )
        if response.startswith("❌"):
            print(f"❌ Ошибка: {response}")
        else:
            print("✅ Поиск информации через чат успешен!")
            print(f"🔍 Ответ: {response[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка при поиске информации: {e}")
    
    # Тест обычного общения
    print("\n💬 Тест обычного общения...")
    try:
        enhanced_prompt = """Ответь на следующее сообщение: расскажи анекдот про программистов

Требования к ответу:
1. Полезный и информативный ответ
2. Если это вопрос - дай развернутый ответ
3. Если это просьба - выполни её
4. Если это шутка - поддержи юмор
5. Будь дружелюбным и полезным

Дай качественный, полезный ответ."""
        
        response = await ai_services.generate_text_response(
            enhanced_prompt,
            max_tokens=400,
            model='deepseek'
        )
        if response.startswith("❌"):
            print(f"❌ Ошибка: {response}")
        else:
            print("✅ Обычное общение работает!")
            print(f"💬 Ответ: {response[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка при общении: {e}")
    
    # Получение статистики
    print("\n📊 Получение статистики...")
    try:
        stats = ai_services.get_usage_stats()
        print("✅ Статистика получена!")
        print(f"🆓 Бесплатные модели: {stats['free_models_used']}/{stats['free_models_limit']}")
        print(f"💳 Платные модели: {stats['paid_models_used']}/{stats['paid_models_limit']}")
        print(f"🔄 Сброс: {stats['reset_time']}")
    except Exception as e:
        print(f"❌ Ошибка при получении статистики: {e}")

def test_config():
    """Тестирование конфигурации"""
    print("⚙️ Тестирование конфигурации...")
    print("-" * 50)
    
    errors = validate_config()
    if errors:
        print("❌ Ошибки в конфигурации:")
        for error in errors:
            print(f"  • {error}")
        return False
    
    print("✅ Конфигурация корректна!")
    
    config_info = get_config_info()
    print(f"📱 Telegram Token: {config_info['telegram_token']}")
    print(f"🔑 OpenRouter API: {config_info['openrouter_api_key']}")
    print(f"📏 Максимальная длина сообщения: {config_info['max_message_length']}")
    print(f"🤖 Доступных моделей: {config_info['available_models']}")
    print(f"💰 Лимиты: {config_info['daily_limits']}")
    
    return True

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования Telegram ИИ бота с OpenRouter...")
    print("💬 Режим: Обычный чат с автоматическими подсказками!")
    print("=" * 60)
    
    # Тест конфигурации
    if not test_config():
        print("\n❌ Конфигурация неверна! Исправьте ошибки и попробуйте снова.")
        return
    
    print()
    
    # Тест OpenRouter сервисов
    asyncio.run(test_openrouter_services())
    
    print("\n" + "=" * 60)
    print("✨ Тестирование завершено!")
    print("\n📋 Рекомендации:")
    print("1. ✅ Убедитесь, что все API ключи настроены в файле .env")
    print("2. ✅ Проверьте подключение к интернету")
    print("3. ✅ Установите все зависимости: pip install -r requirements_clean.txt")
    print("4. 🚀 Запустите бота: python bot_openrouter.py")
    print("\n🎯 Ваш бот готов к работе в режиме обычного чата!")
    print("💬 Просто напишите сообщение - бот сам поймет, что вам нужно!")
    print("💰 100 бесплатных запросов в день!")

if __name__ == "__main__":
    main()
