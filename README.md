
---

# Barter Project

**Barter** — это платформа для обмена объявлениями. Пользователи могут создавать объявления, просматривать их, предлагать обмен и управлять статусами предложений.

---

## Содержание

1. [Требования](#требования)
2. [Установка](#установка)
3. [Запуск проекта](#запуск-проекта)
4. [Выполнение тестов](#выполнение-тестов)
5. [Структура проекта](#структура-проекта)

---

## Требования

Для работы с проектом вам понадобятся:

- Python 3.10 или выше (я использовал 3.12)
- pip (для установки зависимостей)
- Git (для клонирования репозитория)
- База данных SQLite (по умолчанию) или другая база данных (например, PostgreSQL)

---

## Установка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/ainur2511/barter.git
cd barter
```

### 2. Создайте виртуальное окружение

Рекомендуется использовать виртуальное окружение для изоляции зависимостей.

```bash
python -m venv .venv
source .venv/bin/activate  # Для Linux/Mac
.venv\Scripts\activate     # Для Windows
```

### 3. Установите зависимости

Установите все необходимые пакеты из файла `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Настройте базу данных

По умолчанию БД SQLite.
Примените миграции для создания таблиц в базе данных.

```bash
python manage.py migrate
```

### 5. Создайте суперпользователя (опционально)

Если вы хотите получить доступ к админ-панели Django, создайте суперпользователя.
Отображение сущностей в админке по умолчанию не настроено.

```bash
python manage.py createsuperuser
```

---

## Запуск проекта

Запустите сервер разработки Django:

```bash
python manage.py runserver
```

Проект будет доступен по адресу:  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Админ-панель:  
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Выполнение тестов

Для проверки работоспособности проекта выполните тесты:

```bash
python manage.py test
```
---

## Структура проекта

### Основные директории:
- **`ads/`**: Приложение для работы с объявлениями и предложениями.
  - `models.py`: Модели (например, `Ad`, `ExchangeProposal`).
  - `views.py`: Представления (например, `AdListView`, `AdCreateView`).
  - `forms.py`: Формы (например, `AdForm`, `ExchangeProposalForm`).
  - `tests.py`: Тесты для моделей и представлений.
  - `urls.py`: Файл маршрутов приложения, подключенный к основному
- **`ads/templates/`**: Шаблоны HTML.
- ** `core/`: директория с основными настройками проекта.
  - `settings.py`: основные настройки проекта
  - `urls.py`: Основной файл маршрутов
- **`manage.py`**: Утилита для управления проектом.
- **`requirements.txt`**: Список зависимостей.

### Основные функции:
- Создание, просмотр, редактирование и удаление объявлений.
- Предложения обмена между пользователями.
- Управление статусами предложений (ожидание, принятие, отклонение).

---

## Дополнительная информация

### 1. Используемые технологии:
- **Django**: Веб-фреймворк.
- **Bootstrap**: CSS-фреймворк для стилизации интерфейса.
- **SweetAlert2**: Библиотека для красивых уведомлений.
- **SQLite**: База данных (по умолчанию).

### 2. Как внести изменения:
- Добавьте новые модели, формы и представления в соответствующие файлы.
- Обновите шаблоны в директории `templates/`.
- Напишите тесты для новых функций в `tests.py`.

---
