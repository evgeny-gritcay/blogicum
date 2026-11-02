# Blogicum — персональный блог на Django


[![Python](https://img.shields.io/badge/Python-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-green?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-darkgreen?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Git](https://img.shields.io/badge/Git-red?style=flat-square&logo=git)](https://git-scm.com/)
[![Amvera](https://img.shields.io/badge/Deploy-Amvera-purple?style=flat-square)](https://amvera.ru/)

---

**Blogicum** — это Django-приложение для ведения персонального блога с публикацией постов, комментариями, профилями пользователей и пагинацией. Проект реализует типичные сценарии: просмотр ленты, просмотр профиля, фильтрацию по статусу публикации, подсчёт комментариев и обработку ошибок 403/404/500.

Проект отражает понимание Django-архитектуры, работы с ORM, шаблонами, статикой и обработкой ошибок.

## Что реализовано

- **CRUD для постов и комментариев**: создание, просмотр, редактирование и удаление постов и комментариев с проверкой прав доступа (только автор может редактировать/удалять).
- **Публикация и отображение постов**: посты могут быть опубликованы или находиться в черновике; на главной странице отображаются только опубликованные посты.
- **Авторизация и профили пользователей**: система регистрации и входа, отображение профиля пользователя и списка его публикаций.
- **Подсчёт комментариев**: количество комментариев к посту рассчитывается через `annotate(comment_count=Count('comments'))`.
- **Пагинация**: реализована через `Paginator`, вынесена в утилиту `paginate_queryset`.
- **Кастомные страницы ошибок**: 403, 404, 500 с отдельными шаблонами в `templates/pages/`.
- **Статические файлы и медиа**: подключены через `Whitenoise` (middleware), настроены пути для `STATIC_ROOT` и `MEDIA_ROOT`.
- **Администрирование**: настроен Django Admin, включая сворачиваемые поля (`collapse`).
- **Деплой и статика**: проект развёрнут на Amvera; для корректной раздачи статических файлов (CSS, JS, картинки) настроен `Whitenoise`.
- **Наполнение БД**: подготовлены фикстуры (JSON) для быстрого наполнения базы тестовыми данными.

## Стек технологий

- Python, Django (ORM, шаблоны, формы, аутентификация)
- SQL (SQLite для локальной разработки, PostgreSQL для продакшен‑логики)
- HTML/CSS (базовая вёрстка шаблонов)
- Git, GitHub
- Amvera (CI/CD и деплой)

## Установка и запуск

### 1. Клонирование репозитория

'''bash
git clone <URL-репозитория>
cd blogicum

### 2. Создание виртуального окружения и установка зависимостей
python -m venv venv
#### Для Windows:
venv\Scripts\activate
#### Для macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

### 3. Миграции и суперпользователь
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

### 4. Загрузка фикстур (опционально)
Если есть JSON-фикстуры для наполнения тестовыми данными:
python manage.py loaddata fixtures/db.json

### 5. Запуск сервера
python manage.py runserver

Проект будет доступен по адресу: http://127.0.0.1:8000/


## Основные маршруты (URL)
```text
Путь    	            Описание

/	                    Главная страница: лента опубликованных постов
/auth/login/	        Страница входа
/profile/<username>/	Профиль пользователя: его посты
/admin/	                Django Admin
/pages/404/	            Кастомная страница 404 (для тестов)
/pages/403/	            Кастомная страница 403 (для тестов)
```

## Структура проекта
```text
blogicum/
├── .gitignore
├── .mypy_cache/
├── .venv/
├── amvera.yaml
├── db.json
├── db.sqlite3
├── LICENSE
├── manage.py
├── pytest.ini
├── README.md
├── requirements.txt
├── setup.cfg
├── templates/                # <-- Центральная папка шаблонов в корне
│   ├── blog/                 # Шаблоны конкретного приложения blog
│   │   ├── index.html
│   │   ├── profile.html
│   │   └── includes/
│   │       ├── post_card.html
│   │       └── paginator.html
│   ├── pages/                # Шаблоны для приложения pages (ошибки, статические страницы)
│   │   ├── 403.html
│   │   ├── 404.html
│   │   └── 500.html
│   └── base.html             # Базовый шаблон (наследование для всех страниц)
├── blog/                     # Приложение Django: логика постов
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── utils.py
├── blogicum/                 # Корневая папка проекта (настройки)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── media/
├── pages/                    # Приложение Django: страницы ошибок и статика
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── sent_emails/
├── static/
└── tests/
    ├── __init__.py
    └── test_views.py
```

## Ссылки
🔗 Деплой (Amvera): https://blogicum-evgenyg.mia0.amvera.tech

## Лицензия
Проект распространяется под лицензией MIT.

## Автор: Евгений Грицай
## Год: 2026