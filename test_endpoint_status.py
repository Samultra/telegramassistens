#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_endpoint_status():
    """Тест статуса endpoint и диагностика"""
    print("🔍 Диагностика Friendli.ai Endpoint...")
    print("-" * 50)
    
    # Получаем API ключ
    api_key = os.getenv('FRIENDLI_API_KEY')
    if not api_key:
        print("❌ FRIENDLI_API_KEY не найден в .env файле")
        return
    
    print(f"🔑 API ключ: {api_key[:10]}...{api_key[-4:]}")
    print(f"📍 Endpoint ID: depvrmat8854w9c")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Тест 1: Проверка статуса endpoint
    print("\n" + "="*50)
    print("🧪 ТЕСТ 1: Статус Dedicated Endpoint")
    print("="*50)
    
    endpoint_urls = [
        "https://api.friendli.ai/dedicated/depvrmat8854w9c/v1/models",
        "https://api.friendli.ai/dedicated/depvrmat8854w9c/v1/chat/completions"
    ]
    
    for url in endpoint_urls:
        print(f"\n🌐 Тестирую: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            print(f"📊 Статус: {response.status_code}")
            print(f"📄 Ответ: {response.text[:300]}...")
            
            if response.status_code == 200:
                print("✅ Endpoint активен и работает!")
            elif response.status_code == 401:
                print("❌ Ошибка авторизации - проверьте API ключ")
            elif response.status_code == 404:
                print("❌ Endpoint не найден - возможно, неактивен")
            elif response.status_code == 503:
                print("❌ Endpoint недоступен - проверьте статус в аккаунте")
            else:
                print(f"⚠️ Неожиданный статус: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка подключения: {e}")
    
    # Тест 2: Проверка обычного API
    print("\n" + "="*50)
    print("🧪 ТЕСТ 2: Обычный API (fallback)")
    print("="*50)
    
    regular_urls = [
        "https://api.friendli.ai/v1/models",
        "https://api.friendli.ai/v1/chat/completions"
    ]
    
    for url in regular_urls:
        print(f"\n🌐 Тестирую: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            print(f"📊 Статус: {response.status_code}")
            print(f"📄 Ответ: {response.text[:300]}...")
            
            if response.status_code == 200:
                print("✅ Обычный API работает!")
            elif response.status_code == 401:
                print("❌ Ошибка авторизации")
            elif response.status_code == 404:
                print("❌ Endpoint не найден")
            else:
                print(f"⚠️ Неожиданный статус: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка подключения: {e}")
    
    # Тест 3: POST запрос к работающему варианту
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
    
    # Пробуем оба варианта
    post_urls = [
        "https://api.friendli.ai/dedicated/depvrmat8854w9c/v1/chat/completions",
        "https://api.friendli.ai/v1/chat/completions"
    ]
    
    for url in post_urls:
        print(f"\n📝 POST тест: {url}")
        try:
            response = requests.post(url, headers=headers, json=test_payload, timeout=30)
            print(f"📊 Статус: {response.status_code}")
            print(f"📄 Ответ: {response.text[:400]}...")
            
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
            elif response.status_code == 503:
                print("❌ Сервис недоступен - endpoint неактивен")
            else:
                print(f"⚠️ Неожиданный статус: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка POST запроса: {e}")

def main():
    print("🚀 Диагностика Friendli.ai Endpoint")
    print("=" * 60)
    
    test_endpoint_status()
    
    print("\n" + "=" * 60)
    print("📋 РЕКОМЕНДАЦИИ:")
    print("1. 🔧 Активируйте endpoint в аккаунте Friendli.ai")
    print("2. 🔍 Проверьте статус endpoint (должен быть 'Available')")
    print("3. 💳 Убедитесь, что ваш план поддерживает dedicated endpoints")
    print("4. 🔄 Если dedicated не работает, используйте обычный API")
    print("5. 📞 Обратитесь в поддержку Friendli.ai при необходимости")

if __name__ == "__main__":
    main()
