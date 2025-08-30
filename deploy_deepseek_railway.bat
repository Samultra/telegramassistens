@echo off
echo 🚀 Развертывание DeepSeek бота на Railway
echo ===========================================

echo.
echo 📋 Проверка файлов...
if not exist "bot_deepseek.py" (
    echo ❌ Ошибка: bot_deepseek.py не найден!
    pause
    exit /b 1
)

if not exist "app_deepseek.py" (
    echo ❌ Ошибка: app_deepseek.py не найден!
    pause
    exit /b 1
)

if not exist "openrouter_services.py" (
    echo ❌ Ошибка: openrouter_services.py не найден!
    pause
    exit /b 1
)

if not exist "config_openrouter.py" (
    echo ❌ Ошибка: config_openrouter.py не найден!
    pause
    exit /b 1
)

if not exist "requirements_openrouter.txt" (
    echo ❌ Ошибка: requirements_openrouter.txt не найден!
    pause
    exit /b 1
)

echo ✅ Все необходимые файлы найдены!

echo.
echo 🔧 Проверка Procfile...
if exist "Procfile" (
    echo ✅ Procfile найден
) else (
    echo ❌ Procfile не найден, создаю...
    echo web: python app_deepseek.py > Procfile
    echo ✅ Procfile создан
)

echo.
echo 📦 Подготовка к деплою...
echo.
echo 🎯 Инструкции по развертыванию:
echo.
echo 1. Перейдите на https://railway.app/
echo 2. Войдите через GitHub
echo 3. Нажмите "New Project"
echo 4. Выберите "Deploy from GitHub repo"
echo 5. Выберите этот репозиторий
echo.
echo 🔑 Настройка переменных окружения:
echo.
echo В Railway добавьте следующие переменные:
echo TELEGRAM_TOKEN=ваш_telegram_токен
echo OPENROUTER_API_KEY=ваш_openrouter_ключ
echo.
echo 📋 Получение API ключей:
echo.
echo Telegram Bot Token:
echo 1. Напишите @BotFather в Telegram
echo 2. Отправьте /newbot
echo 3. Следуйте инструкциям
echo 4. Скопируйте токен
echo.
echo OpenRouter API Key:
echo 1. Зарегистрируйтесь на https://openrouter.ai/
echo 2. Перейдите в API Keys
echo 3. Создайте новый ключ
echo 4. Скопируйте ключ
echo.
echo 🚀 После настройки Railway автоматически запустит бота!
echo.
echo 💀 Циничные приветствия с философскими матами активированы!
echo 🖕 Подъебы с философским подтекстом включены!
echo 🧠 Черный юмор с ноткой философии активирован!
echo 🎭 ЙОУ! Бот готов к работе, философ-неудачник!
echo.
pause
