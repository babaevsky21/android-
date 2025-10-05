# PowerShell скрипт для запуска SpellChecker на Windows
# Использование: .\run_spellchecker.ps1

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SpellChecker = Join-Path $ScriptDir "dist\SpellChecker.exe"

Write-Host "🚀 Запуск SpellChecker для Windows..." -ForegroundColor Green
Write-Host "📍 Путь: $SpellChecker" -ForegroundColor Yellow
Write-Host ""

# Проверяем существование исполняемого файла
if (-not (Test-Path $SpellChecker)) {
    Write-Host "❌ Ошибка: Исполняемый файл SpellChecker.exe не найден!" -ForegroundColor Red
    Write-Host "   Путь: $SpellChecker" -ForegroundColor Red
    Write-Host "   Возможно, нужно сперва собрать проект с помощью PyInstaller" -ForegroundColor Red
    Write-Host ""
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

# Запускаем приложение
try {
    & $SpellChecker
}
catch {
    Write-Host "❌ Ошибка при запуске: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Нажмите Enter для выхода"
}
