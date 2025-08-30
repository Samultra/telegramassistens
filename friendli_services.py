import requests
import json
import os
from typing import Optional, Dict, Any
import time

class FriendliServices:
    """Friendli.ai API сервисы для Telegram бота с Qwen3 Highlights"""
    
    def __init__(self):
        self.api_key = os.getenv('FRIENDLI_API_KEY')
        self.base_url = "https://api.friendli.ai/dedicated"
        self.endpoint_id = "depvrmat8854w9c"  # Ваш реальный Endpoint ID
        # Формируем полный URL с endpoint ID
        self.full_url = f"{self.base_url}/{self.endpoint_id}"
        
        # Доступные модели Friendli.ai
        self.available_models = {
            'qwen3_highlights': 'Qwen3 Highlights',  # Основная модель
            'qwen3': 'Qwen3',  # Альтернативная модель
            'qwen2': 'Qwen2'   # Базовая модель
        }
        
        # Счетчики для лимитов
        self.request_counts = {
            'qwen3_highlights': 0,
            'total_requests': 0
        }
        self.last_reset = time.time()
        
        # Лимиты Friendli.ai (зависит от вашего плана)
        self.daily_limits = {
            'qwen3_highlights': 1000,  # Примерный лимит
            'total_requests': 5000      # Общий лимит
        }
    
    def _check_daily_limit(self, model_type: str = 'qwen3_highlights') -> bool:
        """Проверка дневного лимита запросов"""
        current_time = time.time()
        
        # Сброс счетчика каждый день
        if current_time - self.last_reset > 24 * 3600:
            self.request_counts = {'qwen3_highlights': 0, 'total_requests': 0}
            self.last_reset = current_time
        
        if model_type == 'qwen3_highlights':
            return self.request_counts['qwen3_highlights'] < self.daily_limits['qwen3_highlights']
        else:
            return self.request_counts['total_requests'] < self.daily_limits['total_requests']
    
    def _increment_counter(self, model_type: str = 'qwen3_highlights'):
        """Увеличение счетчика запросов"""
        if model_type == 'qwen3_highlights':
            self.request_counts['qwen3_highlights'] += 1
        self.request_counts['total_requests'] += 1
    
    async def generate_text_response(self, prompt: str, max_tokens: int = 2000, model: str = 'qwen3_highlights') -> str:
        """Генерация текстового ответа через Friendli.ai API"""
        
        if not self.api_key:
            return "❌ Friendli.ai API ключ не настроен. Добавьте FRIENDLI_API_KEY в .env файл."
        
        # Проверяем лимиты
        if not self._check_daily_limit(model):
            return f"❌ Достигнут дневной лимит для модели {model}. Попробуйте завтра."
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "qwen3-highlights",  # Используем Qwen3 Highlights
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.95,
                "stream": False
            }
            
            response = requests.post(
                f"{self.full_url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Увеличиваем счетчик
                self._increment_counter(model)
                
                return content
            else:
                error_msg = f"Friendli.ai API ошибка: {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('error', {}).get('message', '')}"
                    except:
                        error_msg += f" - {response.text[:100]}"
                
                return f"❌ {error_msg}"
                
        except Exception as e:
            return f"❌ Ошибка при обращении к Friendli.ai: {str(e)}"
    
    async def generate_code(self, description: str, model: str = 'qwen3_highlights') -> str:
        """Генерация кода через Friendli.ai API"""
        prompt = f"""Напиши полноценный, рабочий код на Python для следующей задачи: {description}

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

        return await self.generate_text_response(prompt, max_tokens=3000, model=model)
    
    async def solve_problem(self, problem: str, model: str = 'qwen3_highlights') -> str:
        """Решение задач через Friendli.ai API"""
        prompt = f"""Реши следующую задачу: {problem}

Требования к ответу:
1. Пошаговое решение
2. Объяснение каждого шага
3. Математические выкладки (если применимо)
4. Альтернативные способы решения
5. Практические примеры

Дай подробный, понятный ответ с примерами."""

        return await self.generate_text_response(prompt, max_tokens=2500, model=model)
    
    async def search_information(self, query: str, model: str = 'qwen3_highlights') -> str:
        """Поиск информации через Friendli.ai API"""
        prompt = f"""Найди и проанализируй информацию по запросу: {query}

Требования к ответу:
1. Подробный анализ темы
2. Актуальная информация
3. Практические примеры
4. Связи с другими концепциями
5. Практическое применение

Предоставь глубокий, информативный ответ."""

        return await self.generate_text_response(prompt, max_tokens=2000, model=model)
    
    async def chat_response(self, message: str, conversation_history: list = None, model: str = 'qwen3_highlights') -> str:
        """Генерация ответа для чата с учетом истории"""
        try:
            # Формируем контекст с историей
            messages = []
            
            if conversation_history and len(conversation_history) > 0:
                # Берем последние 5 сообщений для контекста
                recent_history = conversation_history[-5:]
                for msg in recent_history:
                    messages.append({"role": "user", "content": msg})
            
            messages.append({"role": "user", "content": message})
            
            if not self.api_key:
                return "❌ Friendli.ai API ключ не настроен."
            
            # Проверяем лимиты
            if not self._check_daily_limit(model):
                return f"❌ Достигнут дневной лимит для модели {model}."
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "qwen3-highlights",
                "messages": messages,
                "max_tokens": 2000,
                "temperature": 0.7,
                "stream": False
            }
            
            response = requests.post(
                f"{self.full_url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Увеличиваем счетчик
                self._increment_counter(model)
                
                return content
            else:
                return f"❌ Ошибка API: {response.status_code}"
                
        except Exception as e:
            return f"❌ Ошибка в чате: {str(e)}"
    
    def get_available_models(self) -> Dict[str, str]:
        """Получение списка доступных моделей"""
        return self.available_models.copy()
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Получение статистики использования"""
        return {
            'qwen3_highlights_used': self.request_counts['qwen3_highlights'],
            'total_requests_used': self.request_counts['total_requests'],
            'qwen3_highlights_limit': self.daily_limits['qwen3_highlights'],
            'total_requests_limit': self.daily_limits['total_requests'],
            'available_models': list(self.available_models.keys()),
            'reset_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.last_reset))
        }
    
    def test_connection(self) -> bool:
        """Тест подключения к Friendli.ai API"""
        if not self.api_key:
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Тестируем разные endpoints с правильным URL
            test_urls = [
                f"{self.full_url}/v1/models",
                f"{self.full_url}/v1/chat/completions"
            ]
            
            for url in test_urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        return True
                    elif response.status_code == 401:
                        print(f"❌ Ошибка авторизации для {url}")
                    elif response.status_code == 404:
                        print(f"❌ Endpoint не найден: {url}")
                    else:
                        print(f"⚠️ Неожиданный статус {response.status_code} для {url}")
                except requests.exceptions.RequestException as e:
                    print(f"❌ Ошибка подключения к {url}: {e}")
            
            return False
        except Exception as e:
            print(f"❌ Общая ошибка в test_connection: {e}")
            return False
