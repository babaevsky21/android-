# 📦 Пакет файлов для создания Windows .exe

Этот пакет содержит все необходимые файлы для создания исполняемого .exe файла на Windows.

## 📁 Содержимое пакета

### Основные файлы:
- **`spell_checker_windows.py`** - исходный код приложения (кроссплатформенный)
- **`SpellChecker_Windows.spec`** - конфигурация PyInstaller для Windows
- **`BUILD_WINDOWS.md`** - подробная инструкция по сборке

### Скрипты запуска:
- **`run_spellchecker.bat`** - batch-файл для запуска
- **`run_spellchecker.ps1`** - PowerShell-скрипт для запуска  
- **`demo_windows.bat`** - демонстрация работы

## 🚀 Быстрый старт на Windows

1. **Скопируйте все файлы** на Windows машину
2. **Установите Python 3.8+** (если не установлен)
3. **Откройте командную строку** в папке с файлами
4. **Выполните следующие команды:**

```cmd
# Создать виртуальное окружение
python -m venv venv

# Активировать его
venv\Scripts\activate

# Установить зависимости
pip install requests beautifulsoup4 pyinstaller

# Собрать exe файл
pyinstaller SpellChecker_Windows.spec
```

5. **Готовый файл** будет в папке `dist\SpellChecker.exe`

## 🎯 Результат

После сборки у вас будет:
- **SpellChecker.exe** - готовое к использованию приложение
- Работает без установленного Python
- Размер ~15-20 МБ
- Совместимо с Windows 7/8/10/11

## 💻 Использование

```cmd
# Запуск приложения
dist\SpellChecker.exe

# Или через batch-файл
run_spellchecker.bat

# Или через PowerShell
.\run_spellchecker.ps1
```

В приложении:
```
💬 Введите текст: превет как дила
✅ Исправлено: привет как дела
```

## 📋 Требования

- Windows 7/8/10/11
- Интернет-соединение (для API проверки орфографии)
- Для сборки: Python 3.8+ + pip

## 🎉 Готово!

Все файлы готовы для создания Windows .exe приложения!
