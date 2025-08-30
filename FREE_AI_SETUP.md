# 🆓 Настройка БЕСПЛАТНЫХ ИИ сервисов

## 🎯 Обзор бесплатных сервисов

| Сервис | Запросов/месяц | Качество | Скорость | Сложность настройки |
|--------|----------------|----------|----------|---------------------|
| **Hugging Face** | 30,000 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Replicate** | 500 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Cohere** | 1,000 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Локальные модели** | ∞ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🚀 1. Hugging Face (Самый щедрый!)

### Регистрация
1. Перейдите на [huggingface.co](https://huggingface.co/)
2. Нажмите "Sign Up" в правом верхнем углу
3. Выберите способ регистрации:
   - **GitHub** (рекомендуется)
   - **Google**
   - **Email**

### Получение API токена
1. Войдите в аккаунт
2. Нажмите на свой аватар → **Settings**
3. В левом меню выберите **Access Tokens**
4. Нажмите **New token**
5. Заполните форму:
   - **Name**: `Telegram Bot`
   - **Role**: `Read` (достаточно)
6. Нажмите **Generate token**
7. **Скопируйте токен** (начинается с `hf_...`)

### Добавление в .env
```bash
HUGGINGFACE_TOKEN=hf_your_actual_token_here
```

## 🎨 2. Replicate (Лучшие изображения!)

### Регистрация
1. Перейдите на [replicate.com](https://replicate.com/)
2. Нажмите **Sign up**
3. Выберите способ:
   - **GitHub** (рекомендуется)
   - **Google**
   - **Email**

### Получение API токена
1. Войдите в аккаунт
2. Нажмите на аватар → **Account**
3. Выберите **API Tokens**
4. Нажмите **Create API token**
5. Дайте название: `Telegram Bot`
6. **Скопируйте токен** (начинается с `r8_...`)

### Добавление в .env
```bash
REPLICATE_TOKEN=r8_your_actual_token_here
```

## 💬 3. Cohere (Хороший текст!)

### Регистрация
1. Перейдите на [cohere.ai](https://cohere.ai/)
2. Нажмите **Get Started**
3. Заполните форму регистрации
4. Подтвердите email

### Получение API ключа
1. Войдите в аккаунт
2. Перейдите в **API Keys**
3. Нажмите **Create API Key**
4. Дайте название: `Telegram Bot`
5. **Скопируйте ключ** (начинается с `...`)

### Добавление в .env
```bash
COHERE_TOKEN=your_actual_cohere_key_here
```

## 🔧 4. Локальные модели (Без интернета!)

### Установка Ollama
```bash
# Windows (с WSL2)
wsl --install
wsl
curl -fsSL https://ollama.ai/install.sh | sh

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

### Загрузка моделей
```bash
# Текстовая модель
ollama pull llama2:7b

# Модель для кода
ollama pull codellama:7b

# Модель для изображений
ollama pull stable-diffusion
```

### Запуск локального сервера
```bash
ollama serve
```

## 📱 5. Пошаговая настройка бота

### Шаг 1: Создайте .env файл
```bash
# Windows
copy env_example.txt .env

# Linux/macOS
cp env_example.txt .env
```

### Шаг 2: Заполните токены
```bash
# Откройте .env в любом редакторе
notepad .env  # Windows
nano .env      # Linux/macOS
```

### Шаг 3: Добавьте ваши токены
```bash
TELEGRAM_TOKEN=you8444005813:AAHWEbsuT4jhavPtjodcIAWepaFhTlPicbg
HUGGINGFACE_TOKEN=hf_your_huggingface_token
REPLICATE_TOKEN=r8_your_replicate_token
COHERE_TOKEN=your_cohere_token
```

### Шаг 4: Тестирование
```bash
python test_bot.py
```

## 🎯 Приоритеты настройки

### 🥇 Первый приоритет: Hugging Face
- **30,000 запросов** - хватит надолго!
- **Простая настройка**
- **Хорошее качество**

### 🥈 Второй приоритет: Cohere
- **1,000 запросов** - для текста
- **Быстрые ответы**
- **Простая настройка**

### 🥉 Третий приоритет: Replicate
- **500 запросов** - для изображений
- **Лучшее качество картинок**
- **Средняя сложность**

## 🚨 Решение проблем

### Hugging Face
- **"Unauthorized"**: Проверьте правильность токена
- **"Model not found"**: Модель недоступна, выберите другую
- **"Rate limit"**: Превышен лимит, подождите

### Replicate
- **"Invalid token"**: Проверьте токен
- **"Quota exceeded"**: Превышен лимит 500/месяц
- **"Model not available"**: Модель временно недоступна

### Cohere
- **"Invalid API key"**: Проверьте ключ
- **"Rate limit"**: Слишком много запросов
- **"Model not found"**: Выберите доступную модель

## 💡 Советы по экономии

### 1. Кэширование ответов
```python
# Сохраняйте часто используемые ответы
cache = {}
if prompt in cache:
    return cache[prompt]
```

### 2. Умное распределение
```python
# Используйте разные сервисы для разных задач
if "код" in prompt:
    return huggingface.generate(prompt)
elif "изображение" in prompt:
    return replicate.generate(prompt)
else:
    return cohere.generate(prompt)
```

### 3. Локальные модели
```python
# Для простых задач используйте локальные модели
if simple_task:
    return local_model.generate(prompt)
```

## 📊 Мониторинг использования

### Проверка лимитов
```bash
python -c "
from free_ai_services import FreeAIServices
ai = FreeAIServices()
stats = ai.get_usage_stats()
print('Использовано:')
print(f'Hugging Face: {stats[\"huggingface_used\"]}/{stats[\"huggingface_limit\"]}')
print(f'Replicate: {stats[\"replicate_used\"]}/{stats[\"replicate_limit\"]}')
print(f'Cohere: {stats[\"cohere_used\"]}/{stats[\"cohere_limit\"]}')
"
```

## 🎉 Результат

После настройки у вас будет:
- **30,000+ запросов в месяц** - полностью бесплатно!
- **Высокое качество** ответов
- **Быстрая работа** бота
- **Никаких платежей**!

## 🔄 Обновление токенов

### Ежемесячно
- Проверяйте лимиты
- Обновляйте токены при необходимости
- Мониторьте качество ответов

### При проблемах
- Создавайте новые токены
- Проверяйте статус сервисов
- Используйте альтернативные модели

---

**🎯 Начните с Hugging Face - это даст вам 30,000 бесплатных запросов в месяц!**
