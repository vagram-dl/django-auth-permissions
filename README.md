# Django Auth & Permissions System

Кастомная система аутентификации и авторизации на Django REST Framework с гибкой ролевой моделью (RBAC) и управлением правами доступа к бизнес-объектам.

## Основные возможности
- Регистрация и вход пользователей с выдачей JWT-токенов.
- Управление профилем (просмотр, обновление, мягкое удаление через `is_active=False`).
- Гибкая система ролей (`Admin`, `Manager`, `User`, `Guest`).
- Детальная матрица прав доступа (CRUD-права для каждой роли относительно конкретного бизнес-объекта).
- Rate Limiting для защиты эндпоинтов аутентификации от перебора паролей.
- Автоматическое заполнение БД тестовыми данными одной командой (`seed_data`).

## Технологический стек
- **Backend:** Python 3.13, Django, Django REST Framework
- **Database:** MySQL / PostgreSQL
- **Auth:** Custom JWT implementation, `djangorestframework-simplejwt` (или кастомная логика)
- **Testing:** Django `TestCase`, `unittest`
- **Tools:** `python-dotenv` (для `.env`), Git

## Структура базы данных
- **Users:** `id`, `first_name`, `last_name`, `patronymic`, `email` (unique), `password` (hashed), `is_active`, `role_id` (FK).
- **Roles:** `id`, `name` (unique).
- **BusinessElements:** `id`, `name`, `owner_id` (FK -> Users).
- **AccessRoleRules:** `id`, `role_id` (FK), `element_id` (FK), `read_permission`, `create_permission`, `update_permission`, `update_all_permission`, `delete_permission`, `delete_all_permission`.
- **JWT:** `id`, `user_id` (FK), `token`, `expire_at`.

## API Endpoints

### Auth
- `POST /register/` — Регистрация нового пользователя.
- `POST /login/` — Вход в систему, возвращает JWT-токен и время его жизни.
- `POST /logout/` — Аннулирование JWT-токена на сервере.

### Profile
- `GET /profile/` — Получение информации о текущем пользователе.
- `PUT /profile/` — Обновление данных профиля.
- `DELETE /profile/` — Мягкое удаление аккаунта (`is_active=False`).

### Users (Admin/Manager only)
- `GET /users/active/` — Список активных пользователей.
- `GET /users/admin/` — Список администраторов.
- `GET /users/recent/` — Пользователи, зарегистрированные за последние 7 дней.
- `GET /users/managers-or-users/` — Фильтрация по нескольким ролям.

### Access Rules
- `GET /access-rules/` — Просмотр полной матрицы прав доступа (только `Admin`).

## Модель авторизации (RBAC)
 Роль|Доступ к Orders|Доступ к Users |Доступ к /access-rules/ 

| **Guest** | Нет | Только регистрация/логин | Нет |
| **User** | Чтение (свои) | Нет | Нет |
| **Manager**| Чтение/Обновление (свои) | Управление своими | Нет |
| **Admin** | Полный CRUD | Полный CRUD | **Да** |

## Эволюция проекта (Changelog)
Этот проект проходит постоянный рефакторинг для соответствия лучшим практикам разработки:
- **v1.0:** Базовая реализация ТЗ (CRUD, JWT, роли).
- **v1.1:** Исправления по фидбеку код-ревью (безопасность, структура).
- **v2.0 (Текущая):** Глубокая оптимизация и рефакторинг:
  - Устранена проблема N+1 запросов через `select_related` и `list_select_related`.
  - Применены принципы **SOLID** (SRP, DIP) и **DRY** (универсальные функции сериализации, паттерн Repository для токенов).
  - Вынесена бизнес-логика в Service Layer (`AuthService`).
  - Добавлена management-команда `seed_data` для мгновенного развертывания тестового окружения.

## Как запустить проект
1. Клонируйте репозиторий и создайте виртуальное окружение.
2. Установите зависимости: `pip install -r requirements.txt`
3. Настройте переменные окружения в файле `.env`.
4. Примените миграции: `python manage.py migrate`
5. **Заполните БД тестовыми данными:** `python manage.py seed_data`
6. Запустите сервер: `python manage.py runserver`

> **Тестовые доступы (после seed_data):**
> - Admin: `admin@example.com` / `admin123`
> - User: `user@example.com` / `user123`
