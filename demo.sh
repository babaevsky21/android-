#!/bin/bash

# Демонстрационный скрипт для SpellChecker
# Показывает возможности приложения

echo "🎬 ДЕМОНСТРАЦИЯ SpellChecker"
echo "================================"
echo ""

SPELL_CHECKER="/Users/chuvash/Desktop/456/dist/SpellChecker"

if [ ! -f "$SPELL_CHECKER" ]; then
    echo "❌ Исполняемый файл не найден!"
    exit 1
fi

echo "📝 Тест 1: Проверка текста с ошибками"
echo "Вводим: 'превет как дила'"
echo ""

# Отправляем команды приложению
{
    echo "превет как дила"
    sleep 2
    echo "q"
} | "$SPELL_CHECKER"

echo ""
echo "✅ Демонстрация завершена!"
echo "💡 Для полноценного использования запустите: ./dist/SpellChecker"
