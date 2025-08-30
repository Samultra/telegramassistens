import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from free_ai_services import FreeAIServices
from config import TELEGRAM_TOKEN, COMMANDS, MAX_MESSAGE_LENGTH
import io

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.ai_services = FreeAIServices()
        self.conversation_history = {}
        self.user_models = {}  # Сохраняем выбранные модели для каждого пользователя

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        welcome_text = f"""
🤖 Привет, {user.first_name}! 

Я ваш ИИ ассистент, работающий на **бесплатных сервисах**!

🎯 Что я умею:
• 💻 Генерировать код (DeepSeek, CodeLlama, WizardCoder)
• 🧮 Решать задачи и уравнения
• 🔍 Искать информацию
• 🎨 Создавать изображения
• 💬 Общаться и помогать

🚀 Доступные модели:
• **DeepSeek** - лучший для кода (по умолчанию)
• **CodeLlama** - для алгоритмов
• **WizardCoder** - для разработки
• **Phind** - для оптимизации

💡 Команды:
/code <описание> - генерация кода
/solve <задача> - решение задач
/search <запрос> - поиск информации
/image <описание> - создание изображений
/models - выбор модели ИИ
/stats - статистика использования

🎉 **30,000+ бесплатных запросов в месяц!**
        """
        
        keyboard = [
            [InlineKeyboardButton("💻 Генерация кода", callback_data="code")],
            [InlineKeyboardButton("🧮 Решение задач", callback_data="solve")],
            [InlineKeyboardButton("🔍 Поиск информации", callback_data="search")],
            [InlineKeyboardButton("🎨 Создание изображений", callback_data="image")],
            [InlineKeyboardButton("🤖 Выбрать модель", callback_data="models")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = f"""
📚 Справка по командам:

💻 **Генерация кода:**
/code <описание> - создание кода на Python
Пример: /code сортировка списка чисел

🧮 **Решение задач:**
/solve <задача> - решение математических задач
Пример: /solve вычислить факториал 10

🔍 **Поиск информации:**
/search <запрос> - поиск и анализ информации
Пример: /search что такое машинное обучение

🎨 **Создание изображений:**
/image <описание> - генерация изображений
Пример: /image космический корабль в стиле аниме

🤖 **Управление моделями:**
/models - выбор модели ИИ для задач
/stats - статистика использования API

💬 **Общий чат:**
Просто напишите сообщение - я отвечу!

🎯 **Доступные модели:**
• DeepSeek (по умолчанию) - лучший для кода
• CodeLlama - для алгоритмов
• WizardCoder - для разработки
• Phind - для оптимизации

💰 **Стоимость: 0 рублей!**
30,000+ запросов в месяц бесплатно!
        """
        await update.message.reply_text(help_text)

    async def code_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /code"""
        if not context.args:
            await update.message.reply_text(
                "💻 Использование: /code <описание задачи>\n\n"
                "Примеры:\n"
                "• /code сортировка списка чисел\n"
                "• /code функция для вычисления факториала\n"
                "• /code парсер веб-страниц\n\n"
                "🤖 Используется модель: DeepSeek (лучшая для кода)"
            )
            return
        
        description = ' '.join(context.args)
        user_id = update.effective_user.id
        
        # Получаем выбранную модель пользователя или используем DeepSeek по умолчанию
        model_type = self.user_models.get(user_id, 'deepseek')
        
        await update.message.reply_text(f"💻 Генерирую код для: {description}\n🤖 Модель: {model_type.title()}")
        
        try:
            response = await self.ai_services.generate_code(description, model_type)
            if len(response) > MAX_MESSAGE_LENGTH:
                chunks = [response[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(response), MAX_MESSAGE_LENGTH)]
                for i, chunk in enumerate(chunks):
                    await update.message.reply_text(f"{chunk}\n\n(Часть {i+1}/{len(chunks)})")
            else:
                await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при генерации кода: {str(e)}")

    async def solve_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /solve"""
        if not context.args:
            await update.message.reply_text(
                "🧮 Использование: /solve <задача>\n\n"
                "Примеры:\n"
                "• /solve вычислить факториал 10\n"
                "• /solve решить квадратное уравнение x²+5x+6=0\n"
                "• /solve найти сумму чисел от 1 до 100"
            )
            return
        
        problem = ' '.join(context.args)
        user_id = update.effective_user.id
        model_type = self.user_models.get(user_id, 'deepseek')
        
        await update.message.reply_text(f"🧮 Решаю задачу: {problem}\n🤖 Модель: {model_type.title()}")
        
        try:
            response = await self.ai_services.generate_text_response(
                f"Реши следующую задачу: {problem}. Объясни решение пошагово.", 
                max_length=800,
                model_type=model_type
            )
            if len(response) > MAX_MESSAGE_LENGTH:
                chunks = [response[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(response), MAX_MESSAGE_LENGTH)]
                for i, chunk in enumerate(chunks):
                    await update.message.reply_text(f"{chunk}\n\n(Часть {i+1}/{len(chunks)})")
            else:
                await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при решении задачи: {str(e)}")

    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /search"""
        if not context.args:
            await update.message.reply_text(
                "🔍 Использование: /search <запрос>\n\n"
                "Примеры:\n"
                "• /search что такое искусственный интеллект\n"
                "• /search история Python\n"
                "• /search лучшие практики программирования"
            )
            return
        
        query = ' '.join(context.args)
        user_id = update.effective_user.id
        model_type = self.user_models.get(user_id, 'deepseek')
        
        await update.message.reply_text(f"🔍 Ищу информацию: {query}\n🤖 Модель: {model_type.title()}")
        
        try:
            response = await self.ai_services.generate_text_response(
                f"Найди информацию по запросу: {query}. Предоставь краткий, но информативный ответ.", 
                max_length=600,
                model_type=model_type
            )
            if len(response) > MAX_MESSAGE_LENGTH:
                chunks = [response[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(response), MAX_MESSAGE_LENGTH)]
                for i, chunk in enumerate(chunks):
                    await update.message.reply_text(f"{chunk}\n\n(Часть {i+1}/{len(chunks)})")
            else:
                await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при поиске информации: {str(e)}")

    async def image_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /image"""
        if not context.args:
            await update.message.reply_text(
                "🎨 Использование: /image <описание>\n\n"
                "Примеры:\n"
                "• /image космический корабль в стиле аниме\n"
                "• /image кот в шляпе, цифровое искусство\n"
                "• /image футуристический город ночью"
            )
            return
        
        description = ' '.join(context.args)
        await update.message.reply_text(f"🎨 Создаю изображение: {description}")
        
        try:
            response = await self.ai_services.generate_image(description)
            if response:
                image_stream = io.BytesIO(response)
                image_stream.name = 'generated_image.png'
                await update.message.reply_photo(image_stream, caption=f"🎨 Изображение по запросу: {description}")
            else:
                await update.message.reply_text("❌ Не удалось сгенерировать изображение. Попробуйте другой запрос.")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при генерации изображения: {str(e)}")

    async def chat_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /chat"""
        if not context.args:
            await update.message.reply_text(
                "💬 Использование: /chat <сообщение>\n\n"
                "Примеры:\n"
                "• /chat расскажи анекдот\n"
                "• /chat как выучить Python\n"
                "• /chat что нового в технологиях"
            )
            return
        
        message = ' '.join(context.args)
        user_id = update.effective_user.id
        model_type = self.user_models.get(user_id, 'deepseek')
        
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        await update.message.reply_text(f"💬 Обрабатываю сообщение...\n🤖 Модель: {model_type.title()}")
        
        try:
            response = await self.ai_services.chat_response(message, self.conversation_history[user_id], model_type)
            self.conversation_history[user_id].append(message)
            if len(self.conversation_history[user_id]) > 10:
                self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
            
            if len(response) > MAX_MESSAGE_LENGTH:
                chunks = [response[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(response), MAX_MESSAGE_LENGTH)]
                for i, chunk in enumerate(chunks):
                    await update.message.reply_text(f"{chunk}\n\n(Часть {i+1}/{len(chunks)})")
            else:
                await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при обработке сообщения: {str(e)}")

    async def models_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /models - выбор модели ИИ"""
        user_id = update.effective_user.id
        current_model = self.user_models.get(user_id, 'deepseek')
        
        models_text = f"""
🤖 **Выбор модели ИИ**

🎯 **Текущая модель:** {current_model.title()}

📋 **Доступные модели:**

🥇 **DeepSeek** (по умолчанию)
• Лучшая для генерации кода
• Понимает контекст задач
• Высокое качество ответов

🥈 **CodeLlama**
• Специализируется на алгоритмах
• Хорош для математических задач
• Быстрые ответы

🥉 **WizardCoder**
• Отлично для разработки
• Понимает архитектуру кода
• Детальные объяснения

🏅 **Phind**
• Лучший для оптимизации
• Анализ производительности
• Советы по улучшению

💡 **Как выбрать:**
• **Код** → DeepSeek
• **Алгоритмы** → CodeLlama  
• **Разработка** → WizardCoder
• **Оптимизация** → Phind

💰 **Все модели бесплатны!**
30,000 запросов в месяц
        """
        
        keyboard = [
            [InlineKeyboardButton("🥇 DeepSeek", callback_data="model_deepseek")],
            [InlineKeyboardButton("🥈 CodeLlama", callback_data="model_codellama")],
            [InlineKeyboardButton("🥉 WizardCoder", callback_data="model_wizardcoder")],
            [InlineKeyboardButton("🏅 Phind", callback_data="model_phind")],
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
📊 **Статистика использования**

🤖 **Текущая модель:** {current_model.title()}

📈 **Использовано в этом месяце:**

🤗 **Hugging Face:** {stats['huggingface_used']}/{stats['huggingface_limit']}
🎨 **Replicate:** {stats['replicate_used']}/{stats['replicate_limit']}
💬 **Cohere:** {stats['cohere_used']}/{stats['cohere_limit']}

💡 **Рекомендации:**
• Hugging Face: основной сервис (30K запросов)
• Replicate: только важные изображения (500)
• Cohere: быстрые текстовые ответы (1K)

🔄 **Сброс счетчиков:** каждый месяц

💰 **Стоимость: 0 рублей!**
        """
            
            keyboard = [
                [InlineKeyboardButton("🤖 Выбрать модель", callback_data="models")],
                [InlineKeyboardButton("💻 Генерация кода", callback_data="code")],
                [InlineKeyboardButton("🔍 Поиск информации", callback_data="search")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(stats_text, reply_markup=reply_markup)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка при получении статистики: {str(e)}")

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на inline кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "code":
            await query.edit_message_text(
                "💻 **Генерация кода**\n\n"
                "Используйте команду:\n"
                "/code <описание задачи>\n\n"
                "Примеры:\n"
                "• /code сортировка списка\n"
                "• /code функция факториала\n"
                "• /code парсер веб-страниц\n\n"
                "🤖 По умолчанию используется DeepSeek"
            )
        
        elif query.data == "solve":
            await query.edit_message_text(
                "🧮 **Решение задач**\n\n"
                "Используйте команду:\n"
                "/solve <задача>\n\n"
                "Примеры:\n"
                "• /solve вычислить факториал 10\n"
                "• /solve решить уравнение x²+5x+6=0\n"
                "• /solve найти сумму от 1 до 100"
            )
        
        elif query.data == "search":
            await query.edit_message_text(
                "🔍 **Поиск информации**\n\n"
                "Используйте команду:\n"
                "/search <запрос>\n\n"
                "Примеры:\n"
                "• /search что такое ИИ\n"
                "• /search история Python\n"
                "• /search лучшие практики кода"
            )
        
        elif query.data == "image":
            await query.edit_message_text(
                "🎨 **Создание изображений**\n\n"
                "Используйте команду:\n"
                "/image <описание>\n\n"
                "Примеры:\n"
                "• /image космический корабль\n"
                "• /image кот в шляпе\n"
                "• /image футуристический город"
            )
        
        elif query.data == "models":
            await self.models_command(update, context)
        
        elif query.data == "stats":
            await self.stats_command(update, context)
        
        elif query.data.startswith("model_"):
            model_type = query.data.replace("model_", "")
            user_id = update.effective_user.id
            self.user_models[user_id] = model_type
            
            model_names = {
                'deepseek': 'DeepSeek',
                'codellama': 'CodeLlama',
                'wizardcoder': 'WizardCoder',
                'phind': 'Phind'
            }
            
            await query.edit_message_text(
                f"✅ **Модель изменена!**\n\n"
                f"🤖 **Новая модель:** {model_names.get(model_type, model_type.title())}\n\n"
                f"🎯 **Специализация:**\n"
                f"{self._get_model_description(model_type)}\n\n"
                f"💡 Теперь все команды будут использовать эту модель!\n\n"
                f"Попробуйте:\n"
                f"• /code <задача> - генерация кода\n"
                f"• /solve <задача> - решение задач\n"
                f"• /search <запрос> - поиск информации"
            )
    
    def _get_model_description(self, model_type: str) -> str:
        """Получение описания модели"""
        descriptions = {
            'deepseek': '🥇 Лучшая для генерации кода и понимания контекста',
            'codellama': '🥈 Специализируется на алгоритмах и математических задачах',
            'wizardcoder': '🥉 Отлично для разработки и архитектуры кода',
            'phind': '🏅 Лучший для оптимизации и анализа производительности'
        }
        return descriptions.get(model_type, 'Универсальная модель')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик обычных сообщений"""
        message = update.message.text
        user_id = update.effective_user.id
        
        if not message.startswith('/'):
            await update.message.reply_text("💬 Обрабатываю ваше сообщение...")
            
            try:
                # Получаем выбранную модель пользователя
                model_type = self.user_models.get(user_id, 'deepseek')
                
                if any(word in message.lower() for word in ['код', 'программа', 'функция', 'алгоритм']):
                    response = await self.ai_services.generate_code(message, model_type)
                elif any(word in message.lower() for word in ['реши', 'задача', 'уравнение', 'вычисли']):
                    response = await self.ai_services.generate_text_response(
                        f"Реши следующую задачу: {message}. Объясни решение пошагово.", 
                        max_length=800,
                        model_type=model_type
                    )
                elif any(word in message.lower() for word in ['найди', 'информация', 'что такое', 'расскажи']):
                    response = await self.ai_services.generate_text_response(
                        f"Найди информацию по запросу: {message}. Предоставь краткий, но информативный ответ.", 
                        max_length=600,
                        model_type=model_type
                    )
                elif any(word in message.lower() for word in ['картинка', 'изображение', 'рисунок', 'фото']):
                    response = await self.ai_services.generate_image(message)
                    if response:
                        image_stream = io.BytesIO(response)
                        image_stream.name = 'generated_image.png'
                        await update.message.reply_photo(image_stream, caption=f"🎨 Изображение по запросу: {message}")
                        return
                    else:
                        response = "❌ Не удалось сгенерировать изображение"
                else:
                    if user_id not in self.conversation_history:
                        self.conversation_history[user_id] = []
                    response = await self.ai_services.chat_response(message, self.conversation_history[user_id], model_type)
                    self.conversation_history[user_id].append(message)
                    if len(self.conversation_history[user_id]) > 10:
                        self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
                
                if len(response) > MAX_MESSAGE_LENGTH:
                    chunks = [response[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(response), MAX_MESSAGE_LENGTH)]
                    for i, chunk in enumerate(chunks):
                        await update.message.reply_text(f"{chunk}\n\n(Часть {i+1}/{len(chunks)})")
                else:
                    await update.message.reply_text(response)
                    
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка при обработке сообщения: {str(e)}")

    def run(self):
        """Запуск бота"""
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Регистрируем обработчики команд
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("code", self.code_command))
        application.add_handler(CommandHandler("solve", self.solve_command))
        application.add_handler(CommandHandler("search", self.search_command))
        application.add_handler(CommandHandler("image", self.image_command))
        application.add_handler(CommandHandler("chat", self.chat_command))
        application.add_handler(CommandHandler("models", self.models_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        
        # Обработчики кнопок и сообщений
        application.add_handler(CallbackQueryHandler(self.button_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        print("🤖 Telegram ИИ бот запущен с поддержкой DeepSeek!")
        print("🎯 Доступные модели: DeepSeek, CodeLlama, WizardCoder, Phind")
        print("💰 30,000+ бесплатных запросов в месяц!")
        
        application.run_polling()

def main():
    """Главная функция для запуска бота"""
    bot = TelegramBot()
    bot.run()

if __name__ == "__main__":
    main()
