from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from database import init_db, get_db_connection

app = Flask(__name__)
app.secret_key = "super_secret_key_for_shoe_store"

THEMES = {
    "classic": {
        "name": "Темная классика",
        "bg": "#2A2F35", "fg": "#FFFFFF", "accent": "#1ABC9C", "card": "#34495E", "entry_bg": "#1F2326"
    },
    "light": {
        "name": "Светлая корпоративная",
        "bg": "#F5F7FA", "fg": "#2C3E50", "accent": "#2980B9", "card": "#FFFFFF", "entry_bg": "#EAECEE"
    },
    "blueberry": {
        "name": "Яркая черничная",
        "bg": "#1F1A3A", "fg": "#FFFFFF", "accent": "#E91E63", "card": "#2D264D", "entry_bg": "#151126"
    },
    "emerald": {
        "name": "Изумрудный город",
        "bg": "#162B24", "fg": "#EAF2F0", "accent": "#2ECC71", "card": "#1F3D33", "entry_bg": "#0E1C17"
    },
    "cyberpunk": {
        "name": "Неоновый киберпанк",
        "bg": "#0D0D0D", "fg": "#00FF66", "accent": "#FF007F", "card": "#1A1A1A", "entry_bg": "#111111"
    }
}

@app.context_processor
def inject_theme():
    theme_key = session.get("theme", "classic")
    if theme_key not in THEMES:
        theme_key = "classic"
    return dict(theme=THEMES[theme_key], themes_list=THEMES, current_theme_key=theme_key)

@app.route("/change_theme", methods=["POST"])
def change_theme():
    session["theme"] = request.form.get("theme", "classic")
    return redirect(request.referrer or url_for("main_screen"))

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        conn = get_db_connection()
        user = conn.execute("SELECT id, role FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()
        
        if user:
            session["user"] = username
            session["user_id"] = user["id"]  # Сохраняем ID пользователя для корзины
            session["role"] = user["role"]
            flash(f"Добро пожаловать, {username} ({user['role']})!", "success")
            return redirect(url_for("main_screen"))
        else:
            flash("Неверный логин или пароль!", "error")
            
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "Менеджер")
        
        if not username or not password:
            flash("Все поля должны быть заполнены!", "error")
            return redirect(url_for("register"))
            
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            flash(f"Пользователь {username} успешно зарегистрирован!", "success")
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            conn.close()
            flash(f"Логин '{username}' уже занят! Выберите другой.", "error")
            
    return render_template("register.html")

@app.route("/main")
def main_screen():
    if "user" not in session:
        return redirect(url_for("login"))
        
    search_query = request.args.get("search", "").strip().lower()
    conn = get_db_connection()
    
    if search_query:
        products = conn.execute(
            "SELECT id, name, brand, category, material, price FROM products WHERE LOWER(name) LIKE ? OR LOWER(brand) LIKE ?",
            (f"%{search_query}%", f"%{search_query}%")
        ).fetchall()
    else:
        products = conn.execute("SELECT id, name, brand, category, material, price FROM products").fetchall()
        
    conn.close()
    return render_template("main.html", products=products, search_query=search_query)

@app.route("/add_product", methods=["POST"])
def add_product():
    if session.get("role") != "Администратор":
        flash("Изменения доступны только Администратору!", "error")
        return redirect(url_for("main_screen"))
        
    name = request.form.get("name", "").strip()
    brand = request.form.get("brand", "").strip()
    category = request.form.get("category", "")
    material = request.form.get("material", "").strip()
    price_raw = request.form.get("price", "").strip()
    
    if not (name and brand and category and material and price_raw):
        flash("Пожалуйста, заполните все поля формы!", "error")
        return redirect(url_for("main_screen"))
        
    try:
        price = float(price_raw)
        if price <= 0: raise ValueError
    except ValueError:
        flash("Цена должна быть положительным числом!", "error")
        return redirect(url_for("main_screen"))
        
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO products (name, brand, category, price, material) VALUES (?, ?, ?, ?, ?)",
        (name, brand, category, price, material)
    )
    conn.commit()
    conn.close()
    
    flash(f"Товар '{name}' успешно сохранен в базу данных.", "success")
    return redirect(url_for("main_screen"))

@app.route("/delete_product/<int:prod_id>", methods=["POST"])
def delete_product(prod_id):
    if session.get("role") != "Администратор":
        flash("Изменения доступны только Администратору!", "error")
        return redirect(url_for("main_screen"))
        
    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (prod_id,))
    conn.commit()
    conn.close()
    
    flash("Товар успешно удален из базы данных.", "success")
    return redirect(url_for("main_screen"))

# --- НАШИ НОВЫЕ МАРШРУТЫ ДЛЯ КОРЗИНЫ ---

@app.route("/add_to_cart/<int:prod_id>", methods=["POST"])
def add_to_cart(prod_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    conn = get_db_connection()
    
    # Проверяем, есть ли уже этот товар в корзине у текущего пользователя
    existing_item = conn.execute(
        "SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?", 
        (user_id, prod_id)
    ).fetchone()
    
    if existing_item:
        # Если есть, увеличиваем количество
        conn.execute(
            "UPDATE cart SET quantity = quantity + 1 WHERE id = ?", 
            (existing_item["id"],)
        )
    else:
        # Если нет, добавляем новую запись
        conn.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)", 
            (user_id, prod_id)
        )
        
    conn.commit()
    conn.close()
    flash("Товар добавлен в корзину!", "success")
    return redirect(url_for("main_screen"))

@app.route("/cart")
def view_cart():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    conn = get_db_connection()
    
    # Собираем данные товаров, находящихся в корзине, используя JOIN
    cart_items = conn.execute('''
        SELECT cart.id as cart_id, products.name, products.brand, products.price, cart.quantity 
        FROM cart 
        JOIN products ON cart.product_id = products.id 
        WHERE cart.user_id = ?
    ''', (user_id,)).fetchall()
    
    # Считаем общую стоимость корзины
    total_price = sum(item["price"] * item["quantity"] for item in cart_items)
    conn.close()
    
    return render_template("cart.html", cart_items=cart_items, total_price=total_price)

@app.route("/delete_from_cart/<int:item_id>", methods=["POST"])
def delete_from_cart(item_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    conn = get_db_connection()
    conn.execute("DELETE FROM cart WHERE id = ? AND user_id = ?", (item_id, session["user_id"]))
    conn.commit()
    conn.close()
    
    flash("Товар удален из корзины.", "success")
    # БЫЛО: return redirect(url_for("cart"))
    # СТАЛО:
    return redirect(url_for("view_cart"))  # Перенаправляем на функцию просмотра корзины


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
