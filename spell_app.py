#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Приложение для проверки орфографии - терминальная версия
Запускается и работает в режиме чата
"""

import sys
import requests
import json
import time
import os
from datetime import datetime


class SpellCheckerApp:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.history = []
    
    def clear_screen(self):
        """Очищает экран терминала"""
        os.system('clear')
    
    def print_header(self):
        """Выводит заголовок приложения"""
        print("=" * 60)
        print("🔤 ПРОВЕРКА ОРФОГРАФИИ - ТЕРМИНАЛЬНОЕ ПРИЛОЖЕНИЕ")
        print("=" * 60)
        print("Введите текст для проверки или команду:")
        print("• 'help' или 'h' - помощь")
        print("• 'history' - показать историю")
        print("• 'clear' - очистить экран")
        print("• 'quit' или 'q' - выход")
        print("-" * 60)
    
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
            return text, False, f"Ошибка: {e}"
    
    def process_text(self, text):
        """Обрабатывает введенный текст"""
        if not text.strip():
            return
        
        print(f"🔍 Проверяю: {text}")
        print("⏳ Обработка...")
        
        corrected, has_errors, source = self.check_yandex_speller(text)
        
        if has_errors:
            print(f"✅ Исправлено ({source}): {corrected}")
        else:
            print(f"✅ Ошибок не найдено: {text}")
        
        # Сохраняем в историю
        self.history.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'original': text,
            'corrected': corrected,
            'has_errors': has_errors
        })
    
    def show_help(self):
        """Показывает помощь"""
        print("\n📖 СПРАВКА:")
        print("• Просто введите текст для проверки орфографии")
        print("• 'history' - показать последние 10 проверок")
        print("• 'clear' - очистить экран")
        print("• 'quit' или 'q' - выйти из приложения")
        print("• 'help' или 'h' - показать эту справку")
        print()
    
    def show_history(self):
        """Показывает историю проверок"""
        if not self.history:
            print("📝 История пуста")
            return
        
        print("\n📝 ИСТОРИЯ ПРОВЕРОК (последние 10):")
        print("-" * 60)
        
        for i, item in enumerate(self.history[-10:], 1):
            status = "❌ Исправлено" if item['has_errors'] else "✅ Без ошибок"
            print(f"{i:2d}. [{item['time']}] {status}")
            print(f"    Исходный: {item['original']}")
            if item['has_errors']:
                print(f"    Исправленный: {item['corrected']}")
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
                        print("👋 До свидания!")
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
            sys.exit(1)


def main():
    """Точка входа в приложение"""
    print("🚀 Запуск приложения проверки орфографии...")
    time.sleep(1)
    
    app = SpellCheckerApp()
    app.run()


if __name__ == "__main__":
    main()
