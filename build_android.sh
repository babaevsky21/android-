#!/bin/bash

# Автоматический скрипт сборки SpellChecker Android APK
# Требует предустановленных зависимостей (см. BUILD_ANDROID.md)

set -e  # Выход при ошибке

echo "🤖 АВТОМАТИЧЕСКАЯ СБОРКА SpellChecker Android APK"
echo "================================================="
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для цветного вывода
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка зависимостей
print_status "Проверка системных зависимостей..."

# Проверка Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 не найден! Установите Python 3.8+"
    exit 1
fi

python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
print_success "Python найден: $python_version"

# Проверка Java
if ! command -v java &> /dev/null; then
    print_error "Java не найдена! Установите OpenJDK 8+"
    exit 1
fi

java_version=$(java -version 2>&1 | head -n 1)
print_success "Java найдена: $java_version"

# Проверка Git
if ! command -v git &> /dev/null; then
    print_error "Git не найден! Установите Git"
    exit 1
fi

print_success "Git найден"

# Проверка buildozer
print_status "Проверка buildozer..."
if ! command -v buildozer &> /dev/null; then
    print_warning "Buildozer не найден, устанавливаю..."
    pip3 install --user buildozer
    
    # Добавляем в PATH если нужно
    if ! command -v buildozer &> /dev/null; then
        export PATH="$PATH:$HOME/.local/bin"
        if ! command -v buildozer &> /dev/null; then
            print_error "Не удалось установить buildozer!"
            print_error "Попробуйте: pip3 install --user buildozer"
            print_error "И добавьте ~/.local/bin в PATH"
            exit 1
        fi
    fi
fi

print_success "Buildozer найден"

# Проверка файлов проекта
print_status "Проверка файлов проекта..."

required_files=("spellchecker_android.py" "buildozer.spec" "icon.png")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    print_error "Отсутствуют необходимые файлы:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    exit 1
fi

print_success "Все файлы проекта найдены"

# Создание символической ссылки main.py если не существует
if [ ! -f "main.py" ]; then
    print_status "Создание main.py..."
    ln -sf spellchecker_android.py main.py
    print_success "main.py создан"
fi

# Проверка/создание requirements.txt
if [ ! -f "requirements.txt" ]; then
    print_status "Создание requirements.txt..."
    cat > requirements.txt << EOF
kivy>=2.1.0
kivymd>=1.1.0
requests>=2.25.0
EOF
    print_success "requirements.txt создан"
fi

# Настройка переменных окружения
print_status "Настройка переменных окружения..."

# Попытка найти Java автоматически
if [ -z "$JAVA_HOME" ]; then
    if [ -d "/usr/lib/jvm/java-8-openjdk-amd64" ]; then
        export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
    elif [ -d "/opt/homebrew/opt/openjdk@8" ]; then
        export JAVA_HOME="/opt/homebrew/opt/openjdk@8"
    elif [ -d "/usr/local/opt/openjdk@8" ]; then
        export JAVA_HOME="/usr/local/opt/openjdk@8"
    else
        print_warning "JAVA_HOME не установлен автоматически"
        print_warning "Если сборка не удастся, установите JAVA_HOME вручную"
    fi
    
    if [ -n "$JAVA_HOME" ]; then
        print_success "JAVA_HOME установлен: $JAVA_HOME"
        export PATH="$PATH:$JAVA_HOME/bin"
    fi
fi

# Вопрос о типе сборки
echo ""
echo "🔧 Выберите тип сборки:"
echo "1) Debug (быстрая сборка для тестирования)"
echo "2) Release (оптимизированная сборка для распространения)"
echo "3) Clean + Debug (очистка и пересборка)"
echo ""

read -p "Ваш выбор (1-3): " build_choice

case $build_choice in
    1)
        BUILD_TYPE="debug"
        ;;
    2)
        BUILD_TYPE="release"
        ;;
    3)
        BUILD_TYPE="clean_debug"
        ;;
    *)
        print_warning "Неверный выбор, использую debug"
        BUILD_TYPE="debug"
        ;;
esac

# Предупреждение о времени сборки
echo ""
if [ ! -d ".buildozer" ]; then
    print_warning "⏰ ВНИМАНИЕ: Первая сборка может занять 30-60 минут!"
    print_warning "   Buildozer скачает Android SDK, NDK и все зависимости"
    print_warning "   Убедитесь, что у вас есть стабильное интернет-соединение"
    print_warning "   и ~10 ГБ свободного места на диске"
    echo ""
    read -p "Продолжить? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Сборка отменена"
        exit 0
    fi
else
    print_status "Найден кэш buildozer, сборка будет быстрее"
fi

# Запуск сборки
echo ""
print_status "🚀 Запуск сборки Android APK..."
print_status "Тип сборки: $BUILD_TYPE"
echo ""

start_time=$(date +%s)

case $BUILD_TYPE in
    "debug")
        buildozer android debug
        ;;
    "release")
        buildozer android release
        ;;
    "clean_debug")
        print_status "Очистка кэша..."
        buildozer android clean
        print_status "Запуск сборки..."
        buildozer android debug
        ;;
esac

end_time=$(date +%s)
duration=$((end_time - start_time))
minutes=$((duration / 60))
seconds=$((duration % 60))

echo ""
print_success "🎉 СБОРКА ЗАВЕРШЕНА УСПЕШНО!"
print_success "⏱️  Время сборки: ${minutes}м ${seconds}с"
echo ""

# Поиск созданных APK файлов
print_status "📱 Поиск созданных APK файлов..."

if [ -d "bin" ]; then
    apk_files=(bin/*.apk)
    if [ -e "${apk_files[0]}" ]; then
        print_success "Найденные APK файлы:"
        for apk in "${apk_files[@]}"; do
            size=$(du -h "$apk" | cut -f1)
            echo "  📦 $apk (размер: $size)"
        done
        
        echo ""
        print_status "📋 Информация для установки:"
        echo "1. Включите 'Отладка по USB' на Android устройстве"
        echo "2. Подключите устройство по USB"
        echo "3. Установите APK:"
        echo "   adb install \"${apk_files[0]}\""
        echo ""
        echo "Или скопируйте APK на устройство и установите через файловый менеджер"
        
        # Предложение установки через ADB
        if command -v adb &> /dev/null; then
            echo ""
            read -p "🤖 Установить APK через ADB сейчас? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_status "Установка через ADB..."
                if adb devices | grep -q "device$"; then
                    adb install -r "${apk_files[0]}"
                    print_success "APK установлен на устройство!"
                else
                    print_error "Устройство не найдено. Проверьте подключение USB и отладку"
                fi
            fi
        fi
        
    else
        print_error "APK файлы не найдены в папке bin/"
    fi
else
    print_error "Папка bin/ не найдена"
fi

echo ""
print_success "🎊 Готово! SpellChecker Android APK создан"
print_status "📖 Подробные инструкции: BUILD_ANDROID.md"
