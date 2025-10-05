#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI приложение для проверки орфографии на macOS
Использует tkinter для создания интерфейса
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import threading
import json
from datetime import datetime


class SpellCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔤 Проверка орфографии")
        self.root.geometry("700x500")
        self.root.configure(bg='#f0f0f0')
        
        # Настройка сессии для запросов
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        self.setup_ui()
        
        # Центрируем окно
        self.center_window()
    
    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenwidth() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Заголовок
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=10, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🔤 ПРОВЕРКА ОРФОГРАФИИ", 
            font=('SF Pro Display', 18, 'bold'),
            fg='white', 
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Поле для ввода текста
        input_label = tk.Label(
            main_frame, 
            text="Введите текст для проверки:", 
            font=('SF Pro Display', 12),
            bg='#f0f0f0'
        )
        input_label.pack(anchor='w', pady=(5, 2))
        
        self.input_text = scrolledtext.ScrolledText(
            main_frame,
            height=6,
            font=('SF Pro Display', 11),
            wrap=tk.WORD,
            bg='white',
            relief='solid',
            borderwidth=1
        )
        self.input_text.pack(fill='x', pady=(0, 10))
        
        # Кнопки
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=(0, 10))
        
        self.check_button = tk.Button(
            button_frame,
            text="🔍 Проверить",
            command=self.check_spelling_async,
            bg='#3498db',
            fg='white',
            font=('SF Pro Display', 12, 'bold'),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.check_button.pack(side='left', padx=(0, 10))
        
        self.clear_button = tk.Button(
            button_frame,
            text="🗑️ Очистить",
            command=self.clear_text,
            bg='#95a5a6',
            fg='white',
            font=('SF Pro Display', 12),
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.clear_button.pack(side='left')
        
        # Прогресс-бар
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=(0, 10))
        
        # Результат
        result_label = tk.Label(
            main_frame,
            text="Результат:",
            font=('SF Pro Display', 12),
            bg='#f0f0f0'
        )
        result_label.pack(anchor='w', pady=(5, 2))
        
        self.result_text = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            font=('SF Pro Display', 11),
            wrap=tk.WORD,
            bg='#f8f9fa',
            relief='solid',
            borderwidth=1,
            state='disabled'
        )
        self.result_text.pack(fill='both', expand=True)
        
        # Статус-бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            bg='#ecf0f1',
            font=('SF Pro Display', 10)
        )
        status_bar.pack(fill='x', side='bottom')
    
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
    
    def check_spelling_async(self):
        """Асинхронная проверка орфографии"""
        text = self.input_text.get('1.0', tk.END).strip()
        
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст для проверки")
            return
        
        # Запускаем проверку в отдельном потоке
        thread = threading.Thread(target=self.check_spelling_thread, args=(text,))
        thread.daemon = True
        thread.start()
    
    def check_spelling_thread(self, text):
        """Проверка орфографии в отдельном потоке"""
        # Обновляем UI в главном потоке
        self.root.after(0, self.start_checking)
        
        # Проверяем орфографию
        corrected, errors_count, error = self.check_yandex_speller(text)
        
        # Обновляем результат в главном потоке
        self.root.after(0, self.finish_checking, text, corrected, errors_count, error)
    
    def start_checking(self):
        """Начало проверки - обновление UI"""
        self.check_button.config(state='disabled')
        self.progress.start()
        self.status_var.set("Проверяю орфографию...")
        
        # Очищаем результат
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.config(state='disabled')
    
    def finish_checking(self, original_text, corrected_text, errors_count, error):
        """Завершение проверки - обновление результата"""
        self.check_button.config(state='normal')
        self.progress.stop()
        
        self.result_text.config(state='normal')
        
        if error:
            self.result_text.insert(tk.END, f"❌ Ошибка: {error}\n\n")
            self.result_text.insert(tk.END, f"Исходный текст:\n{original_text}")
            self.status_var.set("Ошибка при проверке")
        
        elif errors_count > 0:
            self.result_text.insert(tk.END, f"✅ Найдено и исправлено ошибок: {errors_count}\n\n")
            self.result_text.insert(tk.END, f"Исправленный текст:\n{corrected_text}\n\n")
            self.result_text.insert(tk.END, f"Исходный текст:\n{original_text}")
            self.status_var.set(f"Исправлено ошибок: {errors_count}")
        
        else:
            self.result_text.insert(tk.END, f"✅ Ошибок не найдено!\n\n")
            self.result_text.insert(tk.END, f"Текст:\n{original_text}")
            self.status_var.set("Ошибок не найдено")
        
        self.result_text.config(state='disabled')
        
        # Добавляем время проверки
        current_time = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"{self.status_var.get()} ({current_time})")
    
    def clear_text(self):
        """Очистка полей"""
        self.input_text.delete('1.0', tk.END)
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.config(state='disabled')
        self.status_var.set("Поля очищены")


def main():
    """Запуск GUI приложения"""
    root = tk.Tk()
    
    # Настройки для macOS
    try:
        root.tk.call('tk', 'scaling', 2.0)  # Для Retina дисплеев
    except:
        pass
    
    app = SpellCheckerGUI(root)
    
    # Обработка закрытия окна
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Запуск приложения
    root.mainloop()


if __name__ == "__main__":
    main()
