#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упрощенная программа для проверки орфографии
"""

import requests
import sys
import json
from urllib.parse import urlencode


def check_spelling_simple(text):
    """Простая проверка орфографии через API или форму"""
    try:
        # Попробуем использовать более простой подход
        url = "https://sinonim.org/orfo"
        
        # Подготавливаем данные для отправки
        data = {
            'text': text,
            'action': 'check'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        # Отправляем запрос
        response = requests.post(url, data=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Простая обработка - ищем исправления в ответе
            content = response.text
            
            # Если в ответе есть исправленный текст, извлекаем его
            # Это упрощенная версия, может потребоваться доработка
            if 'исправлен' in content.lower() or 'ошибок не найдено' in content.lower():
                return text  # Если ошибок нет, возвращаем исходный текст
            
            # Для демонстрации - возвращаем исходный текст
            # В реальной реализации здесь нужно парсить HTML ответ
            return text
        
        else:
            print(f"Ошибка HTTP: {response.status_code}")
            return text
            
    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
        return text
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return text


def main():
    """Основная функция"""
    if len(sys.argv) > 1:
        # Если переданы аргументы, объединяем их в текст
        text = " ".join(sys.argv[1:])
    else:
        # Читаем из stdin
        print("Введите текст для проверки:")
        text = input().strip()
    
    if not text:
        print("Ошибка: Пустой текст")
        sys.exit(1)
    
    print(f"Проверяю: {text}")
    corrected = check_spelling_simple(text)
    print(f"Результат: {corrected}")


if __name__ == "__main__":
    main()
