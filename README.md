## Проект YaCut

Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или генерирует сам сервис.

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AigulParamonova/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас Windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить проект:

```
flask run
```

### Технологии:
- Python 3
- Flask 2.0
- REST API
- SQLAlchemy 1.4
- Git
