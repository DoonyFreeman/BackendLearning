# Booking API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.136.1-009688)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7.4-DC382D)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.6-37814A)](https://docs.celeryproject.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)](https://www.docker.com/)

Асинхронный REST API для бронирования отелей. Пет-проект, демонстрирующий
промышленный подход к построению бэкенда на Python.

**Проблема:** типичный учебный проект — это монолит с синхронными запросами,
отсутствием фоновых задач, кэширования и тестов. Сервис кладут под один
нагрузкой.

**Что делает этот проект:** реализует полноценный бэкенд системы бронирования
с регистрацией, поиском отелей по датам, управлением номерами, бронированиями, —
всё асинхронно, с изоляцией слоёв, без блокировок I/O.

**Какие проблемы решает архитектура:**

- **Производительность** — async/await во всём стеке (FastAPI + SQLAlchemy 2.0 +
  asyncpg). Ни один запрос не блокирует event loop.
- **Тяжёлые операции вне request-response** — Celery выносит ресайз изображений
  и будущие email-рассылки в фоновые воркеры. API отвечает мгновенно.
- **Горячие эндпоинты не долбят БД** — список отелей и удобств кэшируется в Redis
  (fastapi-cache2, TTL 10s).
- **Безопасность** — пароли через bcrypt с солью, JWT в HTTP-only cookie
  (недоступен JS), схемы Request → Internal → Response исключают утечку полей.
- **БД под контролем** — Alembic версионирует схему, 7 миграций от первой
  таблицы до связей M2M.
- **Инфраструктура за минуту** — Docker Compose поднимает 6 сервисов одной
  командой: Postgres 16, Redis 7, Nginx с rate limiting, Celery Worker + Beat.
- **Тесты не трогают реальные данные** — отдельная `DB_NAME=test` через
  `.env-test`, изолированные fixtures, мок кэша.
- **Слой Repository + DataMapper** — SQLAlchemy не протекает в бизнес-логику.
  ORM-модели не покидают слой данных, наружу идут только Pydantic-схемы.

## Tech Stack

| Технология | Проблема | Решение |
|-----------|----------|---------|
| **FastAPI** | Синхронный REST фреймворк блокирует I/O | Async endpoints через `async/await`, автодокументация OpenAPI/Swagger |
| **SQLAlchemy 2.0 + asyncpg** | ORM блокирует event loop | Асинхронный движок + пул соединений, typed ORM-запросы |
| **Alembic** | Ручное управление схемой БД | Версионирование миграций, авто-генерация из моделей |
| **Pydantic V2** | Валидация на каждом слое вручную | Схемы RequestAdd → Add → Response с разделением ответственности |
| **Celery + Redis** | Тяжёлые операции (resize image, email) в request-response | Асинхронная очередь задач + периодический Celery Beat |
| **fastapi-cache2 + Redis** | Повторные одинаковые запросы к БД | Кэш с TTL 10с для горячих эндпоинтов (отели, удобства) |
| **JWT + bcrypt** | Хранение сессий на сервере | Stateless auth через HTTP-only cookie, Hash паролей с солью |
| **Repository Pattern + DataMapper** | SQLAlchemy протекает в бизнес-логику | Изоляция ORM: API → Service → Repository → DB, Mapper конвертирует ORM → Pydantic |
| **Nginx (rate limiting)** | Нет защиты от брутфорса | 10 запросов/сек на IP через `limit_req_zone` |
| **Pillow** | Клиентские изображения разного размера | Ресайз 3 варианта (200/500/1000px) в фоне через `BackgroundTasks` |
| **Docker Compose** | Ручной запуск 6 сервисов | Одна команда — Postgres, Redis, API, Celery Worker, Celery Beat, Nginx |

## Quick Start

### 1. Скопируй `.env.example` в `.env`

```bash
cp .env.example .env
# Для Docker: открой .env и замени DB_HOST=booking_db, REDIS_HOST=booking_cache
```

Все настройки в одном файле. `docker compose` сам подхватит переменные для Postgres,
Redis и приложения — дублирования нет.

### 2. Запусти

#### Docker (рекомендуется)

```bash
docker compose up
docker exec booking_back python -m alembic upgrade head
```

- API напрямую: http://localhost:7777/docs
- Через Nginx (rate limit 10 r/s): http://localhost:80/docs

#### Локально

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload
```

Фоновые задачи (отдельные терминалы):

```bash
celery -A src.tasks.celery_app worker -l INFO
celery -A src.tasks.celery_app beat -l INFO
```

### 3. (Опционально) Заполни тестовыми данными

```bash
python seed_data.py
```

## API

| Method | Path | Auth | Описание |
|--------|------|------|----------|
| POST | `/auth/register` | — | Регистрация (email + password) |
| POST | `/auth/login` | — | Вход, JWT в HTTP-only cookie |
| GET | `/auth/me` | Cookie | Текущий пользователь |
| GET | `/auth/logout` | — | Очистка cookie |
| GET | `/hotels` | — | Список отелей (cached 10s, фильтры: location, title, dates, пагинация) |
| GET | `/hotels/{id}` | — | Отель |
| POST | `/hotels` | — | Создать отель |
| PATCH | `/hotels/{id}` | — | Частичное обновление |
| DELETE | `/hotels/{id}` | — | Удалить |
| GET | `/hotels/{id}/rooms` | — | Номера отеля с доступностью (query: date_from, date_to) |
| POST | `/hotels/{id}/rooms` | — | Создать номер (с facilities_ids) |
| GET | `/hotels/{id}/rooms/{rid}` | — | Номер с удобствами |
| PATCH | `/hotels/{id}/rooms/{rid}` | — | Частичное обновление номера |
| DELETE | `/hotels/{id}/rooms/{rid}` | — | Удалить номер |
| GET | `/bookings` | — | Все бронирования |
| GET | `/bookings/me` | Cookie | Мои бронирования |
| POST | `/bookings` | Cookie | Создать бронь (room_id, date_from, date_to) |
| GET | `/facilities` | — | Удобства (cached 10s) |
| POST | `/facilities` | — | Создать удобство |
| POST | `/images` | — | Загрузить изображение (multipart, ресайз в фоне) |

## Architecture

```
Request → API Layer (router) → Service Layer (business logic)
                                     ↓
                              Repository Layer (data access)
                                     ↓
                              ORM Models (SQLAlchemy)
                                     ↓
                              PostgreSQL (asyncpg)
```

**Layered schemas (трёхуровневая валидация):**

```
*RequestAdd  — что шлёт клиент (например, BookingAddRequest: room_id, date_from, date_to)
     ↓
*Add         — что идёт в БД (BookingAdd: + user_id из JWT, + price из БД)
     ↓
*            — что возвращается клиенту (Booking: + id, from_attributes=True)
```

Это гарантирует, что клиент не отправит `user_id` или `price`, и не получит `hashed_password`.

## Project Structure

```
src/
├── main.py               # FastAPI app, lifespan (Redis, cache init)
├── config.py             # Pydantic Settings из .env
├── database.py           # async engine, sessionmaker, Base
├── exceptions.py         # Domain + HTTP exceptions
├── api/                  # Route handlers (auth, hotels, rooms, bookings, ...)
├── services/             # Business logic (AuthService, HotelService, ...)
├── repositories/         # Data access (CRUD, сложные запросы)
│   └── mappers/          # ORM → Pydantic converters
├── models/               # SQLAlchemy ORM models
├── schemas/              # Pydantic validation schemas
├── tasks/                # Celery config + task definitions
├── connectors/           # Redis async connector
├── migrations/           # Alembic migrations (7 files)
└── static/images/        # Uploaded + resized images
tests/
├── unit_tests/           # Unit: JWT creation
└── integration_tests/    # Integration: auth flow, hotels, bookings, facilities
```

## Environment Variables

Все переменные задаются в `.env`. Docker Compose использует их для Postgres и Redis
через `${}` интерполяцию — не нужно дублировать значения.

Шаблон: `.env.example` → копируешь в `.env`, правишь под себя.

| Variable | Пример | Описание |
|----------|--------|----------|
| `DB_HOST` | `booking_db` / `localhost` | Хост Postgres (Docker / локально) |
| `DB_PORT` | `5432` | Порт Postgres |
| `DB_USER` | `postgres` | Пользователь Postgres |
| `DB_PASS` | `postgres` | Пароль Postgres |
| `DB_NAME` | `booking` | Имя БД |
| `REDIS_HOST` | `booking_cache` / `localhost` | Хост Redis |
| `REDIS_PORT` | `6379` | Порт Redis |
| `JWT_SECRET_KEY` | `change-me` | Секрет для JWT (для прода — сгенерируй свой) |
| `JWT_ALGORITHM` | `HS256` | Алгоритм JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Время жизни токена (мин) |

## DB Schema

```
users (id, email*, hashed_password)
  └── bookings (id, user_id*, room_id*, date_from, date_to, price)
hotels (id, title, location)
  └── rooms (id, hotel_id*, title, description, price, quantity)
        └── rooms_facilities (id, room_id*, facility_id*)
facilities (id, title)
```

M2M: `rooms` ↔ `facilities` через `rooms_facilities`.