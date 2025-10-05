#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Альтернативная программа для проверки орфографии
Использует API или другие методы проверки
"""

import sys
import requests
import json
from urllib.parse import quote


def check_spelling_yandex_speller(text):
    """Проверка орфографии через Яндекс.Спеллер API"""
    try:
        url = "https://speller.yandex.net/services/spellservice.json/checkText"
        params = {
            'text': text,
            'lang': 'ru',
            'options': 0
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        corrected_text = text
        
        # Применяем исправления
        offset = 0
        for error in result:
            if 's' in error and error['s']:  # есть предложения исправлений
                pos = error['pos'] + offset
                length = error['len']
                word = error['word']
                suggestion = error['s'][0]  # берем первое предложение
                
                # Заменяем слово в тексте
                corrected_text = (corrected_text[:pos] + 
                                suggestion + 
                                corrected_text[pos + length:])
                
                # Корректируем смещение для следующих замен
                offset += len(suggestion) - length
        
        return corrected_text
        
    except Exception as e:
        print(f"Ошибка при проверке через Яндекс.Спеллер: {e}")
        return text


def check_spelling_languagetool(text):
    """Проверка орфографии через LanguageTool API"""
    try:
        url = "https://api.languagetool.org/v2/check"
        data = {
            'text': text,
            'language': 'ru-RU'
        }
        
        response = requests.post(url, data=data, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        corrected_text = text
        
        # Применяем исправления (в обратном порядке, чтобы не сбить позиции)
        for match in reversed(result.get('matches', [])):
            if match.get('replacements'):
                offset = match['offset']
                length = match['length']
                replacement = match['replacements'][0]['value']
                
                corrected_text = (corrected_text[:offset] + 
                                replacement + 
                                corrected_text[offset + length:])
        
        return corrected_text
        
    except Exception as e:
        print(f"Ошибка при проверке через LanguageTool: {e}")
        return text


def main():
    """Основная функция"""
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        print("Введите текст для проверки:")
        text = input().strip()
    
    if not text:
        print("Ошибка: Пустой текст")
        sys.exit(1)
    
    print(f"Исходный текст: {text}")
    
    # Пробуем разные API для проверки
    corrected = None
    
    # Сначала пробуем Яндекс.Спеллер
    try:
        corrected = check_spelling_yandex_speller(text)
        if corrected != text:
            print(f"Исправленный текст (Яндекс.Спеллер): {corrected}")
            return
    except:
        pass
    
    # Если Яндекс не сработал, пробуем LanguageTool
    try:
        corrected = check_spelling_languagetool(text)
        if corrected != text:
            print(f"Исправленный текст (LanguageTool): {corrected}")
            return
    except:
        pass
    
    # Если ничего не сработало
    if corrected == text or corrected is None:
        print(f"Ошибок не найдено или сервисы недоступны: {text}")


if __name__ == "__main__":
    main()
