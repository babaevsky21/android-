#!/bin/bash

# Скрипт для установки alias в систему
# Позволяет запускать SpellChecker командой 'spellcheck' из любого места

SPELL_CHECKER_PATH="/Users/chuvash/Desktop/456/dist/SpellChecker"
ALIAS_NAME="spellcheck"

echo "🔧 Установка алиаса для SpellChecker"
echo "===================================="

# Проверяем существование исполняемого файла
if [ ! -f "$SPELL_CHECKER_PATH" ]; then
    echo "❌ Ошибка: Исполняемый файл не найден по пути $SPELL_CHECKER_PATH"
    exit 1
fi

# Определяем файл конфигурации shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
    if [ ! -f "$SHELL_CONFIG" ]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    fi
    SHELL_NAME="bash"
else
    echo "⚠️  Неизвестная оболочка, попробуем .bashrc"
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="unknown"
fi

echo "📝 Добавляем алиас в $SHELL_CONFIG"

# Создаем резервную копию
if [ -f "$SHELL_CONFIG" ]; then
    cp "$SHELL_CONFIG" "$SHELL_CONFIG.backup_$(date +%Y%m%d_%H%M%S)"
    echo "✅ Создана резервная копия конфигурации"
fi

# Добавляем алиас
ALIAS_LINE="alias $ALIAS_NAME='$SPELL_CHECKER_PATH'"

# Проверяем, не существует ли уже такой алиас
if grep -q "alias $ALIAS_NAME=" "$SHELL_CONFIG" 2>/dev/null; then
    echo "⚠️  Алиас '$ALIAS_NAME' уже существует в $SHELL_CONFIG"
    echo "   Обновляем существующий алиас..."
    
    # Удаляем старый алиас и добавляем новый
    grep -v "alias $ALIAS_NAME=" "$SHELL_CONFIG" > "$SHELL_CONFIG.tmp" 2>/dev/null || touch "$SHELL_CONFIG.tmp"
    echo "$ALIAS_LINE" >> "$SHELL_CONFIG.tmp"
    mv "$SHELL_CONFIG.tmp" "$SHELL_CONFIG"
else
    echo "📝 Добавляем новый алиас..."
    echo "" >> "$SHELL_CONFIG"
    echo "# SpellChecker alias" >> "$SHELL_CONFIG"
    echo "$ALIAS_LINE" >> "$SHELL_CONFIG"
fi

echo "✅ Алиас успешно добавлен!"
echo ""
echo "🎯 Теперь вы можете использовать команду '$ALIAS_NAME' из любого места:"
echo "   $ALIAS_NAME"
echo ""
echo "🔄 Чтобы алиас заработал в текущей сессии, выполните:"
echo "   source $SHELL_CONFIG"
echo ""
echo "   Или просто откройте новый терминал."

# Предлагаем применить изменения сейчас
echo ""
read -p "🤔 Применить изменения сейчас? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    source "$SHELL_CONFIG"
    echo "✅ Изменения применены!"
    echo "💡 Теперь можете использовать команду: $ALIAS_NAME"
fi
