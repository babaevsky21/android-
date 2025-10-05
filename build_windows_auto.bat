REM ============================================================================
REM АВТОМАТИЧЕСКИЙ СКРИПТ СОЗДАНИЯ SpellChecker.exe ДЛЯ WINDOWS
REM ============================================================================
REM 
REM Этот batch-файл автоматически:
REM 1. Создает виртуальное окружение Python
REM 2. Устанавливает необходимые пакеты
REM 3. Собирает исполняемый .exe файл
REM 
REM ТРЕБОВАНИЯ:
REM - Python 3.8+ должен быть установлен и доступен в PATH
REM - Интернет-соединение для скачивания пакетов
REM 
REM ИСПОЛЬЗОВАНИЕ:
REM 1. Скопируйте все файлы проекта в папку на Windows
REM 2. Запустите этот batch-файл от имени администратора (рекомендуется)
REM 3. Дождитесь завершения сборки
REM 4. Готовый SpellChecker.exe будет в папке dist\
REM
REM ============================================================================

@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo.
echo ⚡ АВТОМАТИЧЕСКАЯ СБОРКА SpellChecker.exe ⚡
echo ==========================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ОШИБКА: Python не найден!
    echo.
    echo 📋 Для работы скрипта требуется:
    echo    1. Python 3.8 или новее
    echo    2. Python должен быть добавлен в PATH  
    echo.
    echo 💡 Скачайте Python с https://python.org
    echo    При установке обязательно отметьте "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python найден:
python --version
echo.

REM Проверяем наличие исходного файла
if not exist "spell_checker_windows.py" (
    echo ❌ ОШИБКА: Файл spell_checker_windows.py не найден!
    echo.
    echo 📋 Убедитесь, что все файлы проекта скопированы в текущую папку:
    echo    - spell_checker_windows.py
    echo    - SpellChecker_Windows.spec
    echo    - Все остальные файлы проекта
    echo.
    pause
    exit /b 1
)

echo 📁 Создание виртуального окружения...
if exist "venv" (
    echo ⚠️  Папка venv уже существует, удаляем...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ ОШИБКА: Не удалось создать виртуальное окружение!
    pause
    exit /b 1
)
echo ✅ Виртуальное окружение создано

echo.
echo 📦 Активация виртуального окружения и установка пакетов...
call venv\Scripts\activate.bat

echo 📥 Обновление pip...
python -m pip install --upgrade pip

echo 📥 Установка requests...
pip install requests

echo 📥 Установка beautifulsoup4...
pip install beautifulsoup4

echo 📥 Установка pyinstaller...
pip install pyinstaller

if %errorlevel% neq 0 (
    echo ❌ ОШИБКА: Не удалось установить пакеты!
    echo 💡 Проверьте интернет-соединение
    pause
    exit /b 1
)
echo ✅ Все пакеты установлены

echo.
echo 🔨 Сборка исполняемого файла...
echo ⏳ Это может занять несколько минут...

if exist "SpellChecker_Windows.spec" (
    echo 📋 Используется конфигурация SpellChecker_Windows.spec
    pyinstaller SpellChecker_Windows.spec
) else (
    echo 📋 Используется автоматическая конфигурация
    pyinstaller --onefile --name SpellChecker --console spell_checker_windows.py
)

if %errorlevel% neq 0 (
    echo ❌ ОШИБКА: Не удалось собрать исполняемый файл!
    echo.
    echo 🔧 Возможные причины:
    echo    - Недостаточно места на диске
    echo    - Антивирус блокирует PyInstaller
    echo    - Проблемы с правами доступа
    echo.
    echo 💡 Попробуйте:
    echo    1. Запустить от имени администратора
    echo    2. Временно отключить антивирус
    echo    3. Освободить место на диске
    echo.
    pause
    exit /b 1
)

echo.
echo 🎉 СБОРКА ЗАВЕРШЕНА УСПЕШНО! 🎉
echo ===============================
echo.

if exist "dist\SpellChecker.exe" (
    echo ✅ Исполняемый файл создан: dist\SpellChecker.exe
    
    REM Получаем размер файла
    for %%I in ("dist\SpellChecker.exe") do set size=%%~zI
    set /a size_mb=!size!/1024/1024
    
    echo 📊 Размер файла: !size_mb! МБ
    echo.
    
    echo 🚀 ГОТОВО К ИСПОЛЬЗОВАНИЮ:
    echo.
    echo 💻 Способы запуска:
    echo    1. Двойной клик на dist\SpellChecker.exe
    echo    2. run_spellchecker.bat
    echo    3. Из командной строки: dist\SpellChecker.exe
    echo.
    
    echo 📁 Файлы можно перенести на другой компьютер:
    echo    - dist\SpellChecker.exe (основной файл)
    echo    - run_spellchecker.bat (для удобного запуска)
    echo.
    
    echo 🧪 Хотите протестировать прямо сейчас? (y/n)
    set /p test_choice="Ваш выбор: "
    
    if /i "!test_choice!"=="y" (
        echo.
        echo 🧪 Запуск тестирования...
        echo ⏳ Приложение откроется в новом окне
        echo 💡 Введите текст с ошибками, например: "превет как дила"
        echo 🚪 Для выхода введите: q
        echo.
        pause
        start "" "dist\SpellChecker.exe"
    )
    
) else (
    echo ❌ ВНИМАНИЕ: Файл dist\SpellChecker.exe не найден!
    echo 🔍 Проверьте папку dist\ на наличие других файлов
    if exist "dist" (
        echo 📁 Содержимое папки dist\:
        dir /b dist\
    )
)

echo.
echo 📋 СБОРКА ЗАВЕРШЕНА
echo ===================
echo ✅ Исполняемый файл: dist\SpellChecker.exe  
echo 📖 Инструкции: BUILD_WINDOWS.md
echo 🎬 Демо: demo_windows.bat
echo.

echo 💡 Совет: Добавьте SpellChecker.exe в системный PATH
echo    для использования из любого места!
echo.

pause
echo.
echo 🎊 Спасибо за использование SpellChecker! 🎊
