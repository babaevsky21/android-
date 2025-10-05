@echo off
REM Демонстрационный batch-файл для SpellChecker Windows
chcp 65001 > nul

echo 🎬 ДЕМОНСТРАЦИЯ SpellChecker для Windows
echo ========================================
echo.

set SPELL_CHECKER=dist\SpellChecker.exe

if not exist "%SPELL_CHECKER%" (
    echo ❌ Исполняемый файл не найден!
    echo    Нужно сначала собрать проект с помощью PyInstaller
    echo    Смотрите BUILD_WINDOWS.md для инструкций
    echo.
    pause
    exit /b 1
)

echo 📝 Тест: Проверка текста с ошибками
echo Вводим: "превет как дила"
echo.

REM Отправляем команды приложению
(
    echo превет как дила
    timeout /t 3 /nobreak > nul
    echo q
) | "%SPELL_CHECKER%"

echo.
echo ✅ Демонстрация завершена!
echo 💡 Для полноценного использования запустите: %SPELL_CHECKER%
echo.
pause
