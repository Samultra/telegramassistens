import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from openrouter_services import OpenRouterServices
from config_openrouter import TELEGRAM_TOKEN, MAX_MESSAGE_LENGTH
import io

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.ai_services = OpenRouterServices()
        self.conversation_history = {}
        self.user_models = {}  # Сохраняем выбранные модели для каждого пользователя

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        welcome_text = f"""
🤖 Привет, {user.first_name}! 

Я ваш ИИ ассистент с настоящим DeepSeek!

💬 **Просто напишите сообщение** - я отвечу на любую тему!

🎯 **Что я умею:**
• 💻 Генерировать код и решать задачи
• 🧮 Математика, алгоритмы, программирование
• 🔍 Поиск и анализ информации
• 💭 Общение на любые темы

🤖 **Доступные модели:**
• DeepSeek - лучший для кода
• CodeLlama - для алгоритмов
• Claude, GPT - для общения

💰 **100 бесплатных запросов в день!**

💡 **Просто пишите - я сам пойму, что вам нужно!**
        """
        
        keyboard = [
            [InlineKeyboardButton("🤖 Выбрать модель", callback_data="models")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

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

💰 **Стоимость: 0 рублей!**
100 запросов в день бесплатно!
        """
        await update.message.reply_text(help_text)

    async def models_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /models - выбор модели ИИ"""
        user_id = update.effective_user.id
        current_model = self.user_models.get(user_id, 'deepseek')
        
        models_text = f"""
🤖 **Выбор модели ИИ**

🎯 **Текущая модель:** {current_model.title()}

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

💡 **Как выбрать:**
• **Код** → DeepSeek
• **Алгоритмы** → CodeLlama  
• **Общение** → Claude
• **Разнообразие** → GPT/Gemini/Llama

💰 **Все модели бесплатны!**
100 запросов в день
        """
        
        keyboard = [
            [InlineKeyboardButton("🥇 DeepSeek", callback_data="model_deepseek")],
            [InlineKeyboardButton("🥈 CodeLlama", callback_data="model_codellama")],
            [InlineKeyboardButton("🥉 Claude", callback_data="model_claude")],
            [InlineKeyboardButton("🤖 GPT", callback_data="model_gpt")],
            [InlineKeyboardButton("🌟 Gemini", callback_data="model_gemini")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(models_text, reply_markup=reply_markup)

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /stats - статистика использования"""
        try:
            stats = self.ai_services.get_usage_stats()
            user_id = update.effective_user.id
            current_model = self.user_models.get(user_id, 'deepseek')
            
            stats_text = f"""
📊 **Статистика использования OpenRouter**

🤖 **Текущая модель:** {current_model.title()}

📈 **Использовано сегодня:**

🆓 **Бесплатные модели:** {stats['free_models_used']}/{stats['free_models_limit']}
💳 **Платные модели:** {stats['paid_models_used']}/{stats['paid_models_limit']}

🔄 **Сброс счетчиков:** каждый день в {stats['reset_time']}

💡 **Рекомендации:**
• Бесплатные модели: 100 запросов/день
• Платные модели: 1000 запросов/день
• Используйте эффективно!

💰 **Стоимость: 0 рублей!**
            """
            
            keyboard = [
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
        
        elif query.data.startswith("model_"):
            model_type = query.data.replace("model_", "")
            user_id = update.effective_user.id
            self.user_models[user_id] = model_type
            
            model_names = {
                'deepseek': 'DeepSeek',
                'codellama': 'CodeLlama',
                'claude': 'Claude',
                'gpt': 'GPT',
                'gemini': 'Gemini'
            }
            
            await query.edit_message_text(
                f"✅ **Модель изменена!**\n\n"
                f"🤖 **Новая модель:** {model_names.get(model_type, model_type.title())}\n\n"
                f"🎯 **Специализация:**\n"
                f"{self._get_model_description(model_type)}\n\n"
                f"💡 Теперь все сообщения будут обрабатываться этой моделью!\n\n"
                f"💬 **Просто напишите сообщение - я отвечу!**"
            )
    
    def _get_model_description(self, model_type: str) -> str:
        """Получение описания модели"""
        descriptions = {
            'deepseek': '🥇 DeepSeek Chat v3.1 - лучший для генерации кода и понимания контекста',
            'codellama': '🥈 Специализируется на алгоритмах и математических задачах',
            'claude': '🥉 Claude 3.5 Haiku - быстрые и качественные ответы',
            'gpt': '🤖 GPT-3.5 Turbo - сбалансированное качество и скорость',
            'gemini': '🌟 Gemini 2.5 Flash - инновационные подходы к решению задач'
        }
        return descriptions.get(model_type, 'Универсальная модель')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик обычных сообщений - основной функционал чата"""
        message = update.message.text
        user_id = update.effective_user.id
        
        if not message.startswith('/'):
            # Получаем выбранную модель пользователя
            model_type = self.user_models.get(user_id, 'deepseek')
            
            # Определяем тип задачи и добавляем подсказку
            task_type, enhanced_prompt = self._analyze_and_enhance_message(message)
            
            # Отправляем сообщение о начале обработки
            processing_msg = await update.message.reply_text(
                f"💬 Обрабатываю ваше сообщение...\n"
                f"🤖 Модель: {model_type.title()}\n"
                f"🎯 Тип: {task_type}"
            )
            
            try:
                # Обрабатываем сообщение с подсказкой
                response = await self._process_enhanced_message(enhanced_prompt, model_type, user_id)
                
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

    async def _process_enhanced_message(self, enhanced_prompt: str, model_type: str, user_id: int) -> str:
        """Обрабатывает сообщение с подсказкой"""
        # Инициализируем историю чата если нужно
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Обрабатываем сообщение через OpenRouter
        response = await self.ai_services.generate_text_response(
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
        """Конвертирует обычный текст в HTML для Telegram"""
        # Заменяем специальные символы для HTML
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Добавляем HTML теги для форматирования
        text = text.replace('\n\n📄 Часть', '\n\n<code>')
        text = text.replace('/', '&#47;') # Для корректного отображения слэша
        text = text.replace('</code>', '</code>\n\n')
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
        
        print("🤖 Telegram ИИ бот запущен с OpenRouter API!")
        print("🎯 Настоящий DeepSeek доступен!")
        print("💬 Режим: Обычный чат с автоматическими подсказками!")
        print("💰 100 бесплатных запросов в день!")
        
        application.run_polling()

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
