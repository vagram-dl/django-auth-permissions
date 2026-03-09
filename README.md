# django-auth-permissions
Кастомная система аутентификации авторизации в Django с ролями и правилами доступа.
Проект реализует регистрацию и вход пользователей, управление профилем, гибкую систему прав доступа,основываясь на роли и бизнес-объекты.

## Основные возможности
- Регистрация и вход пользователей (JWT-аутентификация).
- Управление профилем (просмотр, обновление, мягкое удаление).
- Система ролей (admin,manager,user,guest).
- Бизнес-объекты (users,products,orders).
- Таблица правил доступа (CRUD-права для каждой роли и объекта).
- Мягкое удаление пользователей через 'is_active=False'

# Database Schema

## Users
-id (PK,int)
-first_name(string)
-last_name (string)
-patronymic (string)
-email (string,unique)
-password_hash (string,bcrypt)
-is_active (bool,default=True)

## Roles
-id (PK,int)
-name(string,unique)

## BusinessElements
-id (PK,int)
-name (string,unique)

## AccessRoleRules
-id(PK,int)
-role_id(FK->Roles.id)
-element_id(FK->BusinessElements.id)
-read_permission(bool)
-create_permission(bool)
-update_permission(bool)
-update_all_permission(bool)
-delete_permission(bool)
-delete_all_permission(bool)

## JWT
-id(PK,int)
-user_id(FK->Users.id)
-token(string,jwt)
-expire_at(datetime)

## API Endpoints

### Auth
-POST /register
Регистрация нового пользователя (first_name, last_name, patronymic,email,password).
**Request:**
'''json
{
  "first_name" : "Alina",
  "last_name" : "Ivanova",
  "patronymic" : "Petrovna",
  "email" : "example@exam.com",
  "password":"securepassword"
}

**Response:**
'''json
{
   "message" : "User registered successfully",
   "user_id" : 1
}

-POST /login
Вход в систему, возвращает JWT-токен.
**Request:**
'''json
{
   "email": "example@exam.com",
  "password": "securepassword"
}

**Response:**
'''json
{
   "access_token":"<jwt_token>",
   "token_type" : "bearer",
   "expire_at": "2026-03-09:03:00"
}

-POST /logout
Выход из системы, токен недействителен.
**Request:**
Authorization: Bearer <jwt_token>
**Response:**
'''json
{
   "message" : "Logged out successfully"
}

-GET /profile
Получение информации о пользователе.
**Request:**
Authorization: Bearer <jwt_token>
**Response:**
'''json
{
  "id" : 1,
  "first_name" : "Alina",
  "last_name" : "Ivanova",
  "email" : "example@exam.com",
  "is_active" : true
}

-PUT /profile
Обновление данных профиля.
**Request:**
Authorization: Bearer <jwt_token>

'''json
{
   "first_name" : "Alice",
   "last_name" : "Petrovna",
   "patronymic" : "Ivanova"
}

**Response:**
'''json
{
   "message" : "Profile updated successfully"
}

-DELETE /profile
Удаление аккаунта (is_active=False)
**Request:**
Authorization: Bearer <jwt_token>
**Response:**
'''json
{
   "message" : "Profile deleted successfully"
}
