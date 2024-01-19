# command-7-backend

## Как запустить при разработке

### Перейти в рабочуюю директорию
```
cd 7-command-backend/

```
### Активировать окружение
```
. venv/Scripts/activate

```
### Установить зависимости
```
pip install -r requirements.txt

```
### Активировать pre-commit
```
pre-commit install

```
### Выполнить миграции в БД
```
alembic upgrade head
```
### Запустить приложение
```
uvicorn app.main:app --reload

```

Посмотреть автоматическую документацию можно [здесь](http://127.0.0.1:8000/docs)
