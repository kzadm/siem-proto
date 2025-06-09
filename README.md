1. ## Установка

Клонировать репозиторий
```bash
git clone https://github.com/kzadm/siem-proto.git
```

Перейти в папку с проектом
```bash
cd some-project-folder
```

Установка виртуального окружения python
```bash
python3 -m venv venv
```

Активация виртуального окружения Windows
```bash
.\venv\Scripts\activate.bat
```

Активация виртуального окружения Linux (MacOS)
```bash
source venv/bin/activate
```

Установка зависимостей проекта
```bash
pip install -r requirements.txt
```

Выполить миграции базы данных
```bash
python manage.py migrate
```

Запуск проекта
```bash
python manage.py runserver
```

Запуск отслеживания логов в RealTime - в отдельном терминале
```bash
python -m siem_core.detector_runner
```