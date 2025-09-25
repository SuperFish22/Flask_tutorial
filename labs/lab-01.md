# Лабораторная работа №1

## Настройка окружения и структуры проекта

### Цель
Создать базовую структуру проекта, настроить виртуальное окружение и создать главную страницу.

### Задачи
1. Создание структуры проекта

```bash
mkdir flask_shop
cd flask_shop
```

2. Создание виртуального окружения

```bash
python -m venv venv

# Активация для Windows:
venv\Scripts\activate

# Активация для macOS/Linux:
source venv/bin/activate
```

3. Установка зависимостей

```bash
pip install flask
```

4. Создание структуры файлов

```text
flask_shop/
├── venv/
├── app.py
├── models.py
├── init_db.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── order.html
└── static/
    └── style.css
```

5. Файл `app.py` (базовый код)

```python
from flask import Flask

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)
```

6. Запуск приложения

```bash
python app.py
```

### Вопрос для самоконтроля
- Почему именная такая структура проекта ?
- Что такое вертуальное окружение ?

### Полезные ссылки
- Основы Flask: https://pythonru.com/uroki/3-osnovy-flask

