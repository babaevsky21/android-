#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SpellChecker Android App
Приложение для проверки орфографии с простым интерфейсом
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

import requests
import threading
import json
from datetime import datetime


class SpellCheckerApp(App):
    def build(self):
        # Настройка окна
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # Главный контейнер
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10)
        )
        
        # Заголовок
        title = Label(
            text='🔤 Проверка орфографии',
            font_size=dp(24),
            size_hint_y=None,
            height=dp(60),
            color=(0.2, 0.2, 0.2, 1),
            bold=True
        )
        main_layout.add_widget(title)
        
        # Подзаголовок
        subtitle = Label(
            text='Введите текст с ошибками - получите исправленный вариант',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(40),
            color=(0.5, 0.5, 0.5, 1)
        )
        main_layout.add_widget(subtitle)
        
        # Поле ввода текста
        input_label = Label(
            text='Введите текст:',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(30),
            color=(0.3, 0.3, 0.3, 1),
            halign='left'
        )
        input_label.bind(size=input_label.setter('text_size'))
        main_layout.add_widget(input_label)
        
        self.text_input = TextInput(
            multiline=True,
            size_hint_y=None,
            height=dp(120),
            font_size=dp(16),
            hint_text='Например: превет как дила хароший ден',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1),
            cursor_color=(0.3, 0.6, 1, 1),
            padding=[dp(10), dp(10)]
        )
        main_layout.add_widget(self.text_input)
        
        # Кнопка проверки
        self.check_button = Button(
            text='🔍 Проверить орфографию',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(18),
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        self.check_button.bind(on_press=self.check_spelling)
        main_layout.add_widget(self.check_button)
        
        # Прогресс-бар
        self.progress = ProgressBar(
            size_hint_y=None,
            height=dp(4),
            opacity=0
        )
        main_layout.add_widget(self.progress)
        
        # Статус
        self.status_label = Label(
            text='Готов к работе',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30),
            color=(0.5, 0.5, 0.5, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Результат
        result_label = Label(
            text='Результат:',  
            font_size=dp(16),
            size_hint_y=None,
            height=dp(30),
            color=(0.3, 0.3, 0.3, 1),
            halign='left'
        )
        result_label.bind(size=result_label.setter('text_size'))
        main_layout.add_widget(result_label)
        
        # Поле результата в скролле
        scroll = ScrollView()
        
        self.result_label = Label(
            text='Здесь появится исправленный текст...',
            font_size=dp(16),
            color=(0.2, 0.2, 0.2, 1),
            text_size=(None, None),  
            halign='left',
            valign='top',
            markup=True
        )
        scroll.add_widget(self.result_label)
        main_layout.add_widget(scroll)
        
        # Кнопки действий
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        clear_button = Button(
            text='🗑️ Очистить',
            background_color=(0.8, 0.4, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        clear_button.bind(on_press=self.clear_text)
        
        copy_button = Button(
            text='📋 Копировать',
            background_color=(0.4, 0.8, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        copy_button.bind(on_press=self.copy_result)
        
        button_layout.add_widget(clear_button)
        button_layout.add_widget(copy_button)
        main_layout.add_widget(button_layout)
        
        # Инициализируем сессию для запросов
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Android 10; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0'
        })
        
        self.last_corrected_text = ""
        
        return main_layout
    
    def check_spelling(self, instance):
        """Запуск проверки орфографии"""
        text = self.text_input.text.strip()
        
        if not text:
            self.show_status("⚠️ Введите текст для проверки", error=True)
            return
        
        # Блокируем кнопку и показываем прогресс
        self.check_button.disabled = True
        self.check_button.text = "⏳ Проверяю..."
        self.progress.opacity = 1
        self.show_status("🔍 Проверяем орфографию...")
        
        # Запускаем проверку в отдельном потоке
        thread = threading.Thread(target=self.spell_check_thread, args=(text,))
        thread.daemon = True
        thread.start()
    
    def spell_check_thread(self, text):
        """Проверка орфографии в отдельном потоке"""
        try:
            # Проверяем через Яндекс.Спеллер
            corrected, errors_count, error = self.check_yandex_speller(text)
            
            # Обновляем UI в главном потоке
            Clock.schedule_once(
                lambda dt: self.on_spell_check_complete(text, corrected, errors_count, error),
                0
            )
            
        except Exception as e:
            Clock.schedule_once(
                lambda dt: self.on_spell_check_complete(text, text, 0, str(e)),
                0
            )
    
    def check_yandex_speller(self, text):
        """Проверка через Яндекс.Спеллер"""
        try:
            url = "https://speller.yandex.net/services/spellservice.json/checkText"
            params = {'text': text, 'lang': 'ru', 'options': 0}
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            corrected_text = text
            errors_count = len(result)
            
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
            
            return corrected_text, errors_count, None
            
        except Exception as e:
            return text, 0, str(e)
    
    def on_spell_check_complete(self, original_text, corrected_text, errors_count, error):
        """Обновление UI после завершения проверки"""
        # Восстанавливаем кнопку
        self.check_button.disabled = False
        self.check_button.text = "🔍 Проверить орфографию"
        self.progress.opacity = 0
        
        if error:
            self.show_status(f"❌ Ошибка: {error}", error=True)
            self.result_label.text = f"[color=#cc0000]❌ Ошибка проверки:[/color]\n{error}\n\n[color=#666666]Исходный текст:[/color]\n{original_text}"
        
        elif errors_count > 0:
            self.show_status(f"✅ Найдено и исправлено ошибок: {errors_count}")
            self.result_label.text = (
                f"[color=#00aa00]✅ Исправленный текст:[/color]\n"
                f"[size=18]{corrected_text}[/size]\n\n"
                f"[color=#666666]Исходный текст:[/color]\n"
                f"[size=14]{original_text}[/size]\n\n"
                f"[color=#0066cc]📊 Исправлено ошибок: {errors_count}[/color]"
            )
            self.last_corrected_text = corrected_text
        
        else:
            self.show_status("✅ Ошибок не найдено!")
            self.result_label.text = (
                f"[color=#00aa00]✅ Ошибок не найдено![/color]\n\n"
                f"[color=#666666]Ваш текст:[/color]\n"
                f"[size=18]{original_text}[/size]"
            )
            self.last_corrected_text = original_text
        
        # Обновляем размер текста для переноса строк
        self.result_label.text_size = (Window.width - dp(40), None)
    
    def show_status(self, message, error=False):
        """Показ статуса"""
        self.status_label.text = message
        if error:
            self.status_label.color = (0.8, 0.2, 0.2, 1)
        else:
            self.status_label.color = (0.2, 0.6, 0.2, 1)
    
    def clear_text(self, instance):
        """Очистка полей"""
        self.text_input.text = ""
        self.result_label.text = "Здесь появится исправленный текст..."
        self.last_corrected_text = ""
        self.show_status("Поля очищены")
    
    def copy_result(self, instance):
        """Копирование результата в буфер обмена"""
        if self.last_corrected_text:
            try:
                # Попытка скопировать в буфер обмена
                from kivy.core.clipboard import Clipboard
                Clipboard.copy(self.last_corrected_text)
                self.show_status("📋 Текст скопирован в буфер обмена")
            except:
                self.show_status("⚠️ Не удалось скопировать текст", error=True)
        else:
            self.show_status("⚠️ Нет текста для копирования", error=True)


if __name__ == '__main__':
    SpellCheckerApp().run()
