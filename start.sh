#!/bin/bash

VENV_DIR=".venv"

# Создаем виртуальное окружение, если его нет
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Виртуальное окружение создано."
fi

# Активируем виртуальное окружение
source "$VENV_DIR/bin/activate"

# Устанавливаем зависимости
pip install --upgrade pip
pip install -r requirements.txt

playwright install

# Запускаем основной скрипт
python -m src.main

# Деактивируем виртуальное окружение
deactivate
