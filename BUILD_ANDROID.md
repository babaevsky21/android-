# 📱 Создание Android APK для SpellChecker

## 🎯 Описание

SpellChecker Android App - это мобильное приложение с простым и удобным интерфейсом для проверки орфографии русского текста.

## 📱 Интерфейс приложения

```
┌─────────────────────────────────────┐
│       🔤 Проверка орфографии        │
│  Введите текст - получите результат │
├─────────────────────────────────────┤
│ Введите текст:                      │
│ ┌─────────────────────────────────┐ │
│ │ превет как дила хароший ден     │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│                                     │
│    🔍 Проверить орфографию          │
│                                     │
│ Результат:                          │
│ ┌─────────────────────────────────┐ │
│ │ ✅ Исправленный текст:          │ │
│ │ привет как дела хороший день    │ │
│ │                                 │ │
│ │ Исходный текст:                 │ │
│ │ превет как дила хароший ден     │ │
│ └─────────────────────────────────┘ │
│                                     │
│  🗑️ Очистить    📋 Копировать      │
└─────────────────────────────────────┘
```

## 🔧 Требования для сборки

### На Linux/macOS:
1. **Python 3.8+**
2. **Java JDK 8+**
3. **Android SDK** (будет установлен автоматически)
4. **Android NDK** (будет установлен автоматически)
5. **Git**

### На Windows:
1. **Python 3.8+**
2. **Java JDK 8+**
3. **Git**
4. **WSL** (Windows Subsystem for Linux) - рекомендуется

## 📦 Подготовка к сборке

### 1. Установка зависимостей

#### На Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --user --upgrade Cython==0.29.33 virtualenv
```

#### На macOS:
```bash
# Установить Homebrew если не установлен
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установить зависимости
brew install openjdk@8 autoconf automake libtool pkg-config
pip3 install --user --upgrade Cython==0.29.33 virtualenv
```

### 2. Настройка переменных окружения

```bash
# Добавить в ~/.bashrc или ~/.zshrc
export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"  # Linux
# или
export JAVA_HOME="/opt/homebrew/opt/openjdk@8"  # macOS

export PATH="$PATH:$JAVA_HOME/bin"
export ANDROID_HOME="$HOME/.buildozer/android/platform/android-sdk"
export PATH="$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools"
```

## 🚀 Сборка APK

### 1. Подготовка файлов

Скопируйте все файлы проекта в папку для сборки:
- `spellchecker_android.py` - основной код приложения
- `main.py` - точка входа (символическая ссылка)
- `buildozer.spec` - конфигурация сборки
- `icon.png` - иконка приложения
- `requirements.txt` - зависимости Python

### 2. Первая сборка (долгая)

```bash
# Перейти в папку проекта
cd /path/to/spellchecker/

# Инициализация buildozer (первый раз)
buildozer android debug

# Это может занять 30-60 минут при первой сборке!
# Buildozer скачает и установит:
# - Android SDK
# - Android NDK  
# - Python-for-Android
# - Все зависимости
```

### 3. Последующие сборки (быстрые)

```bash
# Обычная сборка (после изменений в коде)
buildozer android debug

# Очистка и пересборка (если что-то сломалось)
buildozer android clean
buildozer android debug

# Сборка релизной версии
buildozer android release
```

## 📁 Результат сборки

После успешной сборки APK файл будет находиться в:
```
bin/
├── spellchecker-1.0-arm64-v8a-debug.apk     # Debug версия ARM64
├── spellchecker-1.0-armeabi-v7a-debug.apk   # Debug версия ARM32
└── spellchecker-1.0-universal-debug.apk     # Universal версия
```

## 📱 Установка на устройство

### Через ADB (рекомендуется):
```bash
# Включить отладку по USB на устройстве
# Подключить устройство по USB

# Установить APK
adb install bin/spellchecker-1.0-universal-debug.apk

# Или переустановить
adb install -r bin/spellchecker-1.0-universal-debug.apk
```

### Через файловый менеджер:
1. Скопировать APK на устройство
2. Включить "Неизвестные источники" в настройках
3. Открыть APK файл и установить

## 🎮 Использование приложения

1. **Запустите** приложение SpellChecker
2. **Введите** текст с ошибками в поле ввода
3. **Нажмите** "🔍 Проверить орфографию"
4. **Получите** исправленный текст в поле результата
5. **Используйте** кнопки:
   - "🗑️ Очистить" - очистить поля
   - "📋 Копировать" - скопировать результат

## 🔧 Возможные проблемы

### 1. Ошибки при первой сборке:
```bash
# Очистить кэш
buildozer android clean

# Удалить .buildozer папку и начать заново
rm -rf .buildozer/
buildozer android debug
```

### 2. Проблемы с Java:
```bash
# Проверить версию Java
java -version

# Должна быть Java 8
# Если другая версия, установить Java 8
```

### 3. Недостаток места:
```bash
# Buildozer требует ~5-10 ГБ свободного места
# Очистить старые сборки:
buildozer android clean
```

### 4. Проблемы с сетью:
```bash
# При медленном интернете увеличить timeout
# В buildozer.spec добавить:
# [buildozer]
# timeout = 3600
```

## 📊 Размер приложения

- **APK размер:** ~25-35 МБ
- **После установки:** ~60-80 МБ
- **Минимальная версия Android:** 5.0 (API 21)
- **Целевая версия Android:** 13 (API 33)

## 🎯 Особенности Android версии

- ✅ **Простой интерфейс** - поле ввода и результат
- ✅ **Адаптивный дизайн** - подходит для любых экранов
- ✅ **Копирование результата** - в буфер обмена
- ✅ **Офлайн интерфейс** - работает без интернета (для ввода)
- ✅ **Быстрая проверка** - через Яндекс.Спеллер API
- ✅ **Обработка ошибок** - корректная работа при проблемах с сетью

## 🎉 Готово!

После сборки у вас будет полноценное Android приложение для проверки орфографии с красивым интерфейсом!
