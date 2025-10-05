#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone приложение для проверки орфографии
Кроссплатформенная версия для Windows и macOS
"""

import sys
import requests
import json
import time
import os
import platform
from datetime import datetime


class SpellCheckerApp:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.history = []
        self.platform = platform.system()
    
    def clear_screen(self):
        """Очищает экран терминала кроссплатформенно"""
        if self.platform == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
    
    def print_header(self):
        """Выводит заголовок приложения"""
        print("=" * 70)
        print("🔤 ПРОВЕРКА ОРФОГРАФИИ - ТЕРМИНАЛЬНОЕ ПРИЛОЖЕНИЕ")
        print(f"🖥️  Система: {self.platform}")
        print("=" * 70)
        print("Введите текст для проверки или команду:")
        print("• 'help' или 'h' - помощь")
        print("• 'history' - показать историю")
        print("• 'clear' - очистить экран")
        print("• 'quit' или 'q' - выход")
        print("-" * 70)
    
    def check_yandex_speller(self, text):
        """Проверка через Яндекс.Спеллер"""
        try:
            url = "https://speller.yandex.net/services/spellservice.json/checkText"
            params = {'text': text, 'lang': 'ru', 'options': 0}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            corrected_text = text
            errors_found = len(result)
            
            offset = 0
            for error in result:
                if 's' in error and error['s']:
                    pos = error['pos'] + offset
                    length = error['len']
                    suggestion = error['s'][0]
                    
                    corrected_text = (corrected_text[:pos] + 
                                    suggestion + 
                                    corrected_text[pos + length:])
                    
                    offset += len(suggestion) - length
            
            return corrected_text, errors_found > 0, "Яндекс.Спеллер"
            
        except Exception as e:
            return text, False, f"Ошибка: {str(e)[:50]}..."
    
    def check_languagetool(self, text):
        """Проверка через LanguageTool (резервный вариант)"""
        try:
            url = "https://api.languagetool.org/v2/check"
            data = {'text': text, 'language': 'ru-RU'}
            
            response = self.session.post(url, data=data, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            corrected_text = text
            errors_found = len(result.get('matches', []))
            
            for match in reversed(result.get('matches', [])):
                if match.get('replacements'):
                    offset = match['offset']
                    length = match['length']
                    replacement = match['replacements'][0]['value']
                    
                    corrected_text = (corrected_text[:offset] + 
                                    replacement + 
                                    corrected_text[offset + length:])
            
            return corrected_text, errors_found > 0, "LanguageTool"
            
        except Exception as e:
            return text, False, f"Ошибка: {str(e)[:50]}..."
    
    def process_text(self, text):
        """Обрабатывает введенный текст"""
        if not text.strip():
            return
        
        print(f"\n🔍 Проверяю: {text}")
        print("⏳ Обработка...")
        
        # Сначала пробуем Яндекс.Спеллер
        corrected, has_errors, source = self.check_yandex_speller(text)
        
        # Если не сработал, пробуем LanguageTool
        if not has_errors and "Ошибка" in source:
            print("⚠️  Яндекс недоступен, пробую LanguageTool...")
            corrected, has_errors, source = self.check_languagetool(text)
        
        if has_errors:
            print(f"✅ Исправлено ({source}):")
            print(f"   📝 {corrected}")
        else:
            if "Ошибка" in source:
                print(f"❌ Сервисы недоступны: {text}")
            else:
                print(f"✅ Ошибок не найдено ({source})")
        
        # Сохраняем в историю
        self.history.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'original': text,
            'corrected': corrected,
            'has_errors': has_errors,
            'source': source
        })
    
    def show_help(self):
        """Показывает помощь"""
        print("\n📖 СПРАВКА:")
        print("• Просто введите текст для проверки орфографии")
        print("• Программа использует Яндекс.Спеллер и LanguageTool")
        print("• 'history' - показать последние 10 проверок")
        print("• 'clear' - очистить экран")
        print("• 'quit' или 'q' - выйти из приложения")
        print("• 'help' или 'h' - показать эту справку")
        print(f"• Работает на: {self.platform}")
        print()
    
    def show_history(self):
        """Показывает историю проверок"""
        if not self.history:
            print("\n📝 История пуста")
            return
        
        print(f"\n📝 ИСТОРИЯ ПРОВЕРОК (последние 10):")
        print("-" * 70)
        
        for i, item in enumerate(self.history[-10:], 1):
            status = "❌ Исправлено" if item['has_errors'] else "✅ Без ошибок"
            print(f"{i:2d}. [{item['time']}] {status} ({item.get('source', 'Unknown')})")
            print(f"    📄 Исходный: {item['original']}")
            if item['has_errors']:
                print(f"    📝 Исправленный: {item['corrected']}")
            print()
    
    def run(self):
        """Основной цикл приложения"""
        self.clear_screen()
        self.print_header()
        
        try:
            while True:
                try:
                    user_input = input("\n💬 Введите текст: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Обработка команд
                    if user_input.lower() in ['quit', 'q', 'exit']:
                        print("\n👋 До свидания!")
                        break
                    
                    elif user_input.lower() in ['help', 'h']:
                        self.show_help()
                    
                    elif user_input.lower() == 'history':
                        self.show_history()
                    
                    elif user_input.lower() == 'clear':
                        self.clear_screen()
                        self.print_header()
                    
                    else:
                        # Проверяем орфографию
                        self.process_text(user_input)
                
                except KeyboardInterrupt:
                    print("\n\n👋 Программа прервана. До свидания!")
                    break
                    
                except EOFError:
                    print("\n👋 До свидания!")
                    break
        
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            input("Нажмите Enter для выхода...")
            sys.exit(1)


def main():
    """Точка входа в приложение"""
    try:
        print("🚀 Запуск приложения проверки орфографии...")
        print(f"🖥️  Операционная система: {platform.system()} {platform.release()}")
        print("📡 Проверка подключения к интернету...")
        
        # Простая проверка интернета
        test_session = requests.Session()
        test_session.get("https://www.google.com", timeout=5)
        print("✅ Интернет-соединение в порядке")
        
        time.sleep(1)
        
        app = SpellCheckerApp()
        app.run()
        
    except requests.exceptions.RequestException:
        print("❌ Ошибка: Нет подключения к интернету")
        print("   Проверьте интернет-соединение и попробуйте снова")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Критическая ошибка при запуске: {e}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)


if __name__ == "__main__":
    main()
