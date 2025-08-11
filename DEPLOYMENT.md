# 🚀 Руководство по развертыванию

Этот документ содержит инструкции по развертыванию бота на различных платформах.

## 📋 Предварительные требования

### Системные требования:
- Python 3.8 или выше
- Git
- Доступ к интернету

### Необходимые данные:
- Токен бота от @BotFather
- ID администраторов
- (Опционально) Redis сервер

## 🏠 Локальное развертывание

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-username/aiogram-2x-template.git
cd aiogram-2x-template
```

### 2. Создание виртуального окружения
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка конфигурации
```bash
cp env.example .env
# Отредактируйте .env файл
```

### 5. Запуск бота
```bash
python main.py
```

## ☁️ Развертывание на VPS/Сервере

### Ubuntu/Debian

#### 1. Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv git -y

# Установка Redis (опционально)
sudo apt install redis-server -y
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

#### 2. Клонирование и настройка
```bash
# Клонирование репозитория
git clone https://github.com/your-username/aiogram-2x-template.git
cd aiogram-2x-template

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка конфигурации
cp env.example .env
nano .env  # или используйте любой редактор
```

#### 3. Настройка systemd сервиса
```bash
# Создание файла сервиса
sudo nano /etc/systemd/system/telegram-bot.service
```

Содержимое файла `/etc/systemd/system/telegram-bot.service`:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/your/bot
Environment=PATH=/path/to/your/bot/venv/bin
ExecStart=/path/to/your/bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 4. Запуск сервиса
```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Включение автозапуска
sudo systemctl enable telegram-bot

# Запуск сервиса
sudo systemctl start telegram-bot

# Проверка статуса
sudo systemctl status telegram-bot

# Просмотр логов
sudo journalctl -u telegram-bot -f
```

### CentOS/RHEL

#### 1. Подготовка сервера
```bash
# Установка EPEL репозитория
sudo yum install epel-release -y

# Установка Python и зависимостей
sudo yum install python3 python3-pip git -y

# Установка Redis (опционально)
sudo yum install redis -y
sudo systemctl enable redis
sudo systemctl start redis
```

#### 2. Настройка (аналогично Ubuntu)
Следуйте тем же шагам, что и для Ubuntu.

## 🐳 Развертывание с Docker

### 1. Создание Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание пользователя для безопасности
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Запуск бота
CMD ["python", "main.py"]
```

### 2. Создание docker-compose.yml
```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: telegram-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - redis

  redis:
    image: redis:alpine
    container_name: bot-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### 3. Запуск с Docker
```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f bot

# Остановка
docker-compose down
```

## 🌐 Развертывание на облачных платформах

### Heroku

#### 1. Создание Procfile
```
worker: python main.py
```

#### 2. Создание runtime.txt
```
python-3.9.16
```

#### 3. Развертывание
```bash
# Установка Heroku CLI
# Создание приложения
heroku create your-bot-name

# Добавление переменных окружения
heroku config:set BOT_TOKEN=your_token
heroku config:set OWNER_IDS=your_id

# Развертывание
git push heroku main

# Запуск worker
heroku ps:scale worker=1
```

### Railway

#### 1. Подключение репозитория
1. Зайдите на [Railway](https://railway.app)
2. Подключите ваш GitHub репозиторий
3. Добавьте переменные окружения в настройках

#### 2. Настройка
Railway автоматически определит Python проект и запустит его.

### Render

#### 1. Создание сервиса
1. Зайдите на [Render](https://render.com)
2. Создайте новый Web Service
3. Подключите ваш репозиторий

#### 2. Настройка
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- Добавьте переменные окружения

## 🔧 Настройка Nginx (опционально)

Если вы хотите добавить веб-интерфейс или webhook:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Мониторинг и логирование

### Настройка логирования
```python
# В config.py
LOG_LEVEL = 'INFO'
LOG_FILE = '/var/log/telegram-bot/bot.log'

# Создание директории для логов
sudo mkdir -p /var/log/telegram-bot
sudo chown your-username:your-username /var/log/telegram-bot
```

### Мониторинг с помощью systemd
```bash
# Просмотр логов
sudo journalctl -u telegram-bot -f

# Статистика сервиса
sudo systemctl status telegram-bot

# Перезапуск сервиса
sudo systemctl restart telegram-bot
```

### Мониторинг с помощью Docker
```bash
# Просмотр логов
docker logs -f telegram-bot

# Статистика контейнера
docker stats telegram-bot

# Перезапуск контейнера
docker restart telegram-bot
```

## 🔒 Безопасность

### 1. Настройка файрвола
```bash
# Ubuntu/Debian
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 2. Обновление системы
```bash
# Настройка автоматических обновлений
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. Безопасность SSH
```bash
# Изменение порта SSH
sudo nano /etc/ssh/sshd_config
# Port 2222

# Отключение root логина
# PermitRootLogin no

# Перезапуск SSH
sudo systemctl restart sshd
```

## 🚨 Устранение неполадок

### Частые проблемы:

1. **Бот не запускается**
   - Проверьте токен в .env
   - Проверьте логи: `sudo journalctl -u telegram-bot -f`

2. **Ошибки подключения к базе данных**
   - Проверьте права доступа к файлу БД
   - Убедитесь, что директория существует

3. **Проблемы с Redis**
   - Проверьте статус: `sudo systemctl status redis`
   - Проверьте конфигурацию в .env

4. **Высокое потребление памяти**
   - Проверьте логи на утечки памяти
   - Рассмотрите использование Redis вместо MemoryStorage

### Полезные команды:
```bash
# Проверка статуса всех сервисов
sudo systemctl status telegram-bot redis nginx

# Просмотр использования ресурсов
htop
df -h
free -h

# Проверка логов
tail -f /var/log/telegram-bot/bot.log
```

## 📞 Поддержка

Если у вас возникли проблемы:

1. Проверьте логи на наличие ошибок
2. Убедитесь, что все зависимости установлены
3. Проверьте конфигурацию в .env файле
4. Создайте Issue в GitHub репозитории

---

**Удачного развертывания! 🚀**
