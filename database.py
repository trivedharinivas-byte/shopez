import sqlite3
import os
from config import DATABASE_PATH, CATEGORIES

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    
    # Create Products Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT NOT NULL,
            category TEXT NOT NULL,
            stock INTEGER DEFAULT 0
        )
    ''''')
    
    # Create Cart Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE(user_id, product_id)
        )
    ''')
    
    # Create Orders Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            shipping_address TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Create Order Items Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    
    # Seed products if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        seed_products(conn)
        
    conn.close()

def seed_products(conn):
    cursor = conn.cursor()
    sample_products = [
        # Electronics
        (
            'shopEz Pad Pro',
            'Next-generation 11-inch liquid retina display tablet. Powered by an advanced octa-core processor with 128GB storage, perfect for creators, students, and professionals alike.',
            799.99,
            '/static/images/pad_pro.jpg',
            'Electronics',
            25
        ),
        (
            'ZenBook Lite Ultrabook',
            'Sleek, lightweight 14-inch laptop. Featues 16GB RAM, 512GB NVMe SSD, and a breathtaking 2K OLED screen. Designed for high efficiency and productivity on the go.',
            999.99,
            '/static/images/ultrabook.jpg',
            'Electronics',
            15
        ),
        # Wearables
        (
            'AeroFit Watch v4',
            'A premium smartwatch with heart rate monitor, sleep tracking, GPS navigation, and 7-day battery life. Stay connected, active, and monitor your health variables seamlessly.',
            199.99,
            '/static/images/watch.jpg',
            'Wearables',
            50
        ),
        (
            'AeroFit Band Active',
            'Lightweight fitness tracker containing step counters, workout detection, sleep analyzer, and smart notification alerts. Water-resistant up to 50 meters.',
            79.99,
            '/static/images/band.jpg',
            'Wearables',
            100
        ),
        # Audio
        (
            'SonicEcho H9 Headphones',
            'Ultimate noise-cancelling wireless headphones. 40 hours of playtime, crisp high-definition sound, and plush memory foam earcups for unmatched long-session comfort.',
            299.99,
            '/static/images/headphones.jpg',
            'Audio',
            30
        ),
        (
            'SonicBuds Air Wireless',
            'True wireless earbuds with active noise cancellation, customizable touch controls, smart ambient pass-through, and up to 30 hours of case-backed playback.',
            129.99,
            '/static/images/earbuds.jpg',
            'Audio',
            75
        ),
        # Smart Home
        (
            'Orbita Smart Speaker Gen 2',
            'Voice-controlled intelligent speaker. Featuring premium acoustic sound tuning, smart hub integration, and an ambient glowing display for timers and weather updates.',
            89.99,
            '/static/images/speaker.svg',
            'Smart Home',
            40
        ),
        (
            'Aura Smart Glow Lamp',
            'Intelligent bedside lamp. Supports 16 million colors, automated sleep/wake schedules, app control, and syncs seamlessly with music rhythms for ambient moods.',
            59.99,
            '/static/images/lamp.svg',
            'Smart Home',
            60
        ),
        # Accessories
        (
            'VoltGrid Mechanical Keyboard',
            'Ultra-responsive mechanical keyboard with clicky blue switches, customizable dynamic RGB lighting modes, and an ergonomic aluminum frame designed for typing and gaming.',
            109.99,
            '/static/images/keyboard.svg',
            'Accessories',
            35
        ),
        (
            'GlideFlow Wireless Mouse',
            'Ergonomically sculpted precision mouse. 16,000 DPI adjustable optical sensor, silent-click switches, and dual connectivity (Bluetooth + 2.4GHz USB wireless dongle).',
            49.99,
            '/static/images/mouse.svg',
            'Accessories',
            80
        )
    ]
    cursor.executemany('''
        INSERT INTO products (name, description, price, image_url, category, stock)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_products)
    conn.commit()

# Product Operations
def get_all_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    return product

def get_products_by_category(category):
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products WHERE category = ?", (category,)).fetchall()
    conn.close()
    return products

def search_products(query, category=None):
    conn = get_db_connection()
    sql = "SELECT * FROM products WHERE (name LIKE ? OR description LIKE ?)"
    params = [f"%{query}%", f"%{query}%"]
    if category and category != 'All':
        sql += " AND category = ?"
        params.append(category)
    products = conn.execute(sql, params).fetchall()
    conn.close()
    return products

def add_product(name, description, price, image_url, category, stock):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, description, price, image_url, category, stock)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, description, price, image_url, category, stock))
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return product_id

def update_product(product_id, name, description, price, image_url, category, stock):
    conn = get_db_connection()
    conn.execute('''
        UPDATE products 
        SET name = ?, description = ?, price = ?, image_url = ?, category = ?, stock = ?
        WHERE id = ?
    ''', (name, description, price, image_url, category, stock, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# User Operations
def create_user(username, email, password_hash, is_admin=0):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, is_admin)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, is_admin))
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        user_id = None
    finally:
        conn.close()
    return user_id

def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user

# Cart Operations
def get_cart_items(user_id):
    conn = get_db_connection()
    items = conn.execute('''
        SELECT c.id as cart_item_id, c.quantity, p.* 
        FROM cart_items c 
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    ''', (user_id,)).fetchall()
    conn.close()
    return items

def add_to_cart(user_id, product_id, quantity=1):
    conn = get_db_connection()
    # Check current stock
    product = conn.execute("SELECT stock FROM products WHERE id = ?", (product_id,)).fetchone()
    if not product or product['stock'] < quantity:
        conn.close()
        return False, "Not enough stock"
        
    try:
        conn.execute('''
            INSERT INTO cart_items (user_id, product_id, quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = quantity + excluded.quantity
        ''', (user_id, product_id, quantity))
        conn.commit()
        success = True
        msg = "Added to cart"
    except Exception as e:
        success = False
        msg = str(e)
    finally:
        conn.close()
    return success, msg

def update_cart_quantity(user_id, product_id, quantity):
    if quantity <= 0:
        return remove_from_cart(user_id, product_id)
        
    conn = get_db_connection()
    product = conn.execute("SELECT stock FROM products WHERE id = ?", (product_id,)).fetchone()
    if not product or product['stock'] < quantity:
        conn.close()
        return False, "Not enough stock"
        
    conn.execute('''
        UPDATE cart_items 
        SET quantity = ? 
        WHERE user_id = ? AND product_id = ?
    ''', (quantity, user_id, product_id))
    conn.commit()
    conn.close()
    return True, "Quantity updated"

def remove_from_cart(user_id, product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cart_items WHERE user_id = ? AND product_id = ?', (user_id, product_id))
    conn.commit()
    conn.close()
    return True, "Removed from cart"

def clear_cart(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

# Order Operations
def create_order(user_id, shipping_address):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Get cart items
        cart_items = cursor.execute('''
            SELECT c.quantity, p.id as product_id, p.price, p.stock, p.name
            FROM cart_items c 
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
        ''', (user_id,)).fetchall()
        
        if not cart_items:
            return None, "Cart is empty"
            
        # Check stock for all items
        total_amount = 0.0
        for item in cart_items:
            if item['stock'] < item['quantity']:
                return None, f"Insufficient stock for {item['name']}"
            total_amount += item['price'] * item['quantity']
            
        # Create order
        cursor.execute('''
            INSERT INTO orders (user_id, total_amount, status, shipping_address)
            VALUES (?, ?, 'Paid', ?)
        ''', (user_id, total_amount, shipping_address))
        order_id = cursor.lastrowid
        
        # Move items to order_items and update product stock
        for item in cart_items:
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item['product_id'], item['quantity'], item['price']))
            
            cursor.execute('''
                UPDATE products 
                SET stock = stock - ? 
                WHERE id = ?
            ''', (item['quantity'], item['product_id']))
            
        # Clear cart
        cursor.execute('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
        
        conn.commit()
        return order_id, "Order created successfully"
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        conn.close()

def get_orders_by_user(user_id):
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC
    ''', (user_id,)).fetchall()
    
    orders_list = []
    for order in orders:
        order_dict = dict(order)
        # Fetch items
        items = conn.execute('''
            SELECT oi.quantity, oi.price, p.name, p.image_url 
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order['id'],)).fetchall()
        order_dict['items'] = [dict(item) for item in items]
        orders_list.append(order_dict)
        
    conn.close()
    return orders_list

def get_all_orders():
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT o.*, u.username 
        FROM orders o 
        JOIN users u ON o.user_id = u.id 
        ORDER BY o.created_at DESC
    ''').fetchall()
    
    orders_list = []
    for order in orders:
        order_dict = dict(order)
        # Fetch items
        items = conn.execute('''
            SELECT oi.quantity, oi.price, p.name, p.image_url 
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order['id'],)).fetchall()
        order_dict['items'] = [dict(item) for item in items]
        orders_list.append(order_dict)
        
    conn.close()
    return orders_list
