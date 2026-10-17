import tkinter as tk
from tkinter import messagebox, ttk

# --- БАЗА ДАННЫХ ТОВАРОВ ---
INITIAL_PRODUCTS = [
    {"id": 1, "name": "Air Max 270", "brand": "Nike", "category": "Спортивная", "price": 14990.00, "material": "Текстиль"},
    {"id": 2, "name": "Ultraboost Light", "brand": "Adidas", "category": "Спортивная", "price": 18500.00, "material": "Текстиль"},
    {"id": 3, "name": "Classic Oxford", "brand": "Ecco", "category": "Классическая", "price": 12300.00, "material": "Кожа"},
    {"id": 4, "name": "6-Inch Premium Boot", "brand": "Timberland", "category": "Зимняя", "price": 24900.00, "material": "Нубук"},
    {"id": 5, "name": "Chuck Taylor All Star", "brand": "Converse", "category": "Повседневная", "price": 8200.00, "material": "Хлопок"}
]

USERS = {
    "admin": {"password": "123", "role": "Администратор"},
    "manager": {"password": "123", "role": "Менеджер"}
}

# --- ЦВЕТОВЫЕ СТИЛИ И ПАЛИТРЫ ТЕМ ---
THEMES = {
    "Темная классика": {
        "bg": "#2A2F35", "fg": "#FFFFFF", "accent": "#1ABC9C", "card": "#34495E", "entry_bg": "#1F2326"
    },
    "Светлая корпоративная": {
        "bg": "#F5F7FA", "fg": "#2C3E50", "accent": "#2980B9", "card": "#FFFFFF", "entry_bg": "#EAECEE"
    },
    "Яркая черничная": {
        "bg": "#1F1A3A", "fg": "#FFFFFF", "accent": "#E91E63", "card": "#2D264D", "entry_bg": "#151126"
    },
    "Изумрудный город": {
        "bg": "#162B24", "fg": "#EAF2F0", "accent": "#2ECC71", "card": "#1F3D33", "entry_bg": "#0E1C17"
    },
    "Неоновый киберпанк": {
        "bg": "#0D0D0D", "fg": "#00FF66", "accent": "#FF007F", "card": "#1A1A1A", "entry_bg": "#111111"
    }
}

class ShoeStoreApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Информационная система: Магазин обуви")
        self.geometry("950x650")
        
        self.current_theme = "Темная классика"
        self.current_user = None
        self.current_role = None
        self.products = INITIAL_PRODUCTS.copy()
        
        # Движок современных стилей TTK
        self.style = ttk.Style()
        
        self.show_login_screen()

    def update_theme_engine(self):
        """Полная перерисовка всех стилей приложения без использования старых Tk-элементов."""
        colors = THEMES[self.current_theme]
        self.configure(bg=colors["bg"])
        
        self.style.theme_use("clam")
        
        # Стилизация стандартных панелей (ТТК Фреймы)
        self.style.configure("TFrame", background=colors["bg"])
        self.style.configure("Card.TFrame", background=colors["card"])
        self.style.configure("Top.TFrame", background=colors["card"])
        
        # Стилизация рамок с текстом (ТТК LabelFrame)
        self.style.configure("TLableFrame", background=colors["bg"], foreground=colors["accent"])
        self.style.configure("TLableFrame.Label", background=colors["bg"], foreground=colors["accent"], font=("Arial", 11, "bold"))
        
        # Стилизация текстовых надписей (ТТК Метки)
        self.style.configure("TLabel", background=colors["bg"], foreground=colors["fg"], font=("Arial", 10))
        self.style.configure("Top.TLabel", background=colors["card"], foreground=colors["fg"], font=("Arial", 10, "bold"))
        
        # Стилизация кнопок действий (ТТК Кнопки)
        self.style.configure("TButton", background=colors["card"], foreground=colors["fg"], bordercolor=colors["bg"], font=("Arial", 10, "bold"), focuscolor=colors["accent"])
        self.style.map("TButton", background=[("active", colors["accent"]), ("pressed", colors["accent"])], foreground=[("active", "#FFFFFF")])
        
        self.style.configure("Add.TButton", background="#2ECC71", foreground="#FFFFFF")
        self.style.map("Add.TButton", background=[("active", "#27AE60")])
        
        self.style.configure("Del.TButton", background="#E74C3C", foreground="#FFFFFF")
        self.style.map("Del.TButton", background=[("active", "#C0392B")])

        # Стилизация интерактивных выпадающих списков (ТТК Combobox)
        self.style.configure("TCombobox", fieldbackground=colors["entry_bg"], background=colors["card"], foreground=colors["fg"], arrowcolor=colors["accent"], bordercolor=colors["bg"])
        
        # Стилизация таблицы с товарами (Treeview)
        self.style.configure("Treeview", background=colors["card"], foreground=colors["fg"], fieldbackground=colors["card"], rowheight=25, bordercolor=colors["bg"], lightcolor=colors["bg"])
        self.style.map("Treeview", background=[("selected", colors["accent"])], foreground=[("selected", "#FFFFFF")])
        self.style.configure("Treeview.Heading", background=colors["bg"], foreground=colors["accent"], font=("Arial", 10, "bold"), bordercolor=colors["bg"])
        
        # Стилизация полос прокрутки
        self.style.configure("Vertical.TScrollbar", background=colors["card"], troughcolor=colors["bg"], bordercolor=colors["bg"], arrowcolor=colors["accent"])

    # ================= ФУНКЦИЯ 1: АВТОРИЗАЦИЯ =================
    def show_login_screen(self):
        self.clear_screen()
        self.update_theme_engine()
        colors = THEMES[self.current_theme]
        
        # Главный контейнер авторизации
        main_bg = ttk.Frame(self)
        main_bg.pack(fill="both", expand=True)
        
        login_frame = ttk.LabelFrame(main_bg, text=" Авторизация пользователя ", padding=20)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=250)
        
        ttk.Label(login_frame, text="Логин (admin / manager):").pack(anchor="w", pady=2)
        self.login_entry = tk.Entry(login_frame, font=("Arial", 11), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.login_entry.pack(fill="x", pady=5)
        
        ttk.Label(login_frame, text="Пароль (123):").pack(anchor="w", pady=2)
        self.password_entry = tk.Entry(login_frame, font=("Arial", 11), show="*", bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.password_entry.pack(fill="x", pady=5)
        
        btn_login = ttk.Button(login_frame, text="Войти в систему", command=self.handle_login)
        btn_login.pack(fill="x", pady=15)

    def handle_login(self):
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if username in USERS and USERS[username]["password"] == password:
            self.current_user = username
            self.current_role = USERS[username]["role"]
            messagebox.showinfo("Успех", f"Добро пожаловать, {username} ({self.current_role})!")
            self.show_main_screen()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

    # ================= ГЛАВНЫЙ ЭКРАН И ИНТЕРФЕЙС =================
    def show_main_screen(self):
        self.clear_screen()
        self.update_theme_engine()
        colors = THEMES[self.current_theme]
        
        # Верхняя панель управления (Информация о пользователе и темы)
        top_bar = ttk.Frame(self, style="Top.TFrame", height=50)
        top_bar.pack(fill="x", side="top", ipady=5, ipadx=10)
        
        lbl_user = ttk.Label(top_bar, text=f"👤 Пользователь: {self.current_user} ({self.current_role})", style="Top.TLabel")
        lbl_user.pack(side="left", padx=10, pady=10)
        
        btn_logout = ttk.Button(top_bar, text="Выйти", command=self.show_login_screen, style="TButton")
        btn_logout.pack(side="left", padx=15, pady=5)
        
        # Выпадающий список смены тем
        self.theme_combo = ttk.Combobox(top_bar, values=list(THEMES.keys()), state="readonly", width=22)
        self.theme_combo.set(self.current_theme)
        self.theme_combo.pack(side="right", padx=10, pady=5)
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        
        ttk.Label(top_bar, text="Тема оформления:", style="Top.TLabel").pack(side="right", padx=5, pady=5)
        
        # Главный контейнер рабочих панелей
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Левая панель: Настройки поиска и Фильтрации
        left_panel = ttk.LabelFrame(main_container, text=" Настройки поиска ", width=250, padding=10)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False) # Блокирует деформацию размеров
        
        ttk.Label(left_panel, text="Поиск по модели/бренду:").pack(anchor="w", pady=2)
        self.search_entry = tk.Entry(left_panel, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.search_entry.pack(fill="x", pady=5)
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_table())
        
        ttk.Label(left_panel, text="Фильтр по категории:").pack(anchor="w", pady=10)
        categories = ["Все категории"] + list(set(p["category"] for p in self.products))
        self.filter_category = ttk.Combobox(left_panel, values=categories, state="readonly")
        self.filter_category.set("Все категории")
        self.filter_category.pack(fill="x", pady=5)
        self.filter_category.bind("<<ComboboxSelected>>", lambda event: self.refresh_table())
        
        ttk.Label(left_panel, text="Максимальная цена (руб):").pack(anchor="w", pady=10)
        self.price_filter_entry = tk.Entry(left_panel, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.price_filter_entry.pack(fill="x", pady=5)
# ... (Завершение сборки левой панели поиска) ...
        self.price_filter_entry.bind("<KeyRelease>", lambda event: self.refresh_table())
        
        # Правая панель: Таблица товаров
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        table_frame = ttk.Frame(right_panel)
        table_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(table_frame, columns=("id", "name", "brand", "category", "price", "material"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название")
        self.tree.heading("brand", text="Бренд")
        self.tree.heading("category", text="Категория")
        self.tree.heading("price", text="Цена (руб.)")
        self.tree.heading("material", text="Материал")
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("price", width=110, anchor="e")
        self.tree.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill="y", side="right")
        
        # Нижняя панель действий (Управление каталогом)
        crud_frame = ttk.LabelFrame(right_panel, text=" Панель управления каталогом ", padding=10)
        crud_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        if self.current_role == "Администратор":
            btn_add = ttk.Button(crud_frame, text="➕ Добавить пару обуви", style="Add.TButton", command=self.open_add_window)
            btn_add.pack(side="left", padx=5)
            
            btn_delete = ttk.Button(crud_frame, text="❌ Удалить модель", style="Del.TButton", command=self.delete_product)
            btn_delete.pack(side="left", padx=5)
        else:
            lbl_restricted = ttk.Label(crud_frame, text="🔒 Изменение каталога доступна только Администраторам системы.", font=("Arial", 10, "italic"))
            lbl_restricted.pack(anchor="center")
            
        self.refresh_table()

    # ================= ЛОГИКА ТАБЛИЦЫ, ПОИСКА И ФИЛЬТРОВ =================
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        search_query = self.search_entry.get().lower().strip()
        selected_category = self.filter_category.get()
        max_price_str = self.price_filter_entry.get().strip()
        
        try:
            max_price = float(max_price_str) if max_price_str else float('inf')
        except ValueError:
            max_price = float('inf')
            
        for p in self.products:
            matches_search = (search_query in p["name"].lower() or search_query in p["brand"].lower())
            matches_category = (selected_category == "Все категории" or p["category"] == selected_category)
            matches_price = p["price"] <= max_price
            
            if matches_search and matches_category and matches_price:
                self.tree.insert("", "end", values=(p["id"], p["name"], p["brand"], p["category"], f"{p['price']:.2f}", p["material"]))

    # ================= ЛОГИКА ДОБАВЛЕНИЯ И УДАЛЕНИЯ =================
    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите товар в таблице для удаления!")
            return
            
        product_id = int(self.tree.item(selected_item)["values"][0])
        self.products = [p for p in self.products if p["id"] != product_id]
        messagebox.showinfo("Успех", "Товар успешно удален.")
        self.refresh_table()

    def open_add_window(self):
        self.add_win = tk.Toplevel(self)
        self.add_win.title("Добавление товара")
        self.add_win.geometry("360x420")
        self.add_win.grab_set()
        
        colors = THEMES[self.current_theme]
        self.add_win.configure(bg=colors["bg"])
        
        frame = ttk.Frame(self.add_win, padding=15)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Название модели:").pack(anchor="w")
        self.add_name = tk.Entry(frame, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.add_name.pack(fill="x", pady=3)
        
        ttk.Label(frame, text="Бренд:").pack(anchor="w")
        self.add_brand = tk.Entry(frame, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.add_brand.pack(fill="x", pady=3)
        
        ttk.Label(frame, text="Категория:").pack(anchor="w")
        self.add_cat = ttk.Combobox(frame, values=["Спортивная", "Классическая", "Зимняя", "Повседневная"], state="readonly")
        self.add_cat.pack(fill="x", pady=3)
        
        ttk.Label(frame, text="Цена (руб):").pack(anchor="w")
        self.add_price = tk.Entry(frame, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.add_price.pack(fill="x", pady=3)
        
        ttk.Label(frame, text="Материал:").pack(anchor="w")
        self.add_mat = tk.Entry(frame, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.add_mat.pack(fill="x", pady=3)
        
        btn_save = ttk.Button(frame, text="💾 Сохранить в базу", command=self.save_new_product)
        btn_save.pack(fill="x", pady=20)

    def save_new_product(self):
        try:
            name = self.add_name.get().strip()
            brand = self.add_brand.get().strip()
            category = self.add_cat.get()
            price = float(self.add_price.get().strip())
            material = self.add_mat.get().strip()
            
            if not (name and brand and category and material):
                raise ValueError()
                
            new_id = max(p["id"] for p in self.products) + 1 if self.products else 1
            self.products.append({
                "id": new_id, "name": name, "brand": brand, "category": category, "price": price, "material": material
            })
            
            messagebox.showinfo("Успех", "Товар успешно добавлен!")
            self.add_win.destroy()
            self.show_main_screen()
            
        except ValueError:
            messagebox.showerror("Ошибка валидации", "Заполните все поля! Поле 'Цена' должно содержать число.")

    def change_theme(self, event):
        self.current_theme = self.theme_combo.get()
        self.show_main_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

# Исправлено: корректные двойные подчеркивания для системной переменной
if __name__ == "__main__":
    app = ShoeStoreApp()
    app.mainloop()
