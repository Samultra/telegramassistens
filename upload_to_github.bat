@echo off
echo 🚀 Загрузка проекта в GitHub...
echo.

echo 📋 Проверка Git статуса...
git status

echo.
echo 🌐 Инструкции по загрузке в GitHub:
echo.
echo 1. Зайдите на https://github.com
echo 2. Нажмите "New repository" (зеленая кнопка)
echo 3. Введите название: telegram-ai-assistant
echo 4. Оставьте репозиторий публичным
echo 5. НЕ ставьте галочки на README, .gitignore, license
echo 6. Нажмите "Create repository"
echo.
echo После создания репозитория выполните команды:
echo.
echo git remote add origin https://github.com/YOUR_USERNAME/telegram-ai-assistant.git
echo git branch -M main
echo git push -u origin main
echo.

echo 💡 Замените YOUR_USERNAME на ваше имя пользователя GitHub
echo.

pause
