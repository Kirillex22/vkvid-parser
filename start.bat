@echo off
SET VENV_DIR=.venv

:: Создаем виртуальное окружение, если его нет
IF NOT EXIST %VENV_DIR% (
    python -m venv %VENV_DIR%
    echo Виртуальное окружение создано.
)

:: Активируем виртуальное окружение
CALL %VENV_DIR%\Scripts\activate.bat

:: Устанавливаем зависимости
pip install --upgrade pip
pip install -r requirements.txt

playwright install
:: Запускаем основной скрипт
python -m src.main

:: Деактивируем виртуальное окружение
deactivate
pause