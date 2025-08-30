@echo off
echo 🔧 Проверка статуса деплоя на Railway
echo.

echo 📋 Что было исправлено:
echo ✅ Убраны тяжелые ML библиотеки (torch, transformers)
echo ✅ Используется легкий requirements.txt (~200 МБ)
echo ✅ Обновлен Procfile для использования app.py
echo ✅ Код загружен в GitHub
echo.

echo 🌐 Проверьте статус деплоя:
echo 1. Зайдите на https://railway.app
echo 2. Найдите ваш проект
echo 3. Проверьте статус деплоя
echo.

echo 📊 Ожидаемый результат:
echo - Размер образа: ~200 МБ (вместо 5.6 ГБ)
echo - Статус: Deployed ✅
echo - Бот работает с внешними AI API
echo.

echo 💡 Если деплой все еще не проходит:
echo 1. Нажмите "Redeploy" в Railway
echo 2. Проверьте логи на ошибки
echo 3. Убедитесь, что переменная TELEGRAM_TOKEN добавлена
echo.

start https://railway.app

pause
