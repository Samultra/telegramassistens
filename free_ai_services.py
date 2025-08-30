import requests
import json
import os
from typing import Optional, Dict, Any
import time

class FreeAIServices:
    """Бесплатные ИИ сервисы для Telegram бота"""
    
    def __init__(self):
        self.huggingface_token = os.getenv('HUGGINGFACE_TOKEN')
        self.replicate_token = os.getenv('REPLICATE_TOKEN')
        self.cohere_token = os.getenv('COHERE_TOKEN')
        
        # Счетчики для бесплатных лимитов
        self.request_counts = {
            'huggingface': 0,
            'replicate': 0,
            'cohere': 0
        }
        self.last_reset = time.time()
        
        # Доступные модели Hugging Face
        self.available_models = {
            'deepseek': 'deepseek-ai/deepseek-coder-6.7b-instruct',
            'codellama': 'codellama/CodeLlama-7b-Instruct-hf',
            'wizardcoder': 'WizardLM/WizardCoder-15B-V1.0',
            'phind': 'microsoft/Phind-CodeLlama-34B-v2',
            'chat': 'microsoft/DialoGPT-medium',
            'text': 'gpt2',
            'image': 'stabilityai/stable-diffusion-2-1'
        }
    
    def _check_monthly_limit(self, service: str) -> bool:
        """Проверка месячного лимита запросов"""
        current_time = time.time()
        
        # Сброс счетчика каждый месяц
        if current_time - self.last_reset > 30 * 24 * 3600:
            self.request_counts = {k: 0 for k in self.request_counts}
            self.last_reset = current_time
        
        limits = {
            'huggingface': 30000,
            'replicate': 500,
            'cohere': 1000
        }
        
        return self.request_counts[service] < limits.get(service, 0)
    
    def _increment_counter(self, service: str):
        """Увеличение счетчика запросов"""
        if service in self.request_counts:
            self.request_counts[service] += 1
    
    async def generate_text_response(self, prompt: str, max_length: int = 500, model_type: str = 'auto') -> str:
        """Генерация текстового ответа через бесплатные сервисы"""
        
        # Попробуем Hugging Face (самый щедрый)
        if self.huggingface_token and self._check_monthly_limit('huggingface'):
            try:
                # Выбираем модель в зависимости от типа запроса
                model = self._select_model_for_task(prompt, model_type)
                response = self._huggingface_text_generation(prompt, max_length, model)
                if response:
                    self._increment_counter('huggingface')
                    return response
            except Exception as e:
                print(f"Hugging Face ошибка: {e}")
        
        # Попробуем Cohere
        if self.cohere_token and self._check_monthly_limit('cohere'):
            try:
                response = self._cohere_text_generation(prompt, max_length)
                if response:
                    self._increment_counter('cohere')
                    return response
            except Exception as e:
                print(f"Cohere ошибка: {e}")
        
        # Fallback - простые правила
        return self._simple_ai_response(prompt)
    
    def _select_model_for_task(self, prompt: str, model_type: str = 'auto') -> str:
        """Выбор оптимальной модели для задачи"""
        prompt_lower = prompt.lower()
        
        if model_type == 'deepseek' or 'код' in prompt_lower or 'программа' in prompt_lower:
            return self.available_models['deepseek']
        elif model_type == 'codellama' or 'функция' in prompt_lower or 'алгоритм' in prompt_lower:
            return self.available_models['codellama']
        elif model_type == 'wizardcoder' or 'разработка' in prompt_lower:
            return self.available_models['wizardcoder']
        elif model_type == 'phind' or 'оптимизация' in prompt_lower:
            return self.available_models['phind']
        elif 'чат' in prompt_lower or 'общение' in prompt_lower:
            return self.available_models['chat']
        else:
            return self.available_models['deepseek']  # По умолчанию DeepSeek
    
    def _huggingface_text_generation(self, prompt: str, max_length: int, model: str = None) -> Optional[str]:
        """Генерация текста через Hugging Face API"""
        try:
            if not model:
                model = self.available_models['deepseek']
            
            url = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {self.huggingface_token}"}
            
            # Специальные параметры для разных моделей
            if 'deepseek' in model:
                # DeepSeek требует специальный формат
                formatted_prompt = f"<|begin_of_sentence|>User: {prompt}<|end_of_sentence|>\n<|begin_of_sentence|>Assistant: "
                payload = {
                    "inputs": formatted_prompt,
                    "parameters": {
                        "max_new_tokens": max_length,
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "do_sample": True,
                        "repetition_penalty": 1.1
                    }
                }
            elif 'codellama' in model:
                # CodeLlama формат
                formatted_prompt = f"[INST] {prompt} [/INST]"
                payload = {
                    "inputs": formatted_prompt,
                    "parameters": {
                        "max_new_tokens": max_length,
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "do_sample": True
                    }
                }
            else:
                # Стандартный формат
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_length": max_length,
                        "temperature": 0.7,
                        "num_return_sequences": 1
                    }
                }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    
                    # Очистка ответа для DeepSeek
                    if 'deepseek' in model:
                        # Убираем промпт из ответа
                        if formatted_prompt in generated_text:
                            generated_text = generated_text.split(formatted_prompt)[-1]
                        # Убираем теги
                        generated_text = generated_text.replace('<|end_of_sentence|>', '').strip()
                    
                    return generated_text
                return str(result)
            else:
                print(f"Hugging Face API ошибка: {response.status_code} для модели {model}")
                return None
                
        except Exception as e:
            print(f"Ошибка Hugging Face: {e}")
            return None
    
    def _cohere_text_generation(self, prompt: str, max_length: int) -> Optional[str]:
        """Генерация текста через Cohere API"""
        try:
            url = "https://api.cohere.ai/v1/generate"
            headers = {
                "Authorization": f"Bearer {self.cohere_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "command-light",
                "prompt": prompt,
                "max_tokens": max_length,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('generations', [{}])[0].get('text', '')
            else:
                print(f"Cohere API ошибка: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Ошибка Cohere: {e}")
            return None
    
    def _simple_ai_response(self, prompt: str) -> str:
        """Простые ИИ ответы без API"""
        prompt_lower = prompt.lower()
        
        # Простые правила для базовых ответов
        if any(word in prompt_lower for word in ['привет', 'здравствуй', 'hi', 'hello']):
            return "Привет! Я ваш ИИ ассистент. Чем могу помочь?"
        
        elif any(word in prompt_lower for word in ['как дела', 'как ты', 'how are you']):
            return "Спасибо, у меня всё отлично! Готов помогать вам с задачами."
        
        elif any(word in prompt_lower for word in ['спасибо', 'благодарю', 'thanks', 'thank you']):
            return "Пожалуйста! Рад был помочь. Обращайтесь ещё!"
        
        elif any(word in prompt_lower for word in ['код', 'программа', 'функция']):
            return "Я могу помочь с генерацией кода! Используйте команду /code <описание> для получения кода."
        
        elif any(word in prompt_lower for word in ['задача', 'решить', 'уравнение']):
            return "Я могу решать задачи! Используйте команду /solve <задача> для получения решения."
        
        elif any(word in prompt_lower for word in ['информация', 'найти', 'что такое']):
            return "Я могу искать информацию! Используйте команду /search <запрос> для поиска."
        
        elif any(word in prompt_lower for word in ['картинка', 'изображение', 'рисунок']):
            return "Я могу создавать изображения! Используйте команду /image <описание> для генерации."
        
        else:
            return "Интересный вопрос! Я - ИИ ассистент, который может помочь с кодом, задачами, поиском информации и созданием изображений. Попробуйте использовать команды /code, /solve, /search или /image!"
    
    async def generate_code(self, description: str, model_type: str = 'deepseek') -> str:
        """Генерация кода через бесплатные сервисы"""
        prompt = f"Напиши код на Python для следующей задачи: {description}. Код должен быть рабочим и содержать комментарии."
        
        # Попробуем Hugging Face с выбранной моделью
        if self.huggingface_token and self._check_monthly_limit('huggingface'):
            try:
                response = self._huggingface_code_generation(prompt, model_type)
                if response:
                    self._increment_counter('huggingface')
                    return response
            except Exception as e:
                print(f"Ошибка генерации кода: {e}")
        
        # Fallback - простые примеры кода
        return self._simple_code_examples(description)
    
    def _huggingface_code_generation(self, prompt: str, model_type: str = 'deepseek') -> Optional[str]:
        """Генерация кода через Hugging Face"""
        try:
            # Выбираем модель для генерации кода
            if model_type == 'deepseek':
                model = self.available_models['deepseek']
            elif model_type == 'codellama':
                model = self.available_models['codellama']
            elif model_type == 'wizardcoder':
                model = self.available_models['wizardcoder']
            elif model_type == 'phind':
                model = self.available_models['phind']
            else:
                model = self.available_models['deepseek']
            
            url = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {self.huggingface_token}"}
            
            # Специальный формат для генерации кода
            if 'deepseek' in model:
                formatted_prompt = f"<|begin_of_sentence|>User: {prompt}<|end_of_sentence|>\n<|begin_of_sentence|>Assistant: "
                payload = {
                    "inputs": formatted_prompt,
                    "parameters": {
                        "max_new_tokens": 1000,
                        "temperature": 0.2,  # Низкая температура для точного кода
                        "top_p": 0.95,
                        "do_sample": True,
                        "repetition_penalty": 1.1
                    }
                }
            elif 'codellama' in model:
                formatted_prompt = f"[INST] {prompt} [/INST]"
                payload = {
                    "inputs": formatted_prompt,
                    "parameters": {
                        "max_new_tokens": 1000,
                        "temperature": 0.2,
                        "top_p": 0.9,
                        "do_sample": True
                    }
                }
            else:
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 1000,
                        "temperature": 0.3,
                        "num_return_sequences": 1
                    }
                }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    
                    # Очистка ответа
                    if 'deepseek' in model:
                        if formatted_prompt in generated_text:
                            generated_text = generated_text.split(formatted_prompt)[-1]
                        generated_text = generated_text.replace('<|end_of_sentence|>', '').strip()
                    
                    return generated_text
                return str(result)
            else:
                print(f"Ошибка генерации кода: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Ошибка генерации кода: {e}")
            return None
    
    def _simple_code_examples(self, description: str) -> str:
        """Простые примеры кода без API"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['сортировка', 'sort', 'сортировать']):
            return '''```python
def sort_list(numbers):
    """
    Сортирует список чисел по возрастанию
    """
    return sorted(numbers)

# Пример использования
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_numbers = sort_list(numbers)
print(f"Исходный список: {numbers}")
print(f"Отсортированный список: {sorted_numbers}")
```'''
        
        elif any(word in description_lower for word in ['факториал', 'factorial']):
            return '''```python
def factorial(n):
    """
    Вычисляет факториал числа n
    """
    if n < 0:
        return "Факториал отрицательного числа не определен"
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

# Пример использования
n = 5
result = factorial(n)
print(f"Факториал {n} = {result}")
```'''
        
        elif any(word in description_lower for word in ['фибоначчи', 'fibonacci']):
            return '''```python
def fibonacci(n):
    """
    Вычисляет n-ое число Фибоначчи
    """
    if n <= 0:
        return "Введите положительное число"
    elif n == 1 or n == 2:
        return 1
    else:
        a, b = 1, 1
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b

# Пример использования
n = 10
result = fibonacci(n)
print(f"Число Фибоначчи под номером {n} = {result}")
```'''
        
        else:
            return '''```python
def example_function(description):
    """
    Пример функции на Python
    """
    print(f"Описание задачи: {description}")
    print("Это базовая функция. Для более сложного кода используйте платные API.")
    return "Функция выполнена"

# Пример использования
result = example_function("ваша задача")
print(result)
```'''
    
    async def generate_image(self, prompt: str) -> Optional[bytes]:
        """Генерация изображения через бесплатные сервисы"""
        
        # Попробуем Hugging Face Stable Diffusion
        if self.huggingface_token and self._check_monthly_limit('huggingface'):
            try:
                response = self._huggingface_image_generation(prompt)
                if response:
                    self._increment_counter('huggingface')
                    return response
            except Exception as e:
                print(f"Ошибка генерации изображения: {e}")
        
        # Попробуем Replicate
        if self.replicate_token and self._check_monthly_limit('replicate'):
            try:
                response = self._replicate_image_generation(prompt)
                if response:
                    self._increment_counter('replicate')
                    return response
            except Exception as e:
                print(f"Ошибка Replicate: {e}")
        
        return None
    
    async def chat_response(self, message: str, conversation_history: list = None, model_type: str = 'deepseek') -> str:
        """Генерация ответа для чата с учетом истории"""
        try:
            # Формируем контекст с историей
            if conversation_history and len(conversation_history) > 0:
                # Берем последние 5 сообщений для контекста
                recent_history = conversation_history[-5:]
                context = "\n".join([f"User: {msg}" for msg in recent_history])
                full_prompt = f"{context}\nUser: {message}\nAssistant:"
            else:
                full_prompt = f"User: {message}\nAssistant:"
            
            # Генерируем ответ через выбранную модель
            response = await self.generate_text_response(full_prompt, max_length=500, model_type=model_type)
            
            if response:
                return response
            else:
                return "Извините, не удалось сгенерировать ответ. Попробуйте переформулировать вопрос."
                
        except Exception as e:
            print(f"Ошибка в чате: {e}")
            return "Произошла ошибка при обработке сообщения. Попробуйте позже."
    
    def _huggingface_image_generation(self, prompt: str) -> Optional[bytes]:
        """Генерация изображения через Hugging Face"""
        try:
            url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
            headers = {"Authorization": f"Bearer {self.huggingface_token}"}
            
            payload = {"inputs": prompt}
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"Hugging Face изображение ошибка: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Ошибка Hugging Face изображения: {e}")
            return None
    
    def _replicate_image_generation(self, prompt: str) -> Optional[bytes]:
        """Генерация изображения через Replicate"""
        try:
            url = "https://api.replicate.com/v1/predictions"
            headers = {
                "Authorization": f"Token {self.replicate_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "version": "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                "input": {"prompt": prompt}
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 201:
                # Replicate работает асинхронно, нужно ждать
                prediction_id = response.json()['id']
                return self._wait_for_replicate_result(prediction_id)
            else:
                print(f"Replicate ошибка: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Ошибка Replicate: {e}")
            return None
    
    def _wait_for_replicate_result(self, prediction_id: str) -> Optional[bytes]:
        """Ожидание результата от Replicate"""
        try:
            url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
            headers = {"Authorization": f"Token {self.replicate_token}"}
            
            for _ in range(30):  # Ждем максимум 30 секунд
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    status = result.get('status')
                    
                    if status == 'succeeded':
                        image_url = result.get('output', [None])[0]
                        if image_url:
                            img_response = requests.get(image_url, timeout=30)
                            if img_response.status_code == 200:
                                return img_response.content
                        break
                    elif status == 'failed':
                        print("Replicate генерация изображения не удалась")
                        break
                
                time.sleep(1)  # Ждем 1 секунду перед следующей проверкой
            
            return None
            
        except Exception as e:
            print(f"Ошибка ожидания Replicate: {e}")
            return None
    
    def get_available_models(self) -> Dict[str, str]:
        """Получение списка доступных моделей"""
        return self.available_models.copy()
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Получение статистики использования"""
        return {
            'huggingface_used': self.request_counts['huggingface'],
            'replicate_used': self.request_counts['replicate'],
            'cohere_used': self.request_counts['cohere'],
            'huggingface_limit': 30000,
            'replicate_limit': 500,
            'cohere_limit': 1000,
            'available_models': list(self.available_models.keys())
        }
