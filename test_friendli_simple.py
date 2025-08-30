#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_friendli_api():
    """Простой тест Friendli.ai API"""
    print("🔍 Тестирование Friendli.ai API...")
    print("-" * 40)
    
    # Получаем API ключ
    api_key = os.getenv('FRIENDLI_API_KEY')
    if not api_key:
        print("❌ FRIENDLI_API_KEY не найден в .env файле")
        return
    
    print(f"🔑 API ключ: {api_key[:10]}...{api_key[-4:]}")
    
    # Тестируем разные URL с правильным endpoint ID
    urls_to_test = [
        "https://api.friendli.ai/dedicated/depvrmat8854w9c/v1/models",
        "https://api.friendli.ai/dedicated/depvrmat8854w9c/v1/chat/completions",
        "https://api.friendli.ai/dedicated/v1/models"  # Без endpoint ID для сравнения
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for url in urls_to_test:
        print(f"\n🌐 Тестирую URL: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"📊 Статус: {response.status_code}")
            print(f"📄 Ответ: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ Успешное подключение!")
            elif response.status_code == 401:
                print("❌ Ошибка авторизации - проверьте API ключ")
            elif response.status_code == 404:
                print("❌ URL не найден - проверьте endpoint")
            else:
                print(f"⚠️ Неожиданный статус: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка подключения: {e}")
    
    # Тест POST запроса
    print(f"\n📝 Тест POST запроса...")
    test_url = "https://api.friendli.ai/dedicated/depvrmat8854w9c/v1/chat/completions"
    
    test_payload = {
        "model": "qwen3-highlights",
        "messages": [
            {"role": "user", "content": "Привет! Как дела?"}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(test_url, headers=headers, json=test_payload, timeout=30)
        print(f"📊 POST статус: {response.status_code}")
        print(f"📄 POST ответ: {response.text[:300]}...")
        
        if response.status_code == 200:
            print("✅ POST запрос успешен!")
        elif response.status_code == 400:
            print("❌ Ошибка в запросе - проверьте параметры")
        elif response.status_code == 401:
            print("❌ Ошибка авторизации")
        else:
            print(f"⚠️ Неожиданный статус POST: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка POST запроса: {e}")

def check_env_file():
    """Проверка .env файла"""
    print("\n🔧 Проверка .env файла...")
    print("-" * 30)
    
    env_path = ".env"
    if os.path.exists(env_path):
        print(f"✅ Файл {env_path} найден")
        
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'FRIENDLI_API_KEY' in content:
            print("✅ FRIENDLI_API_KEY найден в .env")
        else:
            print("❌ FRIENDLI_API_KEY НЕ найден в .env")
            
        if 'TELEGRAM_TOKEN' in content:
            print("✅ TELEGRAM_TOKEN найден в .env")
        else:
            print("❌ TELEGRAM_TOKEN НЕ найден в .env")
    else:
        print(f"❌ Файл {env_path} НЕ найден")
        print("📝 Создайте .env файл на основе env_friendli.txt")

def main():
    print("🚀 Простой тест Friendli.ai API")
    print("=" * 50)
    
    check_env_file()
    test_friendli_api()
    
    print("\n" + "=" * 50)
    print("📋 Рекомендации:")
    print("1. ✅ Проверьте правильность API ключа")
    print("2. ✅ Убедитесь, что ключ активен на Friendli.ai")
    print("3. ✅ Проверьте endpoint URL")
    print("4. ✅ Убедитесь в правильности модели")
    print("5. 🔍 Проверьте логи ошибок выше")

if __name__ == "__main__":
    main()
