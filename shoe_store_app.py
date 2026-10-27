import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "shoe_store.db"

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


class Database:
    """Класс для управления базой данных SQLite."""
    def __init__(self, db_name):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Создает базу данных и таблицы, если они еще не существуют."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')
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
            
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                cursor.executemany(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    [("admin", "123", "Администратор"), ("manager", "123", "Менеджер")]
                )
                
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

    def authenticate_user(self, username, password):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
            res = cursor.fetchone()
            return res[0] if res else None

    def register_user(self, username, password, role):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))

    def fetch_products(self, search_query=""):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if search_query:
                cursor.execute(
                    "SELECT id, name, brand, category, material, price FROM products WHERE LOWER(name) LIKE ? OR LOWER(brand) LIKE ?",
                    (f"%{search_query}%", f"%{search_query}%")
                )
            else:
                cursor.execute("SELECT id, name, brand, category, material, price FROM products")
            return cursor.fetchall()

    def add_product(self, name, brand, category, price, material):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, brand, category, price, material) VALUES (?, ?, ?, ?, ?)",
                (name, brand, category, price, material)
            )

    def delete_product(self, prod_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (prod_id,))


class LoginScreen(ttk.Frame):
    """Экран авторизации."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        colors = THEMES[self.controller.current_theme]
        
        login_frame = ttk.LabelFrame(self, text=" Авторизация пользователя ", padding=20)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=300)
        
        ttk.Label(login_frame, text="Логин:").pack(anchor="w", pady=2)
        self.login_entry = tk.Entry(login_frame, font=("Arial", 11), bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.login_entry.pack(fill="x", pady=5)
        
        ttk.Label(login_frame, text="Пароль:").pack(anchor="w", pady=2)
        self.password_entry = tk.Entry(login_frame, font=("Arial", 11), show="*", bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["accent"], highlightthickness=1, highlightbackground=colors["card"], highlightcolor=colors["accent"], bd=0)
        self.password_entry.pack(fill="x", pady=5)
        
        btn_login = ttk.Button(login_frame, text="Войти в систему", command=self.handle_login)
        btn_login.pack(fill="x", pady=(15, 5))
        
        btn_reg_screen = ttk.Button(login_frame, text="Зарегистрироваться", command=lambda: controller.show_frame(RegisterScreen))
        btn_reg_screen.pack(fill="x", pady=5)

    def handle_login(self):
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        result = self.controller.db.authenticate_user(username, password)
        if result:
            self.controller.current_user = username
            self.controller.current_role = result
            messagebox.showinfo("Успех", f"Добро пожаловать, {username} ({self.controller.current_role})!")
            self.controller.show_frame(MainScreen)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")


class RegisterScreen(ttk.Frame):
    """Экран регистрации."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        colors = THEMES[self.controller.current_theme]
        
        reg_frame = ttk.LabelFrame(self, text=" Регистрация нового аккаунта ", padding=20)
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
        
        btn_back = ttk.Button(reg_frame, text="Назад к авторизации", command=lambda: controller.show_frame(LoginScreen))
        btn_back.pack(fill="x", pady=5)

    def handle_registration(self):
        username = self.reg_login_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        role = self.reg_role_combo.get()
        
        if not username or not password:
            messagebox.showwarning("Ошибка ввода", "Все поля должны быть заполнены!")
            return
            
        try:
            self.controller.db.register_user(username, password, role)
            messagebox.showinfo("Успех", f"Пользователь {username} успешно зарегистрирован!")
            self.controller.show_frame(LoginScreen)
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", f"Логин '{username}' уже занят! Выберите другой.")


class MainScreen(ttk.Frame):
    """Главный экран информационной системы."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        colors = THEMES[self.controller.current_theme]
        
        # --- ТОР БАР ---
        top_bar = ttk.Frame(self, style="Top.TFrame", height=50)
        top_bar.pack(fill="x", side="top", ipady=5, ipadx=10)
        
        self.lbl_user = ttk.Label(top_bar, text="", style="Top.TLabel")
        self.lbl_user.pack(side="left", padx=10, pady=10)
        
        btn_logout = ttk.Button(top_bar, text="Выйти", command=self.logout, style="TButton")
        btn_logout.pack(side="left", padx=15, pady=5)
        
        self.theme_combo = ttk.Combobox(top_bar, values=list(THEMES.keys()), state="readonly", width=22)
        self.theme_combo.set(self.controller.current_theme)
        self.theme_combo.pack(side="right", padx=10, pady=5)
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)
        
        ttk.Label(top_bar, text="Тема оформления:", style="Top.TLabel").pack(side="right", padx=5, pady=5)
        
        # --- ОСНОВНОЙ КОНТЕЙНЕР ---
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Левая панель формы
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
        
        self.btn_add = ttk.Button(form_frame, text="➕ Добавить товар", style="Add.TButton", command=self.add_product)
        self.btn_add.pack(fill="x", pady=2)
        
        self.btn_del = ttk.Button(form_frame, text="❌ Удалить выбранный", style="Del.TButton", command=self.delete_product)
        self.btn_del.pack(fill="x", pady=5)
        
        self.lbl_restricted = ttk.Label(form_frame, text="*Изменения доступны\nтолько Администратору", foreground="orange", font=("Arial", 9, "italic"))
        
        # Правая панель таблицы
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

    def update_user_info(self):
        """Конфигурация прав доступа при открытии экрана."""
        self.lbl_user.configure(text=f"👤 Пользователь: {self.controller.current_user} ({self.controller.current_role})")
        if self.controller.current_role != "Администратор":
            self.btn_add.configure(state="disabled")
            self.btn_del.configure(state="disabled")
            self.lbl_restricted.pack(pady=5)
        else:
            self.btn_add.configure(state="normal")
            self.btn_del.configure(state="normal")
            self.lbl_restricted.pack_forget()
        self.refresh_table()

    def refresh_table(self, event=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_query = self.entry_search.get().strip().lower() if hasattr(self, 'entry_search') else ""
        rows = self.controller.db.fetch_products(search_query)
        
        for r in rows:
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], f"{r[5]:.2f} руб."))

    def add_product(self):
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
            
        self.controller.db.add_product(name, brand, category, price, material)
        
        for entry in (self.entry_name, self.entry_brand, self.entry_material, self.entry_price):
            entry.delete(0, tk.END)
            
        self.refresh_table()
        messagebox.showinfo("Уsuccess", f"Товар '{name}' успешно сохранен в базу данных.")

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Выбор отсутвует", "Выберите строку с товаром для удаления!")
            return
            
        item_values = self.tree.item(selected_item, "values")
        prod_id = int(item_values[0])
        prod_name = item_values[1]
        
        if messagebox.askyesno("Подтверждение", f"Вы действительно хотите удалить '{prod_name}' из базы данных?"):
            self.controller.db.delete_product(prod_id)
            self.refresh_table()

    def change_theme(self, event):
        self.controller.current_theme = self.theme_combo.get()
        self.controller.refresh_app_ui()

    def logout(self):
        self.controller.current_user = None
        self.controller.current_role = None
        self.controller.show_frame(LoginScreen)


class ShoeStoreApp(tk.Tk):
    """Основной класс контейнера, управляющий состоянием и экранами."""
    def __init__(self):
        super().__init__()
        self.title("Информационная система: Магазин обуви")
        self.geometry("1000x650")
        
        self.db = Database(DB_NAME)
        self.current_theme = "Темная классика"
        self.current_user = None
        self.current_role = None
        self.style = ttk.Style()
        
        # Контейнер для всех фреймов (экранов)
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.active_frame = None
        self.current_frame_class = LoginScreen
        self.show_frame(LoginScreen)

    def show_frame(self, frame_class):
        """Уничтожает старый фрейм и создает новый для обновления стилей."""
        self.current_frame_class = frame_class
        if self.active_frame is not None:
            self.active_frame.destroy()
            
        self.update_theme_engine()
        
        self.active_frame = frame_class(parent=self.container, controller=self)
        self.active_frame.pack(fill="both", expand=True)
        
        # Если открывается главный экран, настраиваем права
        if frame_class == MainScreen:
            self.active_frame.update_user_info()

    def refresh_app_ui(self):
        """Перезапускает текущий кадр с новой темой оформления."""
        self.show_frame(self.current_frame_class)

    def update_theme_engine(self):
        """Обновление стилей ttk."""
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


if __name__ == "__main__":
    app = ShoeStoreApp()
    app.mainloop()
