#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_both_apis():
    """Тест Friendli.ai API - оба варианта"""
    print("🔍 Тестирование Friendli.ai API (оба варианта)...")
    print("-" * 50)
    
    # Получаем API ключ
    api_key = os.getenv('FRIENDLI_API_KEY')
    if not api_key:
        print("❌ FRIENDLI_API_KEY не найден в .env файле")
        return
    
    print(f"🔑 API ключ: {api_key[:10]}...{api_key[-4:]}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Тест 1: Dedicated Endpoint с Endpoint ID
    print("\n" + "="*50)
    print("🧪 ТЕСТ 1: Dedicated Endpoint с Endpoint ID")
    print("="*50)
    
    dedicated_urls = [
        "https://api.friendli.ai/dedicated/depvrmat8854w9c/v1/models",
        "https://api.friendli.ai/dedicated/depvrmat8854w9c/v1/chat/completions"
    ]
    
    for url in dedicated_urls:
        print(f"\n🌐 Тестирую: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"📊 Статус: {response.status_code}")
            print(f"📄 Ответ: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ УСПЕХ! Dedicated endpoint работает!")
            elif response.status_code == 401:
                print("❌ Ошибка авторизации")
            elif response.status_code == 404:
                print("❌ Endpoint не найден - возможно, неверный Endpoint ID")
            else:
                print(f"⚠️ Неожиданный статус: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка подключения: {e}")
    
    # Тест 2: Обычный API без Endpoint ID
    print("\n" + "="*50)
    print("🧪 ТЕСТ 2: Обычный API без Endpoint ID")
    print("="*50)
    
    regular_urls = [
        "https://api.friendli.ai/v1/models",
        "https://api.friendli.ai/v1/chat/completions"
    ]
    
    for url in regular_urls:
        print(f"\n🌐 Тестирую: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"📊 Статус: {response.status_code}")
            print(f"📄 Ответ: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ УСПЕХ! Обычный API работает!")
            elif response.status_code == 401:
                print("❌ Ошибка авторизации")
            elif response.status_code == 404:
                print("❌ Endpoint не найден")
            else:
                print(f"⚠️ Неожиданный статус: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка подключения: {e}")
    
    # Тест POST запроса для работающего варианта
    print("\n" + "="*50)
    print("🧪 ТЕСТ 3: POST запрос")
    print("="*50)
    
    test_payload = {
        "model": "qwen3-highlights",
        "messages": [
            {"role": "user", "content": "Привет! Как дела?"}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    # Пробуем оба варианта для POST
    post_urls = [
        "https://api.friendli.ai/dedicated/depvrmat8854w9c/v1/chat/completions",
        "https://api.friendli.ai/v1/chat/completions"
    ]
    
    for url in post_urls:
        print(f"\n📝 POST тест: {url}")
        try:
            response = requests.post(url, headers=headers, json=test_payload, timeout=30)
            print(f"📊 Статус: {response.status_code}")
            print(f"📄 Ответ: {response.text[:300]}...")
            
            if response.status_code == 200:
                print("✅ POST запрос успешен!")
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    print(f"🤖 Ответ модели: {content}")
            elif response.status_code == 400:
                print("❌ Ошибка в запросе - проверьте параметры")
            elif response.status_code == 401:
                print("❌ Ошибка авторизации")
            else:
                print(f"⚠️ Неожиданный статус: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка POST запроса: {e}")

def main():
    print("🚀 Тест Friendli.ai API - оба варианта")
    print("=" * 60)
    
    test_both_apis()
    
    print("\n" + "=" * 60)
    print("📋 РЕЗУЛЬТАТ:")
    print("✅ Если Dedicated Endpoint работает - используйте Endpoint ID")
    print("✅ Если обычный API работает - не нужен Endpoint ID")
    print("❌ Если оба не работают - проверьте API ключ и аккаунт")

if __name__ == "__main__":
    main()
