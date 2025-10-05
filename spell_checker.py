#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Программа для проверки орфографии с использованием сайта sinonim.org/orfo
"""

import requests
import sys
import argparse
from bs4 import BeautifulSoup
import time


class SpellChecker:
    def __init__(self):
        self.url = "https://sinonim.org/orfo"
        self.session = requests.Session()
        # Заголовки для имитации браузера
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def get_form_data(self):
        """Получает данные формы с сайта"""
        try:
            response = self.session.get(self.url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ищем форму или текстовое поле для ввода
            form = soup.find('form')
            form_data = {}
            
            if form:
                # Находим скрытые поля формы
                for input_tag in form.find_all('input', type='hidden'):
                    name = input_tag.get('name')
                    value = input_tag.get('value', '')
                    if name:
                        form_data[name] = value
                        
                # Ищем CSRF токен или другие важные поля
                csrf_token = soup.find('meta', {'name': 'csrf-token'})
                if csrf_token:
                    form_data['_token'] = csrf_token.get('content', '')
                    
            return form_data
            
        except requests.RequestException as e:
            raise Exception(f"Ошибка при получении формы: {e}")

    def check_spelling(self, text):
        """Проверяет орфографию текста"""
        try:
            # Получаем данные формы
            form_data = self.get_form_data()
            
            # Добавляем текст для проверки
            form_data['text'] = text
            form_data['action'] = 'check'  # Добавляем действие
            
            # Отправляем POST запрос
            response = self.session.post(self.url, data=form_data, timeout=30)
            response.raise_for_status()
            
            # Парсим ответ
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ищем результат проверки в различных возможных местах
            corrected_text = None
            
            # Вариант 1: результат в div с классом result
            result_div = soup.find('div', {'class': 'result'}) or soup.find('div', {'id': 'result'})
            if result_div:
                corrected_text = result_div.get_text(strip=True)
            
            # Вариант 2: результат в textarea
            if not corrected_text:
                result_textarea = soup.find('textarea')
                if result_textarea and result_textarea.get_text(strip=True):
                    corrected_text = result_textarea.get_text(strip=True)
            
            # Вариант 3: ищем в структуре страницы по специфическим паттернам
            if not corrected_text:
                # Ищем все div-ы с текстом и находим наиболее подходящий
                all_divs = soup.find_all('div')
                for div in all_divs:
                    div_text = div.get_text(strip=True)
                    if div_text and len(div_text) > 10 and text.lower() in div_text.lower():
                        corrected_text = div_text
                        break
            
            # Если ничего не найдено, пробуем найти JSON ответ
            if not corrected_text:
                scripts = soup.find_all('script')
                for script in scripts:
                    script_content = script.string
                    if script_content and 'corrected' in script_content.lower():
                        # Пытаемся извлечь исправленный текст из JavaScript
                        import re
                        match = re.search(r'"corrected":\s*"([^"]*)"', script_content)
                        if match:
                            corrected_text = match.group(1)
                            break
            
            # Если всё ещё не найдено, возвращаем исходный текст с предупреждением
            if not corrected_text:
                print(f"Предупреждение: Результат проверки не найден. Возможно, текст не содержит ошибок или сайт изменил структуру.")
                return text
            
            return corrected_text if corrected_text.strip() else text
            
        except requests.RequestException as e:
            raise Exception(f"Ошибка при отправке запроса: {e}")
        except Exception as e:
            raise Exception(f"Ошибка при обработке ответа: {e}")

    def check_multiple_words(self, words):
        """Проверяет список слов"""
        text = " ".join(words)
        return self.check_spelling(text)


def main():
    parser = argparse.ArgumentParser(description='Проверка орфографии с использованием sinonim.org/orfo')
    parser.add_argument('words', nargs='*', help='Слова для проверки')
    parser.add_argument('-f', '--file', help='Файл с текстом для проверки')
    parser.add_argument('-i', '--interactive', action='store_true', help='Интерактивный режим')
    
    args = parser.parse_args()
    
    checker = SpellChecker()
    
    try:
        if args.interactive:
            print("Интерактивный режим проверки орфографии")
            print("Введите текст для проверки (или 'quit' для выхода):")
            
            while True:
                text = input("> ").strip()
                if text.lower() in ['quit', 'exit', 'q']:
                    break
                if text:
                    try:
                        corrected = checker.check_spelling(text)
                        print(f"Исправленный текст: {corrected}")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                    print()
        
        elif args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                if text:
                    corrected = checker.check_spelling(text)
                    print(corrected)
                else:
                    print("Файл пуст")
            except FileNotFoundError:
                print(f"Ошибка: Файл '{args.file}' не найден")
                sys.exit(1)
            except Exception as e:
                print(f"Ошибка при чтении файла: {e}")
                sys.exit(1)
        
        elif args.words:
            corrected = checker.check_multiple_words(args.words)
            print(corrected)
        
        else:
            # Читаем из stdin
            try:
                text = sys.stdin.read().strip()
                if text:
                    corrected = checker.check_spelling(text)
                    print(corrected)
                else:
                    print("Ошибка: Не введен текст для проверки")
                    parser.print_help()
                    sys.exit(1)
            except KeyboardInterrupt:
                print("\nПрограмма прервана пользователем")
                sys.exit(0)
    
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
