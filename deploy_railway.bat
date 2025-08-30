@echo off
echo 🚀 Подготовка к деплою на Railway...
echo.

echo 📋 Проверка файлов...
if not exist "Procfile" (
    echo ❌ Файл Procfile не найден!
    pause
    exit /b 1
)

if not exist "runtime.txt" (
    echo ❌ Файл runtime.txt не найден!
    pause
    exit /b 1
)

if not exist "requirements_deploy.txt" (
    echo ❌ Файл requirements_deploy.txt не найден!
    pause
    exit /b 1
)

echo ✅ Все файлы найдены!
echo.

echo 🌐 Открытие Railway...
start https://railway.app

echo.
echo 📝 Инструкции по деплою:
echo 1. Войдите в Railway через GitHub
echo 2. Нажмите "New Project"
echo 3. Выберите "Deploy from GitHub repo"
echo 4. Выберите ваш репозиторий
echo 5. В настройках добавьте переменную: TELEGRAM_TOKEN=ваш_токен
echo 6. Railway автоматически деплоит ваш бот!
echo.

echo 🎯 После деплоя отправьте боту /start для проверки
echo.

pause
