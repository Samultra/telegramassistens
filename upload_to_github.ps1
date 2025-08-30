# PowerShell скрипт для загрузки в GitHub
Write-Host "🚀 Загрузка проекта в GitHub..." -ForegroundColor Green
Write-Host ""

# Проверка Git статуса
Write-Host "📋 Проверка Git статуса..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "🌐 Инструкции по загрузке в GitHub:" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Зайдите на https://github.com" -ForegroundColor White
Write-Host "2. Нажмите 'New repository' (зеленая кнопка)" -ForegroundColor White
Write-Host "3. Введите название: telegram-ai-assistant" -ForegroundColor White
Write-Host "4. Оставьте репозиторий публичным" -ForegroundColor White
Write-Host "5. НЕ ставьте галочки на README, .gitignore, license" -ForegroundColor White
Write-Host "6. Нажмите 'Create repository'" -ForegroundColor White

Write-Host ""
Write-Host "После создания репозитория выполните команды:" -ForegroundColor Yellow
Write-Host ""

Write-Host "git remote add origin https://github.com/YOUR_USERNAME/telegram-ai-assistant.git" -ForegroundColor Gray
Write-Host "git branch -M main" -ForegroundColor Gray
Write-Host "git push -u origin main" -ForegroundColor Gray

Write-Host ""
Write-Host "💡 Замените YOUR_USERNAME на ваше имя пользователя GitHub" -ForegroundColor Magenta
Write-Host ""

# Открытие GitHub в браузере
Write-Host "🌐 Открываю GitHub в браузере..." -ForegroundColor Green
Start-Process "https://github.com"

Read-Host "Press Enter to continue..."
