#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_openrouter_models():
    """Проверка доступных моделей в OpenRouter"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY не найден в .env файле")
        return
    
    print("🔍 Проверяю доступные модели в OpenRouter...")
    print("-" * 50)
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
        
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Получено {len(models.get('data', []))} моделей")
            print()
            
            # Ищем модели DeepSeek
            print("🥇 Модели DeepSeek:")
            deepseek_models = []
            for model in models.get('data', []):
                model_id = model.get('id', '')
                if 'deepseek' in model_id.lower():
                    deepseek_models.append(model_id)
                    print(f"  • {model_id}")
            
            if not deepseek_models:
                print("  ❌ Модели DeepSeek не найдены")
            
            print()
            
            # Ищем модели CodeLlama
            print("🥈 Модели CodeLlama:")
            codellama_models = []
            for model in models.get('data', []):
                model_id = model.get('id', '')
                if 'codellama' in model_id.lower():
                    codellama_models.append(model_id)
                    print(f"  • {model_id}")
            
            if not codellama_models:
                print("  ❌ Модели CodeLlama не найдены")
            
            print()
            
            # Ищем модели WizardCoder
            print("🥉 Модели WizardCoder:")
            wizardcoder_models = []
            for model in models.get('data', []):
                model_id = model.get('id', '')
                if 'wizardcoder' in model_id.lower():
                    wizardcoder_models.append(model_id)
                    print(f"  • {model_id}")
            
            if not wizardcoder_models:
                print("  ❌ Модели WizardCoder не найдены")
            
            print()
            
            # Ищем другие популярные модели
            print("🏅 Другие популярные модели:")
            popular_models = []
            for model in models.get('data', []):
                model_id = model.get('id', '')
                if any(name in model_id.lower() for name in ['claude', 'gpt', 'gemini', 'llama']):
                    popular_models.append(model_id)
                    print(f"  • {model_id}")
            
            if not popular_models:
                print("  ❌ Популярные модели не найдены")
            
            print()
            print("💡 Используйте эти ID в openrouter_services.py")
            
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            print(f"Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check_openrouter_models()
