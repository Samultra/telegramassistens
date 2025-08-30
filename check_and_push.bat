@echo off
echo 🚀 Проверка и загрузка в GitHub
echo.

echo 📋 Текущий статус:
git status

echo.
echo 🔗 Настроенный remote:
git remote -v

echo.
echo 📦 Коммиты готовые к загрузке:
git log --oneline

echo.
echo 🌐 Инструкции:
echo 1. Создайте репозиторий на GitHub: https://github.com/new
echo 2. Название: telegram-ai-assistant
echo 3. Публичный репозиторий
echo 4. НЕ ставьте галочки на README, .gitignore, license
echo 5. Нажмите "Create repository"
echo.

echo 💻 После создания репозитория выполните:
echo git push -u origin main
echo.

echo 💡 Если репозиторий уже создан, нажмите любую клавишу для загрузки...
pause

echo.
echo 🚀 Загружаю код в GitHub...
git push -u origin main

echo.
echo ✅ Готово! Проверьте: https://github.com/samultra/telegram-ai-assistant
pause
