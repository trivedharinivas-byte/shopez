import os
import shutil
import database
import auth

def run_tests():
    print("==================================================")
    print("            shopEz Test Suite Startup            ")
    print("==================================================")
    
    # 1. Database Init Test
    print("[TEST 1] Initializing SQLite database...")
    try:
        # If database exists from previous run, remove it to start clean
        if os.path.exists('shopez.db'):
            os.remove('shopez.db')
        database.init_db()
        print(" -> Success: Database initialized and seeded.")
    except Exception as e:
        print(f" -> Fail: Database init error: {e}")
        return False

    # 2. Product Seeding Validation
    print("[TEST 2] Verifying seeded products...")
    products = database.get_all_products()
    print(f" -> Info: Found {len(products)} products in the database.")
    if len(products) == 10:
        print(" -> Success: Correct number of items seeded.")
    else:
        print(" -> Fail: Seeding count incorrect.")
        return False
        
    # Check category filter
    audio_prods = database.get_products_by_category('Audio')
    print(f" -> Info: Found {len(audio_prods)} products in 'Audio' category.")
    if len(audio_prods) == 2:
        print(" -> Success: Category filtering functional.")
    else:
        print(" -> Fail: Category filtering issues.")
        return False

    # 3. User Hashing and Registration Test
    print("[TEST 3] Testing user registration and password hashing...")
    # First user should automatically be admin
    reg_success_1, msg_1 = auth.register_user('alex', 'alex@shopez.com', 'securepass123')
    print(f" -> Info: Registering first user (admin): {msg_1}")
    
    # Second user should be customer
    reg_success_2, msg_2 = auth.register_user('emily', 'emily@shopez.com', 'mypassword')
    print(f" -> Info: Registering second user (customer): {msg_2}")
    
    # Attempting duplicate registration
    reg_success_3, msg_3 = auth.register_user('alex', 'alex2@shopez.com', 'otherpwd')
    print(f" -> Info: Registering duplicate user: {msg_3}")
    
    if reg_success_1 and reg_success_2 and not reg_success_3:
        print(" -> Success: User registration constraints and controls verified.")
    else:
        print(" -> Fail: User registration constraints failed.")
        return False
        
    # Verify Admin Role assignment
    admin_user = database.get_user_by_username('alex')
    customer_user = database.get_user_by_username('emily')
    if admin_user['is_admin'] == 1 and customer_user['is_admin'] == 0:
        print(" -> Success: Automated Admin assignment verified.")
    else:
        print(" -> Fail: Role assignment incorrect.")
        return False

    # 4. Authentication / Verification Test
    print("[TEST 4] Testing credential verification...")
    pwd_verified = auth.verify_password('securepass123', admin_user['password_hash'])
    pwd_failed = auth.verify_password('wrongpass', admin_user['password_hash'])
    
    if pwd_verified and not pwd_failed:
        print(" -> Success: PBKDF2 Password verification matching verified.")
    else:
        print(" -> Fail: Hashing mismatch detected.")
        return False

    # 5. Cart Operations Test
    print("[TEST 5] Testing shopping cart logic...")
    user_id = customer_user['id']
    prod_id = products[0]['id'] # shopEz Pad Pro
    initial_stock = products[0]['stock']
    
    # Add to cart
    add_success, add_msg = database.add_to_cart(user_id, prod_id, 2)
    print(f" -> Info: Add to cart details: {add_msg}")
    
    # Check items
    cart_items = database.get_cart_items(user_id)
    if len(cart_items) == 1 and cart_items[0]['quantity'] == 2:
        print(" -> Success: Item added to cart database correctly.")
    else:
        print(" -> Fail: Add to cart verification failed.")
        return False
        
    # Update quantity
    database.update_cart_quantity(user_id, prod_id, 3)
    cart_items = database.get_cart_items(user_id)
    if cart_items[0]['quantity'] == 3:
        print(" -> Success: Quantity updated.")
    else:
        print(" -> Fail: Quantity update failed.")
        return False

    # 6. Order Placement Test
    print("[TEST 6] Testing checkout and stock updates...")
    shipping_addr = "123 Python Way, Code City, 90210, USA"
    order_id, order_msg = database.create_order(user_id, shipping_addr)
    print(f" -> Info: Create order details: {order_msg}")
    
    if order_id:
        print(f" -> Success: Order #{order_id} created.")
    else:
        print(" -> Fail: Order placement failed.")
        return False
        
    # Verify cart cleared
    cart_items = database.get_cart_items(user_id)
    if len(cart_items) == 0:
        print(" -> Success: Cart cleared upon successful order.")
    else:
        print(" -> Fail: Cart not cleared.")
        return False
        
    # Verify stock reduction
    updated_prod = database.get_product_by_id(prod_id)
    if updated_prod['stock'] == initial_stock - 3:
        print(f" -> Success: Product inventory updated. Was {initial_stock}, now {updated_prod['stock']}.")
    else:
        print(" -> Fail: Product inventory failed to update correctly.")
        return False
        
    # Verify order logged in registries
    orders = database.get_orders_by_user(user_id)
    if len(orders) == 1 and len(orders[0]['items']) == 1:
        print(" -> Success: Order details logged correctly.")
    else:
        print(" -> Fail: Order logging verification failed.")
        return False

    print("\n==================================================")
    print("         All shopEz Core Tests Passed!           ")
    print("==================================================")
    return True

if __name__ == '__main__':
    run_tests()
