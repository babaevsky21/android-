#!/bin/bash

# Простой скрипт для проверки орфографии
# Использует финальную версию программы

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH="$SCRIPT_DIR/.venv/bin/python"
CHECKER_PATH="$SCRIPT_DIR/final_checker.py"

# Проверяем существование Python в виртуальном окружении
if [ ! -f "$PYTHON_PATH" ]; then
    echo "Ошибка: Python не найден в виртуальном окружении"
    echo "Убедитесь, что виртуальное окружение настроено правильно"
    exit 1
fi

# Проверяем существование скрипта проверки
if [ ! -f "$CHECKER_PATH" ]; then
    echo "Ошибка: Скрипт проверки орфографии не найден"
    exit 1
fi

# Запускаем проверку орфографии с переданными аргументами
"$PYTHON_PATH" "$CHECKER_PATH" "$@"
