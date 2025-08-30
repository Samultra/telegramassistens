@echo off
echo 🚀 Быстрая загрузка в GitHub
echo.

echo 📋 Текущий статус Git:
git status

echo.
echo 🌐 Создайте репозиторий на GitHub:
echo 1. Зайдите на https://github.com
echo 2. Нажмите "New repository"
echo 3. Название: telegram-ai-assistant
echo 4. Публичный репозиторий
echo 5. НЕ ставьте галочки на README, .gitignore, license
echo 6. Нажмите "Create repository"
echo.

echo 💻 После создания выполните команды:
echo.
echo git remote add origin https://github.com/YOUR_USERNAME/telegram-ai-assistant.git
echo git branch -M main
echo git push -u origin main
echo.

echo 💡 Замените YOUR_USERNAME на ваше имя пользователя GitHub
echo.

start https://github.com

pause
