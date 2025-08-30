@echo off
chcp 65001 >nul
title Telegram ИИ Бот с OpenRouter API

echo.
echo ========================================
echo    🤖 TELEGRAM ИИ БОТ С OPENROUTER
echo ========================================
echo.
echo 🎯 Настоящий DeepSeek, CodeLlama, Claude!
echo 💰 100 бесплатных запросов в день!
echo.

:: Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo 💡 Установите Python с https://python.org/
    echo 💡 Убедитесь, что Python добавлен в PATH
    pause
    exit /b 1
)

echo ✅ Python найден!
python --version

:: Проверяем наличие .env файла
if not exist ".env" (
    echo.
    echo ⚠️  Файл .env не найден!
    echo 💡 Создайте файл .env на основе env_openrouter.txt
    echo 💡 Добавьте ваши API ключи:
    echo.
    echo    TELEGRAM_TOKEN=your_telegram_token
    echo    OPENROUTER_API_KEY=your_openrouter_key
    echo.
    echo 📋 Инструкции в README_OPENROUTER.md
    echo.
    pause
    exit /b 1
)

echo ✅ Файл .env найден!

:: Проверяем зависимости
echo.
echo 📦 Проверяем зависимости...
pip show python-telegram-bot >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  Зависимости не установлены!
    echo 💡 Устанавливаем...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Ошибка установки зависимостей!
        pause
        exit /b 1
    )
    echo ✅ Зависимости установлены!
) else (
    echo ✅ Зависимости уже установлены!
)

:: Тестируем конфигурацию
echo.
echo 🧪 Тестируем конфигурацию...
python test_openrouter.py
if errorlevel 1 (
    echo.
    echo ❌ Тестирование не прошло!
    echo 💡 Проверьте настройки в .env файле
    echo 💡 Убедитесь в правильности API ключей
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Тестирование прошло успешно!
echo.

:: Запускаем бота
echo 🚀 Запускаем Telegram ИИ бота...
echo 💡 Для остановки нажмите Ctrl+C
echo.

python bot_openrouter.py

echo.
echo 👋 Бот остановлен!
pause
