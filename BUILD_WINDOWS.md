# 🪟 Создание .exe файла для Windows

## 📋 Требования для сборки

### На Windows:
1. **Python 3.8+** установленный в системе
2. **pip** (обычно идет с Python)
3. **Интернет-соединение** для установки пакетов

### На macOS (кросс-компиляция невозможна):
К сожалению, PyInstaller не может создавать .exe файлы для Windows на macOS. Нужно использовать Windows машину или виртуальную машину.

## 🔧 Инструкция по сборке на Windows

### Шаг 1: Подготовка окружения
```cmd
# Создать папку проекта
mkdir SpellChecker
cd SpellChecker

# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение
venv\Scripts\activate

# Установить зависимости
pip install requests beautifulsoup4 pyinstaller
```

### Шаг 2: Скопировать файлы
Скопируйте следующие файлы в папку проекта:
- `spell_checker_windows.py`
- `SpellChecker_Windows.spec`

### Шаг 3: Сборка exe файла
```cmd
# Активировать виртуальное окружение (если не активировано)
venv\Scripts\activate

# Собрать exe файл
pyinstaller SpellChecker_Windows.spec

# Или альтернативно:
pyinstaller --onefile --name SpellChecker --console spell_checker_windows.py
```

### Шаг 4: Тестирование
```cmd
# Перейти в папку с готовым файлом
cd dist

# Запустить приложение
SpellChecker.exe
```

## 📁 Структура файлов для Windows

После сборки у вас будет:
```
SpellChecker/
├── venv/                          # Виртуальное окружение
├── build/                         # Временные файлы сборки
├── dist/
│   └── SpellChecker.exe          # ← ГОТОВЫЙ .exe ФАЙЛ
├── spell_checker_windows.py      # Исходный код
├── SpellChecker_Windows.spec     # Конфигурация PyInstaller
├── run_spellchecker.bat          # Batch-скрипт для запуска
└── run_spellchecker.ps1          # PowerShell-скрипт для запуска
```

## 🚀 Использование готового .exe файла

### Способ 1: Прямой запуск
```cmd
# Просто запустить exe файл
dist\SpellChecker.exe

# Или двойной клик в проводнике
```

### Способ 2: Через batch-файл
```cmd
# Запустить batch-скрипт
run_spellchecker.bat
```

### Способ 3: Через PowerShell
```powershell
# Запустить PowerShell-скрипт
.\run_spellchecker.ps1
```

## 📦 Распространение

Готовый `SpellChecker.exe` можно:
- ✅ Копировать на любой Windows компьютер
- ✅ Запускать без установки Python
- ✅ Распространять как единый файл
- ✅ Добавить в PATH для глобального доступа

### Добавление в PATH (Windows):
1. Скопировать `SpellChecker.exe` в папку (например, `C:\Tools\`)
2. Добавить эту папку в системную переменную PATH
3. Теперь можно запускать из любого места: `SpellChecker`

## 🎯 Готовые файлы

Все необходимые файлы для Windows уже созданы:
- `spell_checker_windows.py` - исходный код (кроссплатформенный)
- `SpellChecker_Windows.spec` - конфигурация для PyInstaller
- `run_spellchecker.bat` - batch-скрипт для запуска
- `run_spellchecker.ps1` - PowerShell-скрипт для запуска

## ⚠️ Важные замечания

1. **Антивирус**: Некоторые антивирусы могут ложно срабатывать на exe файлы, созданные PyInstaller
2. **Размер**: exe файл будет около 15-20 МБ (включает Python runtime)
3. **Интернет**: Для работы нужно интернет-соединение (для API проверки орфографии)
4. **Windows версии**: Работает на Windows 7/8/10/11

## 🎉 Результат

После сборки у вас будет полностью автономный `SpellChecker.exe`, который:
- ✅ Запускается двойным кликом
- ✅ Работает в командной строке
- ✅ Не требует установленного Python
- ✅ Проверяет орфографию в интерактивном режиме
- ✅ Совместим с Windows
