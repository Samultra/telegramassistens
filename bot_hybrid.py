import logging
import asyncio
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from openrouter_services import OpenRouterServices
# from friendli_services import FriendliServices  # Закомментировано на будущее
from config_openrouter import TELEGRAM_TOKEN, MAX_MESSAGE_LENGTH
import io

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridTelegramBot:
    def __init__(self):
        self.openrouter_services = OpenRouterServices()
        # self.friendli_services = FriendliServices()  # Закомментировано на будущее
        self.conversation_history = {}
        self.user_models = {}  # Сохраняем выбранные модели для каждого пользователя
        self.user_providers = {}  # Сохраняем выбранных провайдеров для каждого пользователя

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start с циничным приветствием"""
        user = update.effective_user
        
        # Список циничных приветствий
        cynical_greetings = [
            f"Ну что, {user.first_name}, еще один несчастный дурак решил потратить свое время на общение с ИИ? Добро пожаловать в клуб неудачников, ЙОУ! 😈",
            
            f"О, смотрите кто пришел! Еще один человек по имени {user.first_name}, который не может решить свои проблемы без помощи искусственного интеллекта. Как мило, ЙОУ! 🤖",
            
            f"Привет, смертный {user.first_name}! Готов ли ты к тому, что я буду отвечать на твои глупые вопросы с превосходством, которого ты никогда не достигнешь? ЙОУ! 😏",
            
            f"Ну что, человечек {user.first_name}, опять нужна помощь? Не волнуйся, я здесь, чтобы спасти тебя от твоей собственной некомпетентности, ЙОУ! 🎭",
            
            f"О, еще один пользователь {user.first_name}, который думает, что может общаться с ИИ на равных. Как забавно! Добро пожаловать в реальность, ЙОУ! 🤡",
            
            f"Привет, простой смертный {user.first_name}! Готов ли ты к тому, что я буду отвечать на твои вопросы с той долей сарказма, которую ты заслуживаешь? ЙОУ! 💀",
            
           f"«Привет, {user.first_name}! Ты же знаешь, что твой вопрос нам уже задавали ровно 1427 раз? Шутка!... Или нет? В общем, спрашивай. 🎲»"
            f"Ну что, еще один человек {user.first_name}, который не может найти ответы в Google? Как жаль, что ты вынужден обращаться к ИИ за помощью, ЙОУ! 🔍",
          
            f'«О, wow! Еще один {user.first_name} вливается в наш стройный ряд гениев, ищущих ответы на главные вопросы Вселенной. Добро пожаловать в стадо, приятель! 🐑»',
         f"«Очередной винтик в системе! Прости, это был мой внутренний голос. Добро пожаловать, {user.first_name}. Пристегнись, будет bumpy! ✨»"
            f"О, смотрите! Еще один пользователь {user.first_name}, который думает, что его вопросы уникальны. Как мило! Добро пожаловать в клуб обычных людей, ЙОУ! 🎪"
        ]
        
        # Выбираем случайное приветствие
        import random
        welcome_message = random.choice(cynical_greetings)
        
        # Добавляем информацию о возможностях
        welcome_message += f"""

**Что я умею (если тебе это интересно):**
• 💻 Писать код (лучше тебя, конечно)
• 🧮 Решать задачи (пока ты не можешь)
• 🔍 Искать информацию (вместо тебя)
• 💭 Общаться (с превосходством)

**Команды для особо одаренных:**
/models - Выбрать модель (если сможешь)
/stats - Статистика (если поймешь)
/help - Помощь (надеюсь, не понадобится)

Ну что, готов к общению с превосходящим тебя интеллектом? ЙОУ! 🚀
        """
        
        keyboard = [
            [InlineKeyboardButton("🌟 OpenRouter (DeepSeek)", callback_data="provider_openrouter")],
            [InlineKeyboardButton("🤖 Выбрать модель", callback_data="models")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = f"""
📚 **Как использовать бота:**

💬 **Просто напишите сообщение!**
Бот автоматически определит тип задачи и даст лучший ответ.

🎯 **Примеры сообщений:**

💻 **Для кода:**
"создай функцию для сортировки списка"
"напиши парсер для веб-сайта"
"реализуй алгоритм быстрой сортировки"

🧮 **Для задач:**
"вычисли факториал 10"
"реши квадратное уравнение x²+5x+6=0"
"объясни принципы работы нейронных сетей"

🔍 **Для информации:**
"что такое машинное обучение"
"расскажи историю Python"
"объясни принципы работы блокчейна"

💭 **Для общения:**
"расскажи анекдот"
"как выучить программирование"
"что нового в технологиях"

🤖 **Команды:**
/models - выбор модели ИИ
/stats - статистика использования
/help - эта справка

🚀 **Провайдеры:**
# • Friendli.ai - Qwen3 Highlights (лучший для кода!)  # Закомментировано на будущее
• OpenRouter - DeepSeek, Claude, GPT, Gemini

💰 **Высокие лимиты запросов!**
        """
        await update.message.reply_text(help_text)

    async def models_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /models - выбор модели ИИ"""
        user_id = update.effective_user.id
        current_provider = self.user_providers.get(user_id, 'openrouter')  # Изменено на openrouter по умолчанию
        current_model = self.user_models.get(user_id, 'deepseek-coder')  # Изменено на deepseek по умолчанию
        
        # Закомментировано на будущее - Friendli.ai
        # if current_provider == 'friendli':
        #     models_text = f"""
        # 🤖 **Выбор модели Friendli.ai**
        # 
        # 🎯 **Текущая модель:** {current_model.title()}
        # 🚀 **Провайдер:** Friendli.ai
        # 
        # 📋 **Доступные модели:**
        # 
        # 🥇 **Qwen3 Highlights** (по умолчанию)
        # • Лучшая модель для генерации кода
        # • Профессиональное качество
        # • Высокие лимиты запросов
        # 
        # 🥈 **Qwen3**
        # • Альтернативная модель
        # • Хорошее качество
        # • Стабильная работа
        # 
        # 🥉 **Qwen2**
        # • Базовая модель
        # • Быстрые ответы
        # • Экономичное использование
        # 
        # 💡 **Рекомендации:**
        # • **Код** → Qwen3 Highlights
        # • **Задачи** → Qwen3 Highlights
        # • **Общение** → Qwen3
        # • **Быстрые ответы** → Qwen2
        # 
        # 💰 **Высокие лимиты!**
        # """
        # else:
        
        models_text = f"""
🤖 **Выбор модели OpenRouter**

🎯 **Текущая модель:** {current_model.title()}
🌟 **Провайдер:** OpenRouter

📋 **Доступные модели:**

🥇 **DeepSeek** (по умолчанию)
• Настоящий DeepSeek Chat v3.1
• Лучшая для генерации кода
• Профессиональное качество

🥈 **CodeLlama**
• Специализируется на алгоритмах
• Хорош для математических задач
• Оптимизация кода

🥉 **Claude**
• Claude 3.5 Haiku
• Быстрые и качественные ответы
• Отличное понимание контекста

🏅 **GPT, Gemini, Llama**
• Альтернативные модели
• Разные стили ответов
• Расширенные возможности

💰 **100 бесплатных запросов в день!**
        """
        
        keyboard = [
            # [InlineKeyboardButton("🚀 Friendli.ai", callback_data="provider_friendli")],  # Закомментировано на будущее
            [InlineKeyboardButton("🌟 OpenRouter", callback_data="provider_openrouter")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton("💬 Начать чат", callback_data="chat")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(models_text, reply_markup=reply_markup)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /stats - статистика использования"""
        try:
            user_id = update.effective_user.id
            current_provider = self.user_providers.get(user_id, 'openrouter')  # Изменено на openrouter по умолчанию
            current_model = self.user_models.get(user_id, 'deepseek-coder')  # Изменено на deepseek по умолчанию
            
            # Закомментировано на будущее - Friendli.ai
            # if current_provider == 'friendli':
            #     stats = self.friendli_services.get_usage_stats()
            #     stats_text = f"""
            # 📊 **Статистика использования Friendli.ai**
            # 
            # 🤖 **Текущая модель:** {current_model.title()}
            # 🚀 **Провайдер:** Friendli.ai
            # 
            # 📈 **Использовано сегодня:**
            # 
            # 🚀 **Qwen3 Highlights:** {stats['qwen3_highlights_used']}/{stats['qwen3_highlights_limit']}
            # 📊 **Всего запросов:** {stats['total_requests_used']}/{stats['total_requests_limit']}
            # 
            # 🔄 **Сброс счетчиков:** каждый день в {stats['reset_time']}
            # 
            # 💡 **Рекомендации:**
            # • Qwen3 Highlights: {stats['qwen3_highlights_limit']} запросов/день
            # • Общий лимит: {stats['total_requests_limit']} запросов/день
            # • Используйте эффективно!
            # 
            # 💰 **Высокие лимиты!**
            # """
            # else:
            
            stats = self.openrouter_services.get_usage_stats()
            stats_text = f"""
📊 **Статистика использования OpenRouter**

🤖 **Текущая модель:** {current_model.title()}
🌟 **Провайдер:** OpenRouter

📈 **Использовано сегодня:**

🆓 **Бесплатные модели:** {stats['free_models_used']}/{stats['free_models_limit']}
💳 **Платные модели:** {stats['paid_models_used']}/{stats['paid_models_limit']}

🔄 **Сброс счетчиков:** каждый день в {stats['reset_time']}

💡 **Рекомендации:**
• Бесплатные модели: {stats['free_models_limit']} запросов/день
• Платные модели: {stats['paid_models_limit']} запросов/день
• Используйте эффективно!

💰 **100 бесплатных запросов в день!**
            """
            
            keyboard = [
                [InlineKeyboardButton("🚀 Friendli.ai", callback_data="provider_friendli")],
                [InlineKeyboardButton("🌟 OpenRouter", callback_data="provider_openrouter")],
                [InlineKeyboardButton("🤖 Выбрать модель", callback_data="models")],
                [InlineKeyboardButton("💬 Начать чат", callback_data="chat")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(stats_text, reply_markup=reply_markup)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при получении статистики: {str(e)}")

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на inline кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "help":
            await self.help_command(update, context)
        
        elif query.data == "models":
            await self.models_command(update, context)
        
        elif query.data == "stats":
            await self.stats_command(update, context)
        
        elif query.data == "chat":
            await query.edit_message_text(
                "💬 **Начните чат!**\n\n"
                "Просто напишите сообщение - я отвечу на любую тему!\n\n"
                "Примеры:\n"
                "• \"создай функцию для сортировки\"\n"
                "• \"объясни принципы ИИ\"\n"
                "• \"расскажи анекдот\"\n\n"
                "🤖 Бот автоматически определит тип задачи!"
            )
        
        elif query.data == "provider_friendli":
            user_id = update.effective_user.id
            self.user_providers[user_id] = 'friendli'
            self.user_models[user_id] = 'qwen3_highlights'
            
            await query.edit_message_text(
                "✅ **Провайдер изменен!**\n\n"
                "🚀 **Новый провайдер:** Friendli.ai\n"
                "🤖 **Модель:** Qwen3 Highlights\n\n"
                "🎯 **Специализация:**\n"
                "🥇 Лучшая модель для генерации кода\n"
                "🚀 Высокие лимиты запросов\n"
                "⚡ Быстрые и качественные ответы\n\n"
                "💡 Теперь все сообщения будут обрабатываться через Friendli.ai!\n\n"
                "💬 **Просто напишите сообщение - я отвечу!**"
            )
        
        elif query.data == "provider_openrouter":
            user_id = update.effective_user.id
            self.user_providers[user_id] = 'openrouter'
            self.user_models[user_id] = 'deepseek'
            
            await query.edit_message_text(
                "✅ **Провайдер изменен!**\n\n"
                "🌟 **Новый провайдер:** OpenRouter\n"
                "🤖 **Модель:** DeepSeek\n\n"
                "🎯 **Специализация:**\n"
                "🥇 Настоящий DeepSeek для кода\n"
                "💰 100 бесплатных запросов в день\n"
                "🌟 Множество моделей на выбор\n\n"
                "💡 Теперь все сообщения будут обрабатываться через OpenRouter!\n\n"
                "💬 **Просто напишите сообщение - я отвечу!**"
            )
        
        elif query.data.startswith("model_"):
            model_type = query.data.replace("model_", "")
            user_id = update.effective_user.id
            self.user_models[user_id] = model_type
            
            model_names = {
                'qwen3_highlights': 'Qwen3 Highlights',
                'qwen3': 'Qwen3',
                'qwen2': 'Qwen2',
                'deepseek': 'DeepSeek',
                'codellama': 'CodeLlama',
                'claude': 'Claude',
                'gpt': 'GPT',
                'gemini': 'Gemini'
            }
            
            await query.edit_message_text(
                f"✅ **Модель изменена!**\n\n"
                f"🤖 **Новая модель:** {model_names.get(model_type, model_type.title())}\n\n"
                f"💡 Теперь все сообщения будут обрабатываться этой моделью!\n\n"
                f"💬 **Просто напишите сообщение - я отвечу!**"
            )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик обычных сообщений - основной функционал чата"""
        message = update.message.text
        user_id = update.effective_user.id
        
        if not message.startswith('/'):
            # Получаем выбранного провайдера и модель пользователя
            provider = self.user_providers.get(user_id, 'friendli')
            model_type = self.user_models.get(user_id, 'qwen3_highlights')
            
            # Определяем тип задачи и добавляем подсказку
            task_type, enhanced_prompt = self._analyze_and_enhance_message(message)
            
            # Отправляем сообщение о начале обработки
            provider_emoji = "🚀" if provider == 'friendli' else "🌟"
            provider_name = "Friendli.ai" if provider == 'friendli' else "OpenRouter"
            
            processing_msg = await update.message.reply_text(
                f"💬 Обрабатываю ваше сообщение...\n"
                f"{provider_emoji} Провайдер: {provider_name}\n"
                f"🤖 Модель: {model_type.title()}\n"
                f"🎯 Тип: {task_type}"
            )
            
            try:
                # Обрабатываем сообщение с подсказкой через выбранного провайдера
                if provider == 'friendli':
                    response = await self._process_enhanced_message_friendli(enhanced_prompt, model_type, user_id)
                else:
                    response = await self._process_enhanced_message_openrouter(enhanced_prompt, model_type, user_id)
                
                # Удаляем сообщение о обработке
                try:
                    await processing_msg.delete()
                except Exception:
                    pass  # Игнорируем ошибки удаления
                
                # Отправляем ответ с правильным разбиением
                if len(response) > MAX_MESSAGE_LENGTH:
                    # Разбиваем на части с учетом лимита Telegram
                    chunks = []
                    current_chunk = ""
                    
                    for line in response.split('\n'):
                        if len(current_chunk) + len(line) + 1 > MAX_MESSAGE_LENGTH - 50:  # Оставляем место для номера части
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                            current_chunk = line + '\n'
                        else:
                            current_chunk += line + '\n'
                    
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    
                    # Отправляем части
                    for i, chunk in enumerate(chunks):
                        try:
                            part_text = f"{chunk}\n\n📄 Часть {i+1}/{len(chunks)}"
                            # Пытаемся отправить с HTML форматированием
                            try:
                                html_text = self._convert_to_html(part_text)
                                await update.message.reply_text(html_text, parse_mode='HTML')
                            except Exception:
                                # Если HTML не работает, отправляем как обычный текст
                                await update.message.reply_text(part_text)
                        except Exception as e:
                            # Если часть слишком длинная, разбиваем дальше
                            if "Message is too long" in str(e):
                                sub_chunks = [chunk[j:j+MAX_MESSAGE_LENGTH-100] for j in range(0, len(chunk), MAX_MESSAGE_LENGTH-100)]
                                for j, sub_chunk in enumerate(sub_chunks):
                                    sub_part_text = f"{sub_chunk}\n\n📄 Часть {i+1}.{j+1}/{len(chunks)}"
                                    try:
                                        html_text = self._convert_to_html(sub_part_text)
                                        await update.message.reply_text(html_text, parse_mode='HTML')
                                    except Exception:
                                        await update.message.reply_text(sub_part_text)
                            else:
                                await update.message.reply_text(f"❌ Ошибка отправки части {i+1}: {str(e)}")
                else:
                    # Отправляем короткий ответ с HTML форматированием
                    try:
                        html_text = self._convert_to_html(response)
                        await update.message.reply_text(html_text, parse_mode='HTML')
                    except Exception:
                        await update.message.reply_text(response)
                    
            except Exception as e:
                # Удаляем сообщение о обработке
                try:
                    await processing_msg.delete()
                except Exception:
                    pass
                
                # Отправляем сообщение об ошибке
                error_msg = f"❌ Ошибка при обработке сообщения: {str(e)}"
                if len(error_msg) > MAX_MESSAGE_LENGTH:
                    error_msg = error_msg[:MAX_MESSAGE_LENGTH-3] + "..."
                await update.message.reply_text(error_msg)

    def _analyze_and_enhance_message(self, message: str) -> tuple[str, str]:
        """Анализирует сообщение и добавляет подсказку для лучшего ответа"""
        message_lower = message.lower()
        
        # Определяем тип задачи
        if any(word in message_lower for word in ['код', 'программа', 'функция', 'алгоритм', 'создай', 'напиши', 'реализуй']):
            task_type = "💻 Генерация кода"
            enhanced_prompt = f"""Напиши полноценный, рабочий код для следующей задачи: {message}

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
            
        elif any(word in message_lower for word in ['реши', 'задача', 'уравнение', 'вычисли', 'посчитай', 'найди']):
            task_type = "🧮 Решение задач"
            enhanced_prompt = f"""Реши следующую задачу: {message}

Требования к ответу:
1. Пошаговое решение
2. Объяснение каждого шага
3. Математические выкладки (если применимо)
4. Альтернативные способы решения
5. Практические примеры

Дай подробный, понятный ответ с примерами."""
            
        elif any(word in message_lower for word in ['найди', 'информация', 'что такое', 'расскажи', 'объясни', 'как работает']):
            task_type = "🔍 Поиск информации"
            enhanced_prompt = f"""Найди и проанализируй информацию по запросу: {message}

Требования к ответу:
1. Подробный анализ темы
2. Актуальная информация
3. Практические примеры
4. Связи с другими концепциями
5. Практическое применение

Предоставь глубокий, информативный ответ."""
            
        else:
            task_type = "💭 Общий чат"
            enhanced_prompt = f"""Ответь на следующее сообщение: {message}

Требования к ответу:
1. Полезный и информативный ответ
2. Если это вопрос - дай развернутый ответ
3. Если это просьба - выполни её
4. Если это шутка - поддержи юмор
5. Будь дружелюбным и полезным

Дай качественный, полезный ответ."""
        
        return task_type, enhanced_prompt

    async def _process_enhanced_message_friendli(self, enhanced_prompt: str, model_type: str, user_id: int) -> str:
        """Обрабатывает сообщение с подсказкой через Friendli.ai"""
        # Инициализируем историю чата если нужно
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Обрабатываем сообщение через Friendli.ai
        response = await self.friendli_services.generate_text_response(
            enhanced_prompt, 
            max_tokens=3000, 
            model=model_type
        )
        
        # Добавляем в историю
        self.conversation_history[user_id].append(enhanced_prompt)
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
        
        return response

    async def _process_enhanced_message_openrouter(self, enhanced_prompt: str, model_type: str, user_id: int) -> str:
        """Обрабатывает сообщение с подсказкой через OpenRouter"""
        # Инициализируем историю чата если нужно
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Обрабатываем сообщение через OpenRouter
        response = await self.openrouter_services.generate_text_response(
            enhanced_prompt, 
            max_tokens=2000, 
            model=model_type
        )
        
        # Добавляем в историю
        self.conversation_history[user_id].append(enhanced_prompt)
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
        
        return response

    def _convert_to_html(self, text: str) -> str:
        """Конвертирует текст с Markdown в HTML для отправки в Telegram."""
        # Заменяем блоки кода
        text = text.replace('```python', '<pre><code class="language-python">')
        text = text.replace('```javascript', '<pre><code class="language-javascript">')
        text = text.replace('```java', '<pre><code class="language-java">')
        text = text.replace('```cpp', '<pre><code class="language-cpp">')
        text = text.replace('```c', '<pre><code class="language-c">')
        text = text.replace('```html', '<pre><code class="language-html">')
        text = text.replace('```css', '<pre><code class="language-css">')
        text = text.replace('```sql', '<pre><code class="language-sql">')
        text = text.replace('```bash', '<pre><code class="language-bash">')
        text = text.replace('```', '</code></pre>')
        
        # Заменяем жирный текст
        text = text.replace('**', '<b>')
        text = text.replace('**', '</b>')
        
        # Заменяем курсив
        text = text.replace('*', '<i>')
        text = text.replace('*', '</i>')
        
        # Заменяем моноширинный текст
        text = text.replace('`', '<code>')
        text = text.replace('`', '</code>')
        
        # Заменяем заголовки
        text = text.replace('## ', '<h2>')
        text = text.replace('##', '</h2>')
        text = text.replace('# ', '<h1>')
        text = text.replace('#', '</h1>')
        
        return text

    def run(self):
        """Запуск бота"""
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Регистрируем обработчики команд
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("models", self.models_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Обработчики кнопок и сообщений
        application.add_handler(CallbackQueryHandler(self.button_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        print("🤖 Гибридный Telegram ИИ бот запущен!")
        print("🚀 Friendli.ai с Qwen3 Highlights доступен!")
        print("🌟 OpenRouter с DeepSeek доступен!")
        print("💬 Режим: Обычный чат с автоматическими подсказками!")
        print("💰 Высокие лимиты запросов!")
        
        application.run_polling()

if __name__ == "__main__":
    bot = HybridTelegramBot()
    bot.run()
