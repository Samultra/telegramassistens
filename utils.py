import re
import hashlib
import time
from typing import List, Dict, Any
import json

class MessageUtils:
    """Утилиты для работы с сообщениями"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Очистка текста от лишних символов"""
        if not text:
            return ""
        
        # Убираем лишние пробелы
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Убираем специальные символы Telegram
        text = re.sub(r'[<>]', '', text)
        
        return text
    
    @staticmethod
    def split_long_message(text: str, max_length: int = 4000) -> List[str]:
        """Разбивка длинного сообщения на части"""
        if len(text) <= max_length:
            return [text]
        
        parts = []
        current_part = ""
        
        # Разбиваем по предложениям
        sentences = re.split(r'([.!?]+)', text)
        
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""
            full_sentence = sentence + punctuation
            
            if len(current_part + full_sentence) <= max_length:
                current_part += full_sentence
            else:
                if current_part:
                    parts.append(current_part.strip())
                current_part = full_sentence
        
        if current_part:
            parts.append(current_part.strip())
        
        return parts
    
    @staticmethod
    def extract_code_blocks(text: str) -> List[str]:
        """Извлечение блоков кода из текста"""
        code_pattern = r'```(?:\w+)?\n(.*?)\n```'
        matches = re.findall(code_pattern, text, re.DOTALL)
        return [match.strip() for match in matches]
    
    @staticmethod
    def format_code_block(code: str, language: str = "python") -> str:
        """Форматирование блока кода для Telegram"""
        return f"```{language}\n{code}\n```"

class UserManager:
    """Управление пользователями"""
    
    def __init__(self):
        self.users: Dict[int, Dict[str, Any]] = {}
        self.user_stats: Dict[int, Dict[str, int]] = {}
    
    def add_user(self, user_id: int, user_info: Dict[str, Any]) -> None:
        """Добавление нового пользователя"""
        if user_id not in self.users:
            self.users[user_id] = {
                'id': user_id,
                'first_name': user_info.get('first_name', ''),
                'last_name': user_info.get('last_name', ''),
                'username': user_info.get('username', ''),
                'joined_at': time.time(),
                'last_activity': time.time()
            }
            
            self.user_stats[user_id] = {
                'messages_sent': 0,
                'commands_used': 0,
                'images_generated': 0,
                'code_generated': 0
            }
    
    def update_user_activity(self, user_id: int) -> None:
        """Обновление активности пользователя"""
        if user_id in self.users:
            self.users[user_id]['last_activity'] = time.time()
    
    def increment_stat(self, user_id: int, stat_name: str) -> None:
        """Увеличение статистики пользователя"""
        if user_id in self.user_stats and stat_name in self.user_stats[user_id]:
            self.user_stats[user_id][stat_name] += 1
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Получение статистики пользователя"""
        if user_id in self.user_stats:
            return self.user_stats[user_id].copy()
        return {}
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Получение общей статистики"""
        total_users = len(self.users)
        total_messages = sum(stats.get('messages_sent', 0) for stats in self.user_stats.values())
        total_commands = sum(stats.get('commands_used', 0) for stats in self.user_stats.values())
        total_images = sum(stats.get('images_generated', 0) for stats in self.user_stats.values())
        total_code = sum(stats.get('code_generated', 0) for stats in self.user_stats.values())
        
        return {
            'total_users': total_users,
            'total_messages': total_messages,
            'total_commands': total_commands,
            'total_images': total_images,
            'total_code': total_code
        }

class RateLimiter:
    """Ограничитель частоты запросов"""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[int, List[float]] = {}
    
    def is_allowed(self, user_id: int) -> bool:
        """Проверка, разрешен ли запрос"""
        current_time = time.time()
        
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Убираем старые запросы
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time < self.time_window
        ]
        
        # Проверяем лимит
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        # Добавляем текущий запрос
        self.requests[user_id].append(current_time)
        return True
    
    def get_remaining_requests(self, user_id: int) -> int:
        """Получение количества оставшихся запросов"""
        current_time = time.time()
        
        if user_id not in self.requests:
            return self.max_requests
        
        # Убираем старые запросы
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time < self.time_window
        ]
        
        return max(0, self.max_requests - len(self.requests[user_id]))

class Cache:
    """Простой кэш для хранения данных"""
    
    def __init__(self, max_size: int = 100, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def set(self, key: str, value: Any) -> None:
        """Установка значения в кэш"""
        if len(self.cache) >= self.max_size:
            # Убираем самый старый элемент
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
    
    def get(self, key: str) -> Any:
        """Получение значения из кэша"""
        if key not in self.cache:
            return None
        
        item = self.cache[key]
        
        # Проверяем TTL
        if time.time() - item['timestamp'] > self.ttl:
            del self.cache[key]
            return None
        
        return item['value']
    
    def clear(self) -> None:
        """Очистка кэша"""
        self.cache.clear()
    
    def size(self) -> int:
        """Размер кэша"""
        return len(self.cache)

class Logger:
    """Простой логгер"""
    
    def __init__(self, log_file: str = "bot.log"):
        self.log_file = log_file
    
    def log(self, level: str, message: str, user_id: int = None) -> None:
        """Запись лога"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        user_info = f" [User: {user_id}]" if user_id else ""
        log_entry = f"[{timestamp}] {level.upper()}{user_info}: {message}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Ошибка записи лога: {e}")
    
    def info(self, message: str, user_id: int = None) -> None:
        """Информационное сообщение"""
        self.log("INFO", message, user_id)
    
    def warning(self, message: str, user_id: int = None) -> None:
        """Предупреждение"""
        self.log("WARNING", message, user_id)
    
    def error(self, message: str, user_id: int = None) -> None:
        """Ошибка"""
        self.log("ERROR", message, user_id)
    
    def debug(self, message: str, user_id: int = None) -> None:
        """Отладочная информация"""
        self.log("DEBUG", message, user_id)
