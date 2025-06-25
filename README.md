# EduCounter

[![Python](https://img.shields.io/badge/python-3.12.x-blue)](#)
[![Django](https://img.shields.io/badge/Django-5.x-green)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-informational)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue)](#)
[![YOLOv11](https://img.shields.io/badge/YOLO-v11-orange)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](#)

## Содержание

1. [Описание проекта](#clipboard-описание-проекта)
2. [Технологии](#satellite-технологии)
3. [Установка](#inbox_tray-установка)
   - [Локально (Windows)](#локально-windows)
   - [На сервере (Ubuntu)](#на-сервере-ubuntu)
4. [Настройка](#floppy_disk-настройка-сервиса)
5. [Структура](#open_file_folder-структура-проекта)


---

## :clipboard: Описание проекта

EduCounter — это сервис для автоматического подсчёта количества людей в аудиториях. Состоит из двух основных компонентов:

1. **Веб-приложение на Django**  
   - Управление пользователями, авторизация, хранение статистики посещаемости (PostgreSQL).
   - Интерфейс для просмотра текущих показателей (через SSE обновляется информация о числе людей в реальном времени).
   - Интерфейс для просмотра статистики посещаемости.
2. **Асинхронный микросервис с FastAPI и YOLOv11**  
   - Подключается к видеопотоку, на лету детектирует людей с помощью обученной модели YOLOv11.  
   - Общается с фронтендом через FastAPI и Server-Sent Events (SSE).

---

## :satellite: Технологии

- **Python 3.12.x**
- **Django**
- **FastAPI**
- **PostgreSQL**
- **asyncio**
- **YOLO**
---

## :inbox_tray: Установка

### Локально (Windows)

1. **Создание базы данных PostgreSQL**
	```bash
	psql -U postgres
	# введите пароль, затем в psql:
	CREATE DATABASE educounter;
	CREATE USER educounter_admin WITH PASSWORD 'ваш пароль';
	ALTER SCHEMA public OWNER TO educounter_admin;
	GRANT ALL PRIVILEGES ON SCHEMA public TO educounter_admin;
	ALTER DATABASE educounter OWNER TO educounter_admin;
	GRANT ALL PRIVILEGES ON DATABASE educounter TO educounter_admin;
	```

2. **Клонирование репозитория**
	```bash
	git clone https://github.com/MrCrise/EduCounter.git
	cd EduCounter
	```

3. **Настройка виртуального окружения**
	```bash
	python3 -m venv venv
	source venv/Scripts/activate
	pip install --upgrade pip
	```

4. **Установка зависимостей**
	```bash
	pip install -r requirements.txt
	```

5. **Инициализация базы данных и создание суперпользователя Django**
	```bash
	cd site
	python manage.py migrate
	python manage.py createsuperuser
	```

6. **Запуск микросервиса FastAPI (в отдельном терминале, в директории neural)**
	```bash
	uvicorn main:app --reload --host 0.0.0.0 --port 8001
	```

7. **Запуск Django-сайта (в отдельном терминале, в директории site)**
	```bash
	python manage.py runserver
	```

---

### На сервере (Ubuntu)

1. **Установка системных пакетов**
	```bash
	sudo apt update && sudo apt upgrade -y
	sudo apt install -y python3-pip python3-venv git nginx postgresql postgresql-contrib
	```

2. **Настройка PostgreSQL**
	```bash
	sudo -u postgres psql <<SQL
	CREATE DATABASE educounter_db;
	CREATE USER educounter_admin WITH PASSWORD 'ваш пароль';
	ALTER SCHEMA public OWNER TO educounter_admin;
	GRANT ALL PRIVILEGES ON SCHEMA public TO educounter_admin;
	ALTER DATABASE educounter OWNER TO educounter_admin;
	GRANT ALL PRIVILEGES ON DATABASE educounter TO educounter_admin;
	\q
	SQL
	```

3. **Клонирование репозитория и создание окружения**
	```bash
	cd /opt
	sudo git clone https://github.com/MrCrise/EduCounter.git
	sudo chown -R $USER:$USER EduCounter
	cd EduCounter
	python3 -m venv venv
	source venv/bin/activate
	```

4. **Установка зависимостей**
	```bash
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install gunicorn
	```

5. **Миграции и сбор статики**
	```bash
	cd site
	python manage.py migrate
	python manage.py collectstatic --noinput
	```

6. **Создание Systemd сервисов**
	- FastAPI (/etc/systemd/system/educounter-api.service)
	```ini
	[Unit]
	Description=EduCounter FastAPI Service
	After=network.target

	[Service]
	User=$USER
	Group=$USER
	WorkingDirectory=/opt/EduCounter/neural
	EnvironmentFile=/opt/EduCounter/.env
	ExecStart=/opt/EduCounter/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001
	Restart=always

	[Install]
	WantedBy=multi-user.target
	```
	
	- Django + Gunicorn (/etc/systemd/system/educounter-web.service)
	```ini
	[Unit]
	Description=EduCounter Django Service
	After=network.target

	[Service]
	User=$USER
	Group=$USER
	WorkingDirectory=/opt/EduCounter/site
	EnvironmentFile=/opt/EduCounter/.env
	ExecStart=/opt/EduCounter/venv/bin/gunicorn EduCounter.wsgi:application \
		--bind unix:/run/educounter-web.sock --workers 3
	Restart=always

	[Install]
	WantedBy=multi-user.target
	```

7. **Включение созданных сервисов**
	```bash
	sudo mkdir -p /run/educounter
	sudo chown $USER:$USER /run/educounter
	sudo systemctl daemon-reload
	sudo systemctl enable educounter-api educounter-web
	sudo systemctl start  educounter-api educounter-web
	```

8. **Создание обратного прокси Nginx**
	- (/etc/nginx/sites-available/educounter)
	```nginx
	server {
		listen 80;
		server_name _;

		location / {
			proxy_pass http://unix:/run/educounter-web.sock;
			include proxy_params;
		}

		location /api/stream/ {
			proxy_pass            http://127.0.0.1:8001;
			proxy_http_version    1.1;
			proxy_set_header      Connection "";
			proxy_buffering       off;
			proxy_read_timeout    3600;
		}

		location /api/sse/ {
			proxy_pass            http://127.0.0.1:8001;
			proxy_http_version    1.1;
			proxy_set_header      Connection "";
			proxy_buffering       off;
			proxy_read_timeout    3600;
		}

		location /api/ {
			proxy_pass http://127.0.0.1:8001;
			include proxy_params;
			proxy_read_timeout 3600;
		}

		location /static/ {
			alias /opt/EduCounter/site/static/;
		}
	}
	```

9. **Активация и перезагрузка Nginx**
	```
	sudo ln -sf /etc/nginx/sites-available/educounter /etc/nginx/sites-enabled/
	sudo nginx -t
	sudo systemctl restart nginx
	```

---

## :floppy_disk: Настройка сервиса

### Нейросеть
- /neural/neural_config.py

### Пути к видео/стримам для обработки
Поддерживает как загрузку локального видео, так и стриминг по прямой ссылке (RTSP).
- /site/data/auditoriums_urls.py

---

## :open_file_folder: Структура проекта

```text
EduCounter/
├─ neural/
│  ├─ framegen.py
│  ├─ main.py
│  ├─ neural_config.py
│  ├─ predict.py
│  ├─ sessions.py
│  ├─ sse_api.py
├─ site/
│  ├─ attendance/
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ models.py
│  │  ├─ tests.py
│  │  ├─ urls.py
│  │  ├─ views.py
│  ├─ auditoriums/
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ models.py
│  │  ├─ tests.py
│  │  ├─ urls.py
│  │  ├─ views.py
│  ├─ data/
│  │  ├─ auditoriums_data.json
│  │  ├─ auditoriums_urls.py
│  ├─ EduCounter/
│  │  ├─ asgi.py
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  ├─ wsgi.py
│  ├─ login/
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ models.py
│  │  ├─ tests.py
│  │  ├─ urls.py
│  │  ├─ views.py
│  ├─ templates/
│  │  ├─ auditoriums/
│  │  │  ├─ auditorium_detail.html
│  │  │  ├─ auditoriums.html
│  │  │  ├─ charts.html
│  │  ├─ login/
│  │  │  ├─ login.html
│  ├─ manage.py
├─ .gitignore
├─ README.md
├─ requirements.txt
```

---
