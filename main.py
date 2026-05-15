# -*- coding: utf-8 -*-
"""
Лабораторная работа 1: Шифр Цезаря
Оконное приложение на Tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

RU_ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
EN_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

RU_FREQ = {
    'о': 10.97, 'а': 8.01, 'и': 7.35, 'е': 7.18, 'н': 6.62,
    'т': 6.26, 'с': 5.47, 'р': 4.73, 'в': 4.68, 'л': 4.35,
    'к': 3.49, 'м': 3.17, 'д': 2.98, 'п': 2.79, 'у': 2.61,
    'я': 2.02, 'ы': 1.90, 'з': 1.68, 'ь': 1.62, 'г': 1.57,
    'ч': 1.44, 'й': 1.21, 'х': 0.97, 'ж': 0.94, 'ш': 0.73,
    'ю': 0.64, 'ц': 0.45, 'щ': 0.36, 'э': 0.32, 'ф': 0.26,
    'ъ': 0.04, 'ё': 0.00
}

class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифр Цезаря")
        self.root.geometry("850x700")
        self.root.resizable(True, True)
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.encrypt_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.encrypt_frame, text='Шифрование/Расшифрование')
        
        self.crack_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.crack_frame, text='Взлом шифра')
        
        self.create_encrypt_tab()
        self.create_crack_tab()

    def create_encrypt_tab(self):
        title_label = ttk.Label(self.encrypt_frame, text="Шифр Цезаря", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        input_frame = ttk.LabelFrame(self.encrypt_frame, text="Входной текст", padding=10)
        input_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=6, 
                                                    font=('Arial', 11), wrap=tk.WORD)
        self.input_text.pack(fill='both', expand=True)
        self.create_context_menu(self.input_text)
        
        settings_frame = ttk.Frame(self.encrypt_frame)
        settings_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(settings_frame, text="Ключ сдвига:").grid(row=0, column=0, 
                                                           padx=5, pady=5, sticky='e')
        self.key_entry = ttk.Entry(settings_frame, width=10)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.key_entry.insert(0, "3")
        
        ttk.Label(settings_frame, text="Режим:").grid(row=0, column=2, 
                                                     padx=10, pady=5, sticky='e')
        self.mode_var = tk.StringVar(value="encrypt")
        ttk.Radiobutton(settings_frame, text="Зашифровать", 
                       variable=self.mode_var, value="encrypt").grid(row=0, column=3, 
                                                                     padx=5, pady=5)
        ttk.Radiobutton(settings_frame, text="Расшифровать", 
                       variable=self.mode_var, value="decrypt").grid(row=0, column=4, 
                                                                     padx=5, pady=5)
        
        btn_frame = ttk.Frame(self.encrypt_frame)
        btn_frame.pack(pady=10)
        
        self.process_btn = ttk.Button(btn_frame, text="Выполнить", 
                                     command=self.process_text, width=20)
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="Очистить", 
                                   command=self.clear_encrypt_tab, width=20)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        result_frame = ttk.LabelFrame(self.encrypt_frame, text="Результат", padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        result_text_frame = ttk.Frame(result_frame)
        result_text_frame.pack(fill='both', expand=True)
        
        self.result_text = scrolledtext.ScrolledText(result_text_frame, height=6, 
                                                    font=('Arial', 11), wrap=tk.WORD)
        self.result_text.pack(side=tk.LEFT, fill='both', expand=True)
        self.create_context_menu(self.result_text)
        
        copy_btn_frame = ttk.Frame(result_text_frame)
        copy_btn_frame.pack(side=tk.RIGHT, fill='y', padx=5)
        
        self.copy_result_btn = ttk.Button(copy_btn_frame, text="📋 Копировать\nрезультат", 
                                         command=self.copy_result, width=15)
        self.copy_result_btn.pack(pady=5)
        
        self.key_info_label = ttk.Label(self.encrypt_frame, text="", 
                                       font=('Arial', 10, 'italic'))
        self.key_info_label.pack(pady=5)

    def create_crack_tab(self):
        title_label = ttk.Label(self.crack_frame, text="Взлом шифра Цезаря\n(метод наименьших квадратов)", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        desc_label = ttk.Label(self.crack_frame, 
                              text="Введите зашифрованный русский текст для автоматического взлома",
                              font=('Arial', 10))
        desc_label.pack(pady=5)
        
        input_frame = ttk.LabelFrame(self.crack_frame, text="Зашифрованный текст", padding=10)
        input_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.crack_input = scrolledtext.ScrolledText(input_frame, height=4, 
                                                    font=('Arial', 11), wrap=tk.WORD)
        self.crack_input.pack(fill='both', expand=True)
        self.create_context_menu(self.crack_input)
        
        self.crack_btn = ttk.Button(self.crack_frame, text="Взломать шифр", 
                                   command=self.crack_cipher, width=30)
        self.crack_btn.pack(pady=10)
        
        result_frame = ttk.LabelFrame(self.crack_frame, text="Результат взлома", padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        result_text_frame = ttk.Frame(result_frame)
        result_text_frame.pack(fill='both', expand=True)
        
        self.crack_result = scrolledtext.ScrolledText(result_text_frame, height=10, 
                                                     font=('Arial', 11), wrap=tk.WORD)
        self.crack_result.pack(side=tk.LEFT, fill='both', expand=True)
        self.create_context_menu(self.crack_result)
        
        copy_crack_btn_frame = ttk.Frame(result_text_frame)
        copy_crack_btn_frame.pack(side=tk.RIGHT, fill='y', padx=5)
        
        self.copy_crack_btn = ttk.Button(copy_crack_btn_frame, text="📋 Копировать\nрезультат", 
                                        command=self.copy_crack_result, width=15)
        self.copy_crack_btn.pack(pady=5)

    def create_context_menu(self, widget):
        context_menu = tk.Menu(widget, tearoff=0)
        context_menu.add_command(label="✂ Вырезать", command=lambda: widget.event_generate('<<Cut>>'))
        context_menu.add_command(label="📋 Копировать", command=lambda: widget.event_generate('<<Copy>>'))
        context_menu.add_command(label="📥 Вставить", command=lambda: widget.event_generate('<<Paste>>'))
        context_menu.add_separator()
        context_menu.add_command(label="🗑 Удалить всё", command=lambda: widget.delete('1.0', tk.END))
        context_menu.add_command(label="✅ Выделить всё", command=lambda: widget.tag_add(tk.SEL, '1.0', tk.END))
        widget.bind('<Button-3>', lambda e: self.show_context_menu(e, context_menu))
    
    def show_context_menu(self, event, menu):
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def copy_result(self):
        result = self.result_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Копирование", "Результат скопирован в буфер обмена!")
    
    def copy_crack_result(self):
        result = self.crack_result.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Копирование", "Результат взлома скопирован в буфер обмена!")
    
    def clean_text(self, text):
        text = text.replace('Ё', 'Е').replace('ё', 'е')
        cleaned = ''
        for char in text:
            char_lower = char.lower()
            if char_lower in RU_ALPHABET or char_lower in EN_ALPHABET:
                cleaned += char_lower
        return cleaned
    
    def shift_char(self, char, key, alphabet):
        index = alphabet.index(char)
        new_index = (index + key) % len(alphabet)
        return alphabet[new_index]
    
    def encrypt(self, text, key):
        text = self.clean_text(text)
        result = ''
        for char in text:
            if char in RU_ALPHABET:
                result += self.shift_char(char, key, RU_ALPHABET)
            elif char in EN_ALPHABET:
                result += self.shift_char(char, key, EN_ALPHABET)
        return result
    
    def decrypt(self, text, key):
        result = ''
        for char in text:
            if char in RU_ALPHABET:
                index = RU_ALPHABET.index(char)
                new_index = (index - key) % len(RU_ALPHABET)
                result += RU_ALPHABET[new_index]
            elif char in EN_ALPHABET:
                index = EN_ALPHABET.index(char)
                new_index = (index - key) % len(EN_ALPHABET)
                result += EN_ALPHABET[new_index]
            else:
                result += char
        return result
    
    def format_groups(self, text):
        groups = []
        for i in range(0, len(text), 5):
            groups.append(text[i:i+5])
        return ' '.join(groups)
    
    def count_frequencies(self, text):
        counts = {}
        for char in text:
            if char in RU_ALPHABET:
                counts[char] = counts.get(char, 0) + 1
        
        total = len(text)
        if total == 0:
            return {}
        
        frequencies = {}
        for char, count in counts.items():
            frequencies[char] = (count / total) * 100
        
        return frequencies
    
    def validate_key(self, key_input):
        try:
            key = int(key_input)
            key = key % 32
            return key, True
        except ValueError:
            return 0, False
    
    def process_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст!")
            return
        
        key_input = self.key_entry.get().strip()
        key, valid = self.validate_key(key_input)
        
        if not valid:
            messagebox.showerror("Ошибка", "Ключ должен быть числом!")
            return
        
        mode = self.mode_var.get()
        if mode == "encrypt":
            result = self.encrypt(text, key)
            formatted = self.format_groups(result)
        else:
            cleaned = self.clean_text(text)
            result = self.decrypt(cleaned, key)
            formatted = self.format_groups(result)
        
        self.result_text.config(state='normal')
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", formatted)
        
        self.key_info_label.config(text=f"Использован ключ: {key}")
    
    def clear_encrypt_tab(self):
        self.input_text.delete("1.0", tk.END)
        self.result_text.config(state='normal')
        self.result_text.delete("1.0", tk.END)
        self.key_info_label.config(text="")
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, "3")
    
    def crack_cipher(self):
        text = self.crack_input.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Предупреждение", "Введите зашифрованный текст!")
            return
        
        cleaned = self.clean_text(text)
        
        if not any(c in RU_ALPHABET for c in cleaned):
            messagebox.showerror("Ошибка", "Текст должен содержать русские буквы!")
            return
        
        best_key = 0
        min_error = float('inf')
        results = []
        
        for key in range(32):
            decrypted = self.decrypt(cleaned, key)
            freq = self.count_frequencies(decrypted)
            
            error = 0
            for char in RU_ALPHABET:
                actual_freq = freq.get(char, 0)
                expected_freq = RU_FREQ.get(char, 0)
                error += (actual_freq - expected_freq) ** 2
            
            results.append((key, error, decrypted[:50]))
            
            if error < min_error:
                min_error = error
                best_key = key
        
        best_decrypted = self.decrypt(cleaned, best_key)
        formatted = self.format_groups(best_decrypted)
        
        output = "=== РЕЗУЛЬТАТЫ ПЕРЕБОРА ===\n\n"
        output += f"{'Ключ':<8}{'Ошибка':<15}{'Текст (начало)':<40}\n"
        output += "-" * 65 + "\n"
        
        sorted_results = sorted(results, key=lambda x: x[1])[:5]
        for key, error, preview in sorted_results:
            marker = " ← ЛУЧШИЙ" if key == best_key else ""
            output += f"{key:<8}{error:<15.2f}{preview:<40}{marker}\n"
        
        output += "\n" + "=" * 65 + "\n"
        output += f"\n✓ НАЙДЕН ЛУЧШИЙ КЛЮЧ: {best_key}\n\n"
        output += "✓ РАСШИФРОВАННЫЙ ТЕКСТ (группами по 5):\n"
        output += formatted + "\n\n"
        output += "✓ ПОЛНЫЙ ТЕКСТ:\n"
        output += best_decrypted
        
        self.crack_result.config(state='normal')
        self.crack_result.delete("1.0", tk.END)
        self.crack_result.insert("1.0", output)

if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherApp(root)
    root.mainloop()
