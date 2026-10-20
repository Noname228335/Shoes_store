import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "shoe_store.db"

# --- ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ ---
def init_db():
    """Создает базу данных и таблицы, если они еще не существуют."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Таблица товаров
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            material TEXT NOT NULL
        )
    ''')
    
    # Добавляем стандартных пользователей, если таблица пуста
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            [("admin", "123", "Администратор"), ("manager", "123", "Менеджер")]
        )
        
    # Добавляем стартовые товары, если таблица пуста
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        initial_products = [
            ("Air Max 270", "Nike", "Спортивная", 14990.00, "Текстиль"),
            ("Ultraboost Light", "Adidas", "Спортивная", 18500.00, "Текстиль"),
            ("Classic Oxford", "Ecco", "Классическая", 12300.00, "Кожа"),
            ("6-Inch Premium Boot", "Timberland", "Зимняя", 24900.00, "Нубук"),
            ("Chuck Taylor All Star", "Converse", "Повседневная", 8200.00, "Хлопок")
        ]
        cursor.executemany(
            "INSERT INTO products (name, brand, category, price, material) VALUES (?, ?, ?, ?, ?)",
            initial_products
        )
        
    conn.commit()
    conn.close()


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
        self.geometry("1000x650")
        
        self.current_theme = "Темная классика"
        self.current_user = None
        self.current_role = None
        
        self.style = ttk.Style()
        self.show_login_screen()

    def update_theme_engine(self):
        """Полная перерисовка всех стилей приложения."""
        colors = THEMES[self.current_theme]
        self.configure(bg=colors["bg"])
        self.style.theme_use("clam")
        
        self.style.configure("TFrame", background=colors["bg"])
        self.style.configure("Card.TFrame", background=colors["card"])
        self.style.configure("Top.TFrame", background=colors["card"])
        
        self.style.configure("TLabelframe", background=colors["bg"], foreground=colors["accent"])
        self.style.configure("TLabelframe.Label", background=colors["bg"], foreground=colors["accent"], font=("Arial", 11, "bold"))
        
        self.style.configure("TLabel", background=colors["bg"], foreground=colors["fg"], font=("Arial", 10))
        self.style.configure("Top.TLabel", background=colors["card"], foreground=colors["fg"], font=("Arial", 10, "bold"))
        
        self.style.configure("TButton", background=colors["card"], foreground=colors["fg"], bordercolor=colors["bg"], font=("Arial", 10, "bold"), focuscolor=colors["accent"])
        self.style.map("TButton", background=[("active", colors["accent"]), ("pressed", colors["accent"])], foreground=[("active", "#FFFFFF")])
        
        self.style.configure("Add.TButton", background="#2ECC71", foreground="#FFFFFF")
        self.style.map("Add.TButton", background=[("active", "#27AE60")])
        
        self.style.configure("Del.TButton", background="#E74C3C", foreground="#FFFFFF")
        self.style.map("Del.TButton", background=[("active", "#C0392B")])

        self.style.configure("TCombobox", fieldbackground=colors["entry_bg"], background=colors["card"], foreground=colors["fg"], arrowcolor=colors["accent"], bordercolor=colors["bg"])
        
        self.style.configure("Treeview", background=colors["card"], foreground=colors["fg"], fieldbackground=colors["card"], rowheight=25, bordercolor=colors["bg"], lightcolor=colors["bg"])
        self.style.map("Treeview", background=[("selected", colors["accent"])], foreground=[("selected", "#FFFFFF")])
        self.style.configure("Treeview.Heading", background=colors["bg"], foreground=colors["accent"], font=("Arial", 10, "bold"), bordercolor=colors["bg"])
        
        self.style.configure("Vertical.TScrollbar", background=colors["card"], troughcolor=colors["bg"], bordercolor=colors["bg"], arrowcolor=colors["accent"])

    # ================= ЭКРАН 1: АВТОРИЗАЦИЯ =================
    def show_login_screen(self):
        self.clear_screen()
        self.update_theme_engine()
        colors = THEMES[self.current_theme]
        
        main_bg = ttk.Frame(self)
        main_bg.pack(fill="both", expand=True)
        
        login_frame = ttk.LabelFrame(main_bg, text=" Авторизация пользователя ", padding=20)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=300)
        
        ttk.Label(login_frame, text="Логин:").pack(anchor="w", pady=2)
        self.login_entry = tk.Entry(login_frame, font=("Arial", 11), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.login_entry.pack(fill="x", pady=5)
        
        ttk.Label(login_frame, text="Пароль:").pack(anchor="w", pady=2)
        self.password_entry = tk.Entry(login_frame, font=("Arial", 11), show="*", bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.password_entry.pack(fill="x", pady=5)
        
        btn_login = ttk.Button(login_frame, text="Войти в систему", command=self.handle_login)
        btn_login.pack(fill="x", pady=(15, 5))
        
        btn_reg_screen = ttk.Button(login_frame, text="Зарегистрироваться", command=self.show_register_screen)
        btn_reg_screen.pack(fill="x", pady=5)

    def handle_login(self):
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.current_user = username
            self.current_role = result[0]
            messagebox.showinfo("Успех", f"Добро пожаловать, {username} ({self.current_role})!")
            self.show_main_screen()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

    # ================= ЭКРАН 2: РЕГИСТРАЦИЯ =================
    def show_register_screen(self):
        self.clear_screen()
        colors = THEMES[self.current_theme]
        
        main_bg = ttk.Frame(self)
        main_bg.pack(fill="both", expand=True)
        
        reg_frame = ttk.LabelFrame(main_bg, text=" Регистрация нового аккаунта ", padding=20)
        reg_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=340)
        
        ttk.Label(reg_frame, text="Придумайте логин:").pack(anchor="w", pady=2)
        self.reg_login_entry = tk.Entry(reg_frame, font=("Arial", 11), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.reg_login_entry.pack(fill="x", pady=5)
        
        ttk.Label(reg_frame, text="Придумайте пароль:").pack(anchor="w", pady=2)
        self.reg_password_entry = tk.Entry(reg_frame, font=("Arial", 11), show="*", bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.reg_password_entry.pack(fill="x", pady=5)
        
        ttk.Label(reg_frame, text="Выберите роль в системе:").pack(anchor="w", pady=2)
        self.reg_role_combo = ttk.Combobox(reg_frame, values=["Менеджер", "Администратор"], state="readonly")
        self.reg_role_combo.set("Менеджер")
        self.reg_role_combo.pack(fill="x", pady=5)
        
        btn_do_reg = ttk.Button(reg_frame, text="Создать аккаунт", style="Add.TButton", command=self.handle_registration)
        btn_do_reg.pack(fill="x", pady=(15, 5))
        
        btn_back = ttk.Button(reg_frame, text="Назад к авторизации", command=self.show_login_screen)
        btn_back.pack(fill="x", pady=5)

    def handle_registration(self):
        username = self.reg_login_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        role = self.reg_role_combo.get()
        
        if not username or not password:
            messagebox.showwarning("Ошибка ввода", "Все поля должны быть заполнены!")
            return
            
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            # Пытаемся вставить пользователя в базу данных
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            messagebox.showinfo("Успех", f"Пользователь {username} успешно зарегистрирован в базе данных!")
            conn.close()
            self.show_login_screen()
        except sqlite3.IntegrityError:
            # Ошибка сработает, если username нарушает UNIQUE ограничение
            conn.close()
            messagebox.showerror("Ошибка", f"Логин '{username}' уже занят! Выберите другой.")

    # ================= ГЛАВНЫЙ ЭКРАН И ИНТЕРФЕЙС =================
    def show_main_screen(self):
        self.clear_screen()
        self.update_theme_engine()
        colors = THEMES[self.current_theme]
        
        top_bar = ttk.Frame(self, style="Top.TFrame", height=50)
        top_bar.pack(fill="x", side="top", ipady=5, ipadx=10)
        
        lbl_user = ttk.Label(top_bar, text=f"👤 Пользователь: {self.current_user} ({self.current_role})", style="Top.TLabel")
        lbl_user.pack(side="left", padx=10, pady=10)
        
        btn_logout = ttk.Button(top_bar, text="Выйти", command=self.show_login_screen, style="TButton")
        btn_logout.pack(side="left", padx=15, pady=5)
        
        self.theme_combo = ttk.Combobox(top_bar, values=list(THEMES.keys()), state="readonly", width=22)
        self.theme_combo.set(self.current_theme)
        self.theme_combo.pack(side="right", padx=10, pady=5)
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        
        ttk.Label(top_bar, text="Тема оформления:", style="Top.TLabel").pack(side="right", padx=5, pady=5)
        
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        form_frame = ttk.LabelFrame(left_panel, text=" Управление каталогом ", padding=15)
        form_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(form_frame, text="Название обуви:").pack(anchor="w")
        self.entry_name = tk.Entry(form_frame, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], bd=1)
        self.entry_name.pack(fill="x", pady=(2, 8))
        
        ttk.Label(form_frame, text="Бренд:").pack(anchor="w")
        self.entry_brand = tk.Entry(form_frame, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], bd=1)
        self.entry_brand.pack(fill="x", pady=(2, 8))
        
        ttk.Label(form_frame, text="Категория:").pack(anchor="w")
        self.combo_category = ttk.Combobox(form_frame, values=["Спортивная", "Классическая", "Зимняя", "Повседневная", "Летняя"], state="readonly")
        self.combo_category.pack(fill="x", pady=(2, 8))
        
        ttk.Label(form_frame, text="Материал:").pack(anchor="w")
        self.entry_material = tk.Entry(form_frame, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], bd=1)
        self.entry_material.pack(fill="x", pady=(2, 8))
        
        ttk.Label(form_frame, text="Цена (руб):").pack(anchor="w")
        self.entry_price = tk.Entry(form_frame, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], bd=1)
        self.entry_price.pack(fill="x", pady=(2, 12))
        
        btn_add = ttk.Button(form_frame, text="➕ Добавить товар", style="Add.TButton", command=self.add_product)
        btn_add.pack(fill="x", pady=2)
        
        btn_del = ttk.Button(form_frame, text="❌ Удалить выбранный", style="Del.TButton", command=self.delete_product)
        btn_del.pack(fill="x", pady=5)
        
        if self.current_role != "Администратор":
            btn_add.configure(state="disabled")
            btn_del.configure(state="disabled")
            ttk.Label(form_frame, text="*Изменения доступны\nтолько Администратору", foreground="orange", font=("Arial", 9, "italic")).pack(pady=5)
            
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side="right", fill="both", expand=True)
        
        filter_frame = ttk.Frame(right_panel)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(filter_frame, text="🔍 Быстрый поиск:").pack(side="left", padx=(0, 10))
        self.entry_search = tk.Entry(filter_frame, font=("Arial", 10), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], bd=1)
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_search.bind("<KeyRelease>", self.refresh_table)
        
        table_frame = ttk.Frame(right_panel)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("id", "name", "brand", "category", "material", "price")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Модель")
        self.tree.heading("brand", text="Бренд")
        self.tree.heading("category", text="Категория")
        self.tree.heading("material", text="Материал")
        self.tree.heading("price", text="Цена")
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("brand", width=100, anchor="center")
        self.tree.column("category", width=120, anchor="center")
        self.tree.column("material", width=100, anchor="center")
        self.tree.column("price", width=100, anchor="e")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.refresh_table()

    # ================= ЛОГИКА SQL РАБОТЫ С ДАННЫМИ =================
    def refresh_table(self, event=None):
        """Обновление таблицы, загружая актуальные данные из SQLite с фильтрацией."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_query = self.entry_search.get().strip().lower() if hasattr(self, 'entry_search') else ""
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        if search_query:
            cursor.execute(
                "SELECT id, name, brand, category, material, price FROM products WHERE LOWER(name) LIKE ? OR LOWER(brand) LIKE ?",
                (f"%{search_query}%", f"%{search_query}%")
            )
        else:
            cursor.execute("SELECT id, name, brand, category, material, price FROM products")
            
        rows = cursor.fetchall()
        conn.close()
        
        for r in rows:
            # Исправлена распаковка кортежа r по индексам
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], f"{r[5]:.2f} руб."))

    def add_product(self):
        """Добавление нового товара в SQLite."""
        name = self.entry_name.get().strip()
        brand = self.entry_brand.get().strip()
        category = self.combo_category.get()
        material = self.entry_material.get().strip()
        price_raw = self.entry_price.get().strip()
        
        if not (name and brand and category and material and price_raw):
            messagebox.showwarning("Ошибка ввода", "Пожалуйста, заполните все поля формы!")
            return
            
        try:
            price = float(price_raw)
            if price <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка типа", "Цена должна быть положительным числом!")
            return
            
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, brand, category, price, material) VALUES (?, ?, ?, ?, ?)",
            (name, brand, category, price, material)
        )
        conn.commit()
        conn.close()
        
        self.entry_name.delete(0, tk.END)
        self.entry_brand.delete(0, tk.END)
        self.entry_material.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        
        self.refresh_table()
        messagebox.showinfo("Успех", f"Товар '{name}' успешно сохранен в базу данных.")

    def delete_product(self):
        """Удаление выбранного товара из SQLite."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Выбор отсутвует", "Выберите строку с товаром для удаления!")
            return
            
        item_values = self.tree.item(selected_item, "values")
        prod_id = int(item_values[0])
        prod_name = item_values[1]
        
        if messagebox.askyesno("Подтверждение", f"Вы действительно хотите удалить '{prod_name}' из базы данных?"):
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (prod_id,))
            conn.commit()
            conn.close()
            self.refresh_table()

    def change_theme(self, event):
        self.current_theme = self.theme_combo.get()
        self.show_main_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    init_db()  # Сначала проверяем и подготавливаем базу данных
    app = ShoeStoreApp()
    app.mainloop()