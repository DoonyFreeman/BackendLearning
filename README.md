# Hotel Booking System (BackendLearning)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.136.1-009688)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11.9-3776AB)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7.4.0-DC382D)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.6.3-37814A)](https://docs.celeryproject.org/)

## Обзор

Проект представляет собой учебный (пет-проект) бэкенд системы бронирования отелей, разработанный на асинхронном фреймворке FastAPI. Демонстрирует современный стек Python для создания REST API, работы с базами данных, кэширования и фоновых задач.

Основные возможности:
- Регистрация и аутентификация пользователей (JWT)
- Полный CRUD для отелей, номеров, бронирований
- Фильтрация отелей и номеров по датам доступности
- Кэширование ответов через Redis
- Фоновая обработка задач (изменение размера изображений, уведомления о заезде) с помощью Celery
- Асинхронная работа с PostgreSQL через SQLAlchemy и asyncpg
- Миграции базы данных через Alembic
- Автоматическая документация API (Swagger UI)

## Стек технологий

### Основные зависимости (requirements.txt)
| Технология | Версия | Назначение |
|-----------|--------|------------|
| FastAPI | 0.136.1 | Веб-фреймворк для создания REST API |
| Uvicorn | 0.46.0 | ASGI-сервер для запуска приложения |
| SQLAlchemy | 2.0.49 | Асинхронный ORM для работы с базой данных |
| asyncpg | 0.31.0 | Асинхронный драйвер PostgreSQL |
| psycopg2-binary | 2.9.12 | Адаптер PostgreSQL |
| Alembic | 1.18.4 | Инструмент для миграций базы данных |
| Pydantic | 2.13.3 | Валидация данных и сериализация |
| pydantic-settings | 2.14.0 | Управление настройками приложения |
| Redis | 7.4.0 | Кэширование и брокер сообщений Celery |
| Celery | 5.6.3 | Фоновые задачи |
| fastapi-cache2 | 0.2.2 | Кэширование ответов API |
| PyJWT | 2.9.0 | Работа с JWT-токенами |
| python-jose | 3.5.0 | Кодирование/декодирование JWT |
| passlib | 1.7.4 | Хэширование паролей (bcrypt) |
| bcrypt | 4.0.1 | Шифрование паролей |
| Pillow | 12.2.0 | Обработка изображений |
| python-dotenv | 1.2.2 | Загрузка переменных окружения |

### Инфраструктура
- Python 3.11.9
- PostgreSQL 14+
- Redis 7.4.0

## Структура проекта

```
BackendLearning/
├── .env                  # Переменные окружения
├── .gitignore            # Исключения для Git
├── .python-version       # Версия Python
├── alembic.ini           # Конфигурация Alembic
├── requirements.txt      # Зависимости проекта
├── seed_data.py          # Скрипт заполнения БД тестовыми данными
├── _course_helpers/      # Вспомогательные файлы курса
│   └── fastapi_load_test.py
└── src/                  # Исходный код
    ├── main.py           # Точка входа в приложение FastAPI
    ├── config.py         # Настройки приложения (pydantic-settings)
    ├── database.py       # Настройка асинхронного подключения к БД
    ├── init.py           # Инициализация Redis
    ├── api/              # Обработчики маршрутов API
    │   ├── auth.py       # Аутентификация
    │   ├── hotels.py     # Отели
    │   ├── rooms.py      # Номера
    │   ├── bookings.py   # Бронирования
    │   ├── facilities.py # Удобства
    │   ├── images.py     # Загрузка изображений
    │   └── dependencies.py # Зависимости FastAPI (DI)
    ├── models/           # Модели SQLAlchemy ORM
    │   ├── hotels.py
    │   ├── rooms.py
    │   ├── bookings.py
    │   ├── users.py
    │   └── facilities.py
    ├── repositories/     # Слой доступа к данным
    │   ├── base.py       # Базовый класс репозитория
    │   ├── hotels.py
    │   ├── rooms.py
    │   ├── bookings.py
    │   ├── users.py
    │   ├── facilities.py
    │   └── mappers/      # Преобразование ORM <-> Схемы
    ├── schemas/          # Pydantic-схемы (валидация данных)
    │   ├── hotels.py
    │   ├── rooms.py
    │   ├── bookings.py
    │   ├── users.py
    │   └── facilities.py
    ├── services/         # Бизнес-логика
    │   └── auth.py       # Сервис аутентификации
    ├── tasks/            # Фоновые задачи Celery
    │   ├── celery_app.py # Конфигурация Celery
    │   └── tasks.py      # Определения задач
    ├── connectors/       # Коннекторы внешних сервисов
    │   └── redis_connector.py
    ├── utils/            # Вспомогательные функции
    │   └── db_manager.py
    ├── migrations/       # Миграции Alembic
    │   └── versions/     # Файлы миграций
    └── static/           # Статические файлы (изображения)
        └── images/
```

## Предварительные требования

- Python 3.11+
- PostgreSQL (настроенная база данных)
- Redis (запущенный сервер)
- Установленный менеджер пакетов pip

## Установка и настройка

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd BackendLearning
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # Для Linux/macOS
# .venv\Scripts\activate  # Для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корне проекта и заполните переменными:
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=booking

REDIS_HOST=localhost
REDIS_PORT=6379

JWT_SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Примените миграции базы данных:
```bash
alembic upgrade head
```

6. (Опционально) Заполните базу тестовыми данными:
```bash
python seed_data.py
```

## Запуск приложения

### Основной сервер FastAPI
```bash
uvicorn src.main:app --reload
```
Документация API будет доступна: http://localhost:8000/docs

### Воркер Celery (фоновые задачи)
```bash
celery -A src.tasks.celery_app worker --loglevel=info
```

### Планировщик Celery Beat (периодические задачи)
```bash
celery -A src.tasks.celery_app beat --loglevel=info
```

## Обзор API

### Аутентификация (`/auth`)
| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/auth/register` | Регистрация пользователя |
| POST | `/auth/login` | Вход (возвращает JWT в cookie) |
| GET | `/auth/me` | Информация о текущем пользователе |
| GET | `/auth/logout` | Выход (очистка cookie) |

### Отели (`/hotels`)
| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/hotels` | Список отелей (фильтрация по локации, названию, датам) |
| GET | `/hotels/{hotel_id}` | Информация об отеле |
| POST | `/hotels` | Создание отеля |
| PUT | `/hotels/{hotel_id}` | Полное обновление отеля |
| PATCH | `/hotels/{hotel_id}` | Частичное обновление отеля |
| DELETE | `/hotels/{hotel_id}` | Удаление отеля |

### Номера (`/hotels/{hotel_id}/rooms`)
| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/hotels/{hotel_id}/rooms` | Список номеров с доступностью (требуются date_from, date_to) |
| GET | `/hotels/{hotel_id}/rooms/{room_id}` | Информация о номере с удобствами |
| POST | `/hotels/{hotel_id}/rooms` | Создание номера (с facility_ids) |
| PUT | `/hotels/{hotel_id}/rooms/{room_id}` | Полное обновление номера |
| PATCH | `/hotels/{hotel_id}/rooms/{room_id}` | Частичное обновление номера |
| DELETE | `/hotels/{hotel_id}/rooms/{room_id}` | Удаление номера |

### Бронирования (`/bookings`)
| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/bookings` | Список всех бронирований |
| GET | `/bookings/me` | Бронирования текущего пользователя |
| POST | `/bookings` | Создание бронирования |

### Удобства (`/facilities`)
| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/facilities` | Список всех удобств (кэшируется на 60с) |
| POST | `/facilities` | Создание удобства |

### Изображения (`/images`)
| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/images` | Загрузка изображения (обрабатывается в фоне) |

## Переменные окружения (.env)

| Переменная | Описание | Пример значения |
|-----------|----------|-----------------|
| DB_HOST | Хост базы данных | localhost |
| DB_PORT | Порт базы данных | 5432 |
| DB_USER | Пользователь БД | postgres |
| DB_PASS | Пароль БД | postgres |
| DB_NAME | Имя базы данных | booking |
| REDIS_HOST | Хост Redis | localhost |
| REDIS_PORT | Порт Redis | 6379 |
| JWT_SECRET_KEY | Секретный ключ для JWT | "09d25e094faa6ca..." |
| JWT_ALGORITHM | Алгоритм шифрования JWT | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Время жизни токена (минуты) | 30 |

## Схема базы данных

### Основные сущности:
- **Users**: Пользователи (id, email, hashed_password)
- **Hotels**: Отели (id, title, location)
- **Rooms**: Номера (id, hotel_id, title, description, price, quantity)
- **Bookings**: Бронирования (id, user_id, room_id, date_from, date_to, price, total_cost)
- **Facilities**: Удобства (id, title)

### Связи:
- Отель → Номера: Один-ко-многим
- Пользователь → Бронирования: Один-ко-многим
- Номер → Бронирования: Один-ко-многим
- Номера ↔ Удобства: Многие-ко-многим (через rooms_facilities)

## Планы по развитию

- Добавление тестов (pytest)
- Ролевой доступ (RBAC) для администраторов
- Возможность отмены бронирования
- Интеграция с платежными системами
- Расширение фильтрации и поиска
- Документирование кода (docstrings)
