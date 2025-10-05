#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Финальная программа для проверки орфографии
Использует несколько методов проверки для максимальной надежности
"""

import sys
import requests
import argparse
from bs4 import BeautifulSoup
import json
import time


class MultiSpellChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def check_yandex_speller(self, text):
        """Проверка через Яндекс.Спеллер API"""
        try:
            url = "https://speller.yandex.net/services/spellservice.json/checkText"
            params = {
                'text': text,
                'lang': 'ru',
                'options': 0
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            corrected_text = text
            
            # Применяем исправления
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
            
            return corrected_text, True
            
        except Exception as e:
            return text, False

    def check_languagetool(self, text):
        """Проверка через LanguageTool API"""
        try:
            url = "https://api.languagetool.org/v2/check"
            data = {
                'text': text,
                'language': 'ru-RU'
            }
            
            response = self.session.post(url, data=data, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            corrected_text = text
            
            for match in reversed(result.get('matches', [])):
                if match.get('replacements'):
                    offset = match['offset']
                    length = match['length']
                    replacement = match['replacements'][0]['value']
                    
                    corrected_text = (corrected_text[:offset] + 
                                    replacement + 
                                    corrected_text[offset + length:])
            
            return corrected_text, True
            
        except Exception as e:
            return text, False

    def check_sinonim_org(self, text):
        """Проверка через sinonim.org/orfo"""
        try:
            url = "https://sinonim.org/orfo"
            
            # Получаем страницу
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Отправляем текст на проверку
            form_data = {'text': text}
            response = self.session.post(url, data=form_data, timeout=15)
            response.raise_for_status()
            
            # Пытаемся найти результат
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ищем различные варианты результата
            result_selectors = [
                'div.result',
                'div#result', 
                'textarea[name="text"]',
                '.corrected-text',
                '.spell-result'
            ]
            
            for selector in result_selectors:
                element = soup.select_one(selector)
                if element:
                    result_text = element.get_text(strip=True)
                    if result_text and result_text != text:
                        return result_text, True
            
            return text, False
            
        except Exception as e:
            return text, False

    def check_spelling(self, text):
        """Основная функция проверки, использует несколько методов"""
        methods = [
            ("Яндекс.Спеллер", self.check_yandex_speller),
            ("LanguageTool", self.check_languagetool),
            ("Sinonim.org", self.check_sinonim_org)
        ]
        
        for method_name, method_func in methods:
            try:
                corrected, success = method_func(text)
                if success and corrected != text:
                    return corrected, method_name
                    
                # Небольшая пауза между запросами
                time.sleep(0.5)
                
            except Exception as e:
                continue
        
        return text, None


def main():
    parser = argparse.ArgumentParser(description='Проверка орфографии с использованием нескольких сервисов')
    parser.add_argument('words', nargs='*', help='Слова или текст для проверки')
    parser.add_argument('-f', '--file', help='Файл с текстом для проверки')
    parser.add_argument('-i', '--interactive', action='store_true', help='Интерактивный режим')
    parser.add_argument('-v', '--verbose', action='store_true', help='Подробный вывод')
    
    args = parser.parse_args()
    
    checker = MultiSpellChecker()
    
    def process_text(text):
        if args.verbose:
            print(f"Исходный текст: {text}")
        
        corrected, method = checker.check_spelling(text)
        
        if method:
            if args.verbose:
                print(f"Исправлено через {method}: {corrected}")
            else:
                print(corrected)
        else:
            if args.verbose:
                print(f"Ошибок не найдено или сервисы недоступны: {text}")
            else:
                print(text)
    
    try:
        if args.interactive:
            print("Интерактивный режим проверки орфографии")
            print("Введите текст для проверки (или 'quit' для выхода):")
            
            while True:
                text = input("> ").strip()
                if text.lower() in ['quit', 'exit', 'q']:
                    break
                if text:
                    process_text(text)
                    print()
        
        elif args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                if text:
                    process_text(text)
                else:
                    print("Файл пуст")
            except FileNotFoundError:
                print(f"Ошибка: Файл '{args.file}' не найден")
                sys.exit(1)
        
        elif args.words:
            text = " ".join(args.words)
            process_text(text)
        
        else:
            # Читаем из stdin
            try:
                text = sys.stdin.read().strip()
                if text:
                    process_text(text)
                else:
                    print("Введите текст для проверки:")
                    text = input().strip()
                    if text:
                        process_text(text)
                    else:
                        print("Ошибка: Не введен текст для проверки")
                        sys.exit(1)
            except KeyboardInterrupt:
                print("\nПрограмма прервана пользователем")
                sys.exit(0)
    
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
