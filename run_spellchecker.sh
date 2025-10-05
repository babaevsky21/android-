#!/bin/bash

# Скрипт для удобного запуска SpellChecker из любого места
# Использование: ./run_spellchecker.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SPELL_CHECKER="$SCRIPT_DIR/dist/SpellChecker"

# Проверяем существование исполняемого файла
if [ ! -f "$SPELL_CHECKER" ]; then
    echo "❌ Ошибка: Исполняемый файл SpellChecker не найден в $SCRIPT_DIR/dist/"
    echo "   Возможно, нужно сперва собрать проект с помощью PyInstaller"
    exit 1
fi

# Проверяем права на выполнение
if [ ! -x "$SPELL_CHECKER" ]; then
    echo "📝 Устанавливаю права на выполнение..."
    chmod +x "$SPELL_CHECKER"
fi

echo "🚀 Запуск SpellChecker..."
echo "📍 Путь: $SPELL_CHECKER"
echo ""

# Запускаем приложение
"$SPELL_CHECKER"
