# 🚀 Инструкции по развертыванию Telegram ИИ бота

## 📋 Предварительные требования

### Системные требования
- Python 3.8 или выше
- Минимум 4GB RAM
- 2GB свободного места на диске
- Стабильное интернет-соединение

### Операционные системы
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Ubuntu 18.04+ / Debian 9+
- ✅ CentOS 7+ / RHEL 7+

## 🔧 Установка на Windows

### 1. Установка Python
1. Скачайте Python с [python.org](https://www.python.org/downloads/)
2. При установке отметьте "Add Python to PATH"
3. Проверьте установку: `python --version`

### 2. Установка зависимостей
```cmd
# Откройте командную строку в папке проекта
cd C:\Users\Happy PC\Desktop\telegramAssistent

# Установите зависимости
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
1. Создайте файл `.env` в корне проекта
2. Скопируйте содержимое из `env_example.txt`
3. Заполните реальными значениями API ключей

### 4. Запуск бота
```cmd
python bot.py
```

## 🐧 Установка на Linux/macOS

### 1. Установка Python
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip

# macOS (с Homebrew)
brew install python3
```

### 2. Создание виртуального окружения
```bash
# Перейдите в папку проекта
cd /path/to/telegramAssistent

# Создайте виртуальное окружение
python3 -m venv venv

# Активируйте его
source venv/bin/activate  # Linux/macOS
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
```bash
# Создайте файл .env
cp env_example.txt .env

# Отредактируйте файл
nano .env
```

### 5. Запуск бота
```bash
python3 bot.py
```

## 🐳 Развертывание в Docker

### 1. Создание Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

### 2. Создание docker-compose.yml
```yaml
version: '3.8'

services:
  telegram-bot:
    build: .
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - HUGGINGFACE_TOKEN=${HUGGINGFACE_TOKEN}
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

### 3. Запуск в Docker
```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

## ☁️ Развертывание в облаке

### Heroku
1. Создайте аккаунт на [Heroku](https://heroku.com/)
2. Установите Heroku CLI
3. Создайте приложение: `heroku create your-bot-name`
4. Настройте переменные окружения
5. Разверните: `git push heroku main`

### Railway
1. Зарегистрируйтесь на [Railway](https://railway.app/)
2. Подключите GitHub репозиторий
3. Настройте переменные окружения
4. Автоматическое развертывание

### DigitalOcean
1. Создайте Droplet с Ubuntu
2. Подключитесь по SSH
3. Следуйте инструкциям для Linux
4. Настройте systemd сервис для автозапуска

## 🔄 Автозапуск

### Windows (Task Scheduler)
1. Откройте "Планировщик задач"
2. Создайте новую задачу
3. Настройте запуск при старте системы
4. Укажите команду: `python C:\path\to\bot.py`

### Linux (systemd)
Создайте файл `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram AI Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/telegramAssistent
ExecStart=/path/to/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Затем:
```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### macOS (launchd)
Создайте файл `~/Library/LaunchAgents/com.telegram.bot.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.telegram.bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/venv/bin/python</string>
        <string>/path/to/telegramAssistent/bot.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/path/to/telegramAssistent</string>
</dict>
</plist>
```

Затем:
```bash
launchctl load ~/Library/LaunchAgents/com.telegram.bot.plist
```

## 📊 Мониторинг

### Логирование
Бот автоматически ведет логи в файл `bot.log`. Настройте ротацию логов:

```bash
# Создайте скрипт для ротации
cat > rotate_logs.sh << 'EOF'
#!/bin/bash
if [ -f bot.log ]; then
    mv bot.log "bot.$(date +%Y%m%d_%H%M%S).log"
    gzip "bot.$(date +%Y%m%d_%H%M%S).log"
fi
EOF

chmod +x rotate_logs.sh

# Добавьте в crontab для ежедневной ротации
crontab -e
# Добавьте строку:
0 0 * * * /path/to/rotate_logs.sh
```

### Мониторинг процесса
```bash
# Проверка статуса
ps aux | grep bot.py

# Мониторинг ресурсов
htop
iotop

# Проверка логов
tail -f bot.log
```

## 🔒 Безопасность

### Firewall
```bash
# Ubuntu/Debian
sudo ufw allow 22/tcp
sudo ufw enable

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```

### SSL/TLS
Для HTTPS соединений настройте SSL сертификаты (Let's Encrypt).

### Обновления
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade

# CentOS/RHEL
sudo yum update

# macOS
brew update && brew upgrade
```

## 🚨 Устранение неполадок

### Бот не запускается
1. Проверьте логи: `python bot.py`
2. Убедитесь, что все зависимости установлены
3. Проверьте правильность API ключей
4. Проверьте подключение к интернету

### Ошибки API
1. Проверьте лимиты API
2. Убедитесь в правильности ключей
3. Проверьте статус сервисов

### Проблемы с производительностью
1. Мониторьте использование ресурсов
2. Настройте кэширование
3. Используйте более легкие модели

## 📈 Масштабирование

### Горизонтальное масштабирование
- Используйте балансировщик нагрузки
- Разверните несколько экземпляров бота
- Настройте общую базу данных

### Вертикальное масштабирование
- Увеличьте RAM и CPU
- Используйте SSD диски
- Оптимизируйте код

## 🔄 Обновления

### Автоматические обновления
```bash
# Создайте скрипт обновления
cat > update_bot.sh << 'EOF'
#!/bin/bash
cd /path/to/telegramAssistent
git pull origin main
pip install -r requirements.txt
sudo systemctl restart telegram-bot
EOF

chmod +x update_bot.sh
```

### Резервное копирование
```bash
# Создайте скрипт бэкапа
cat > backup_bot.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backup/telegram-bot"
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/bot_backup_$DATE.tar.gz" /path/to/telegramAssistent
find $BACKUP_DIR -name "bot_backup_*.tar.gz" -mtime +7 -delete
EOF

chmod +x backup_bot.sh
```

---

**Успешного развертывания! 🚀**
