import requests
import json
from config import HUGGINGFACE_TOKEN

class HuggingFaceClient:
    """Клиент для работы с Hugging Face API"""
    
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co"
        self.headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"} if HUGGINGFACE_TOKEN else {}
    
    def text_generation(self, prompt, model="microsoft/DialoGPT-medium", max_length=100):
        """Генерация текста с помощью Hugging Face API"""
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": max_length,
                    "temperature": 0.7,
                    "num_return_sequences": 1
                }
            }
            
            response = requests.post(
                f"{self.api_url}/models/{model}",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '')
                return str(result)
            else:
                print(f"Ошибка API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Ошибка при генерации текста: {e}")
            return None
    
    def image_generation(self, prompt, model="stabilityai/stable-diffusion-2-1"):
        """Генерация изображения с помощью Hugging Face API"""
        try:
            payload = {"inputs": prompt}
            
            response = requests.post(
                f"{self.api_url}/models/{model}",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"Ошибка API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Ошибка при генерации изображения: {e}")
            return None
    
    def text_classification(self, text, model="distilbert-base-uncased-finetuned-sst-2-english"):
        """Классификация текста"""
        try:
            payload = {"inputs": text}
            
            response = requests.post(
                f"{self.api_url}/models/{model}",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Ошибка при классификации текста: {e}")
            return None
    
    def translation(self, text, target_language="en", source_language="auto"):
        """Перевод текста"""
        try:
            model = f"Helsinki-NLP/opus-mt-{source_language}-{target_language}"
            payload = {"inputs": text}
            
            response = requests.post(
                f"{self.api_url}/models/{model}",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('translation_text', '')
                return str(result)
            else:
                print(f"Ошибка API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Ошибка при переводе: {e}")
            return None
    
    def sentiment_analysis(self, text):
        """Анализ тональности текста"""
        return self.text_classification(text, "cardiffnlp/twitter-roberta-base-sentiment-latest")
    
    def summarize_text(self, text, model="facebook/bart-large-cnn"):
        """Суммаризация текста"""
        try:
            payload = {"inputs": text}
            
            response = requests.post(
                f"{self.api_url}/models/{model}",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('summary_text', '')
                return str(result)
            else:
                print(f"Ошибка API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Ошибка при суммаризации: {e}")
            return None
    
    def get_available_models(self, task=None):
        """Получение списка доступных моделей"""
        try:
            url = f"{self.api_url}/models"
            if task:
                url += f"?search={task}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                models = response.json()
                return [model['id'] for model in models[:10]]  # Первые 10 моделей
            else:
                print(f"Ошибка API: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Ошибка при получении моделей: {e}")
            return []
    
    def test_connection(self):
        """Тестирование подключения к API"""
        try:
            response = requests.get(f"{self.api_url}/models", headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
