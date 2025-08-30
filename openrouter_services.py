import requests
import json
import os
from typing import Optional, Dict, Any
import time

class OpenRouterServices:
    """OpenRouter API сервисы для Telegram бота с настоящим DeepSeek"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        
        # Доступные модели OpenRouter (правильные ID)
        self.available_models = {
            'deepseek': 'deepseek/deepseek-chat-v3.1:free',  # Бесплатная модель DeepSeek
            'deepseek_large': 'deepseek/deepseek-chat-v3.1',  # Платная модель DeepSeek
            'deepseek_coder': 'deepseek/deepseek-coder-6.7b-instruct',  # Кодовая модель
            'codellama': 'alfredpros/codellama-7b-instruct-solidity',  # CodeLlama для Solidity
            'claude': 'anthropic/claude-3.5-haiku',  # Claude Haiku
            'gpt': 'openai/gpt-3.5-turbo',  # GPT-3.5
            'gpt4': 'openai/gpt-4o-mini',  # GPT-4
            'gemini': 'google/gemini-2.5-flash',  # Gemini Flash
            'llama': 'meta-llama/llama-3.1-8b-instruct:free'  # Бесплатная Llama
        }
        
        # Счетчики для бесплатных лимитов
        self.request_counts = {
            'free_models': 0,
            'paid_models': 0
        }
        self.last_reset = time.time()
        
        # Лимиты OpenRouter
        self.daily_limits = {
            'free_models': 100,  # 100 запросов в день бесплатно
            'paid_models': 1000  # 1000 запросов в день для платных
        }
    
    def _check_daily_limit(self, model_type: str = 'free') -> bool:
        """Проверка дневного лимита запросов"""
        current_time = time.time()
        
        # Сброс счетчика каждый день
        if current_time - self.last_reset > 24 * 3600:
            self.request_counts = {'free_models': 0, 'paid_models': 0}
            self.last_reset = current_time
        
        if model_type == 'free':
            return self.request_counts['free_models'] < self.daily_limits['free_models']
        else:
            return self.request_counts['paid_models'] < self.daily_limits['paid_models']
    
    def _increment_counter(self, model_type: str = 'free'):
        """Увеличение счетчика запросов"""
        if model_type == 'free':
            self.request_counts['free_models'] += 1
        else:
            self.request_counts['paid_models'] += 1
    
    def _is_free_model(self, model: str) -> bool:
        """Проверка, является ли модель бесплатной"""
        free_models = [
            'deepseek/deepseek-chat-v3.1:free',
            'meta-llama/llama-3.1-8b-instruct:free',
            'meta-llama/llama-3.1-405b-instruct:free',
            'meta-llama/llama-3.3-8b-instruct:free',
            'meta-llama/llama-3.3-70b-instruct:free',
            'meta-llama/llama-4-maverick:free',
            'meta-llama/llama-4-scout:free',
            'nvidia/llama-3.1-nemotron-ultra-253b-v1:free',
            'deepseek/deepseek-r1:free',
            'deepseek/deepseek-r1-0528:free',
            'deepseek/deepseek-r1-0528-qwen3-8b:free',
            'deepseek/deepseek-r1-distill-qwen-14b:free',
            'deepseek/deepseek-r1-distill-llama-70b:free',
            'deepseek/deepseek-chat-v3-0324:free',
            'tngtech/deepseek-r1t2-chimera:free',
            'tngtech/deepseek-r1t-chimera:free',
            'google/gemini-2.5-flash-lite',
            'google/gemini-2.0-flash-exp:free',
            'nousresearch/deephermes-3-llama-3-8b-preview:free',
            'openai/gpt-oss-120b:free',
            'openai/gpt-oss-20b:free',
            'shisa-ai/shisa-v2-llama3.3-70b:free',
            'nvidia/llama-3.1-nemotron-ultra-253b-v1:free'
        ]
        return model in free_models
    
    async def generate_text_response(self, prompt: str, max_tokens: int = 1000, model: str = 'deepseek') -> str:
        """Генерация текстового ответа через OpenRouter API"""
        
        if not self.api_key:
            return "❌ OpenRouter API ключ не настроен. Добавьте OPENROUTER_API_KEY в .env файл."
        
        # Выбираем модель
        model_id = self.available_models.get(model, self.available_models['deepseek'])
        is_free = self._is_free_model(model_id)
        
        # Проверяем лимиты
        if not self._check_daily_limit('free' if is_free else 'paid'):
            return f"❌ Достигнут дневной лимит для {'бесплатных' if is_free else 'платных'} моделей. Попробуйте завтра."
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-repo",  # Замените на ваш репозиторий
                "X-Title": "Telegram AI Bot"
            }
            
            payload = {
                "model": model_id,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.95
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Увеличиваем счетчик
                self._increment_counter('free' if is_free else 'paid')
                
                return content
            else:
                error_msg = f"OpenRouter API ошибка: {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('error', {}).get('message', '')}"
                    except:
                        error_msg += f" - {response.text[:100]}"
                
                return f"❌ {error_msg}"
                
        except Exception as e:
            return f"❌ Ошибка при обращении к OpenRouter: {str(e)}"
    
    async def generate_code(self, description: str, model: str = 'deepseek') -> str:
        """Генерация кода через OpenRouter API"""
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

        return await self.generate_text_response(prompt, max_tokens=2000, model=model)
    
    async def solve_problem(self, problem: str, model: str = 'deepseek') -> str:
        """Решение задач через OpenRouter API"""
        prompt = f"""Реши следующую задачу: {problem}

Требования к ответу:
1. Пошаговое решение
2. Объяснение каждого шага
3. Математические выкладки (если применимо)
4. Альтернативные способы решения
5. Практические примеры

Дай подробный, понятный ответ с примерами."""

        return await self.generate_text_response(prompt, max_tokens=1500, model=model)
    
    async def search_information(self, query: str, model: str = 'deepseek') -> str:
        """Поиск информации через OpenRouter API"""
        prompt = f"""Найди и проанализируй информацию по запросу: {query}

Требования к ответу:
1. Подробный анализ темы
2. Актуальная информация
3. Практические примеры
4. Связи с другими концепциями
5. Практическое применение

Предоставь глубокий, информативный ответ."""

        return await self.generate_text_response(prompt, max_tokens=1200, model=model)
    
    async def chat_response(self, message: str, conversation_history: list = None, model: str = 'deepseek') -> str:
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
                return "❌ OpenRouter API ключ не настроен."
            
            # Выбираем модель
            model_id = self.available_models.get(model, self.available_models['deepseek'])
            is_free = self._is_free_model(model_id)
            
            # Проверяем лимиты
            if not self._check_daily_limit('free' if is_free else 'paid'):
                return f"❌ Достигнут дневной лимит для {'бесплатных' if is_free else 'платных'} моделей."
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-repo",
                "X-Title": "Telegram AI Bot"
            }
            
            payload = {
                "model": model_id,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Увеличиваем счетчик
                self._increment_counter('free' if is_free else 'paid')
                
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
            'free_models_used': self.request_counts['free_models'],
            'paid_models_used': self.request_counts['paid_models'],
            'free_models_limit': self.daily_limits['free_models'],
            'paid_models_limit': self.daily_limits['paid_models'],
            'available_models': list(self.available_models.keys()),
            'reset_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.last_reset))
        }
    
    def test_connection(self) -> bool:
        """Тест подключения к OpenRouter API"""
        if not self.api_key:
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(f"{self.base_url}/models", headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
