@echo off
echo 🤖 Запуск Telegram ИИ бота...
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.8+ с python.org
    pause
    exit /b 1
)

echo ✅ Python найден
echo.

REM Проверяем наличие .env файла
if not exist ".env" (
    echo ⚠️ Файл .env не найден!
    echo 📝 Создаю .env из примера...
    copy env_example.txt .env
    echo.
    echo 🔑 Отредактируйте файл .env и добавьте ваши API ключи!
    echo.
    pause
)

REM Устанавливаем зависимости
echo 📦 Устанавливаем зависимости...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)

echo ✅ Зависимости установлены
echo.

REM Запускаем бота
echo 🚀 Запускаем бота...
echo.
python bot.py

pause
