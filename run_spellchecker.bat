@echo off
REM Batch-файл для запуска SpellChecker на Windows
REM Использование: run_spellchecker.bat

set SCRIPT_DIR=%~dp0
set SPELL_CHECKER=%SCRIPT_DIR%dist\SpellChecker.exe

echo 🚀 Запуск SpellChecker для Windows...
echo 📍 Путь: %SPELL_CHECKER%
echo.

REM Проверяем существование исполняемого файла
if not exist "%SPELL_CHECKER%" (
    echo ❌ Ошибка: Исполняемый файл SpellChecker.exe не найден!
    echo    Путь: %SPELL_CHECKER%
    echo    Возможно, нужно сперва собрать проект с помощью PyInstaller
    echo.
    pause
    exit /b 1
)

REM Запускаем приложение
"%SPELL_CHECKER%"

REM Пауза после завершения (если запущено двойным кликом)
if "%1" neq "nopause" pause
