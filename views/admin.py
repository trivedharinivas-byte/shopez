from nicegui import ui, app
import auth
import database
from config import CATEGORIES
from views import common

@ui.page('/admin')
def admin_page():
    # Authorization check
    if not auth.is_logged_in() or not auth.is_admin():
        ui.navigate.to('/')
        ui.notify('Access Denied: Admin authorization required.', type='negative')
        return
        
    common.setup_page('shopEz - Admin Control Panel')
    common.header_navigation()
    
    # Dashboard metrics calculations
    orders = database.get_all_orders()
    products = database.get_all_products()
    
    conn = database.get_db_connection()
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    
    total_sales = sum(order['total_amount'] for order in orders)
    
    with ui.column().classes('w-full max-w-7xl mx-auto px-4 md:px-8 py-8 gap-8'):
        ui.label('Admin Control Panel').classes('text-3xl font-extrabold text-white border-b-2 border-purple-500 pb-1 align-self-start')
        
        # Metric Cards Row
        with ui.row().classes('w-full gap-4 grid grid-cols-2 md:grid-cols-4'):
            # Sales Metric
            with ui.card().classes('shopez-card admin-card-metric flex-grow'):
                ui.label(f"${total_sales:.2f}").classes('metric-val')
                ui.label('Total Revenue').classes('metric-lbl')
                
            # Orders Metric
            with ui.card().classes('shopez-card admin-card-metric flex-grow'):
                ui.label(str(len(orders))).classes('metric-val')
                ui.label('Orders Processed').classes('metric-lbl')
                
            # Products Metric
            with ui.card().classes('shopez-card admin-card-metric flex-grow'):
                ui.label(str(len(products))).classes('metric-val')
                ui.label('Active Inventory').classes('metric-lbl')
                
            # Users Metric
            with ui.card().classes('shopez-card admin-card-metric flex-grow'):
                ui.label(str(user_count)).classes('metric-val')
                ui.label('Registered Customers').classes('metric-lbl')
                
        # Tabbed panel: Products vs Orders
        with ui.tabs().classes('w-full text-white border-b border-gray-800') as tabs:
            prod_tab = ui.tab('Manage Products').classes('capitalize text-sm font-semibold')
            order_tab = ui.tab('Order Registry').classes('capitalize text-sm font-semibold')
            
        with ui.tab_panels(tabs, value=prod_tab).classes('w-full bg-transparent p-0 mt-4'):
            # Products Panel
            with ui.tab_panel(prod_tab).classes('w-full gap-4 p-0'):
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.label('Products Directory').classes('text-xl font-bold text-gray-200')
                    ui.button('Add Product', on_click=lambda: open_add_product_dialog()).classes('btn-gradient-glow px-4 py-2').props('icon=add')
                    
                products_container = ui.element('div').classes('w-full')
                with products_container:
                    render_products_table(products_container)
                    
            # Orders Panel
            with ui.tab_panel(order_tab).classes('w-full gap-4 p-0'):
                ui.label('Orders Placed').classes('text-xl font-bold text-gray-200 mb-2')
                render_orders_table(orders)
                
    common.footer()

# Refreshable Products Table
@ui.refreshable
def render_products_table(container):
    products = database.get_all_products()
    
    if not products:
        with ui.column().classes('w-full items-center justify-center py-12'):
            ui.label('No products in catalog. Add some to get started!').classes('text-gray-400 font-semibold')
        return
        
    with ui.card().classes('shopez-card p-0 w-full overflow-x-auto bg-black/20 border border-gray-800/80'):
        # Table UI
        ui.html('''
            <table class="glass-table">
                <thead>
                    <tr>
                        <th>Product ID</th>
                        <th>Name</th>
                        <th>Category</th>
                        <th>Price</th>
                        <th>Stock</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="products-table-body">
                </tbody>
            </table>
        ''').classes('w-full')
        
        # We populate the table rows dynamically
        # Since we want to attach event handlers to buttons, we can construct them in NiceGUI:
        table_body = ui.element('div').classes('hidden') # hidden element to reference rows
        
        # Alternatively, we can use NiceGUI's standard list view or a clean layout with grids
        # NiceGUI has a grid layout that works nicely for tables:
        with ui.column().classes('w-full p-4 gap-2'):
            # Header Row
            with ui.row().classes('w-full text-xs font-bold text-gray-400 border-b border-gray-800 pb-2 px-2'):
                ui.label('ID').classes('w-12')
                ui.label('Name').classes('flex-grow min-w-0')
                ui.label('Category').classes('w-32')
                ui.label('Price').classes('w-24 text-right')
                ui.label('Stock').classes('w-20 text-center')
                ui.label('Actions').classes('w-28 text-right')
                
            # Product Rows
            for prod in products:
                p_id = prod['id']
                with ui.row().classes('w-full items-center text-sm border-b border-gray-900/60 py-2 px-2 hover:bg-white/5 rounded-lg transition-colors'):
                    ui.label(str(p_id)).classes('w-12 text-gray-500 font-mono')
                    
                    with ui.row().classes('flex-grow min-w-0 items-center gap-2'):
                        ui.html(f'<img src="{prod["image_url"]}" class="w-8 h-8 object-cover rounded-md flex-shrink-0" />')
                        ui.label(prod['name']).classes('font-bold text-white line-clamp-1 cursor-pointer').on('click', lambda pid=p_id: ui.navigate.to(f'/product/{pid}'))
                        
                    ui.label(prod['category']).classes('w-32 text-gray-400')
                    ui.label(f"${prod['price']:.2f}").classes('w-24 text-right font-bold text-purple-400')
                    
                    stock_cls = 'text-success' if prod['stock'] >= 10 else ('text-warning' if prod['stock'] > 0 else 'text-error')
                    ui.label(str(prod['stock'])).classes(f"w-20 text-center font-bold {stock_cls}")
                    
                    with ui.row().classes('w-28 justify-end gap-1'):
                        ui.button(
                            icon='edit', 
                            on_click=lambda p=prod: open_edit_product_dialog(p, container)
                        ).props('flat round color=purple size=sm')
                        
                        ui.button(
                            icon='delete', 
                            on_click=lambda pid=p_id: delete_prod_confirm(pid, container)
                        ).props('flat round color=red size=sm')

# Dialog for Adding a Product
def open_add_product_dialog():
    with ui.dialog() as dialog, ui.card().classes('shopez-card p-6 w-full max-w-md gap-4'):
        ui.label('Add New Product').classes('text-lg font-bold text-white border-b border-gray-800 pb-2')
        
        # State values
        fields = {'name': '', 'desc': '', 'price': 0.0, 'img': '', 'cat': CATEGORIES[0], 'stock': 10}
        
        name_in = ui.input('Product Name', on_change=lambda e: fields.update({'name': e.value})).classes('w-full shopez-input')
        desc_in = ui.textarea('Description', on_change=lambda e: fields.update({'desc': e.value})).classes('w-full shopez-input')
        
        with ui.row().classes('w-full gap-4'):
            price_in = ui.number('Price ($)', format='%.2f', value=0.0, on_change=lambda e: fields.update({'price': float(e.value or 0)})).classes('flex-grow shopez-input')
            stock_in = ui.number('Stock Quantity', value=10, step=1, on_change=lambda e: fields.update({'stock': int(e.value or 0)})).classes('w-32 shopez-input')
            
        img_in = ui.input('Image URL', on_change=lambda e: fields.update({'img': e.value})).classes('w-full shopez-input')
        cat_in = ui.select(CATEGORIES, value=CATEGORIES[0], on_change=lambda e: fields.update({'cat': e.value})).classes('w-full shopez-input')
        
        def save():
            if not fields['name'] or not fields['desc'] or not fields['img']:
                ui.notify('Please fill out all required fields.', type='warning')
                return
            if fields['price'] <= 0:
                ui.notify('Price must be greater than zero.', type='warning')
                return
                
            database.add_product(fields['name'], fields['desc'], fields['price'], fields['img'], fields['cat'], fields['stock'])
            ui.notify('Product added successfully!', type='positive')
            dialog.close()
            ui.navigate.to('/admin') # Reload to sync state
            
        with ui.row().classes('w-full justify-end gap-2 mt-4'):
            ui.button('Cancel', on_click=dialog.close).classes('btn-secondary px-4')
            ui.button('Add Product', on_click=save).classes('btn-primary px-4')
            
    dialog.open()

# Dialog for Editing a Product
def open_edit_product_dialog(prod, container):
    with ui.dialog() as dialog, ui.card().classes('shopez-card p-6 w-full max-w-md gap-4'):
        ui.label('Edit Product Settings').classes('text-lg font-bold text-white border-b border-gray-800 pb-2')
        
        fields = {
            'name': prod['name'], 
            'desc': prod['description'], 
            'price': prod['price'], 
            'img': prod['image_url'], 
            'cat': prod['category'], 
            'stock': prod['stock']
        }
        
        name_in = ui.input('Product Name', value=fields['name'], on_change=lambda e: fields.update({'name': e.value})).classes('w-full shopez-input')
        desc_in = ui.textarea('Description', value=fields['desc'], on_change=lambda e: fields.update({'desc': e.value})).classes('w-full shopez-input')
        
        with ui.row().classes('w-full gap-4'):
            price_in = ui.number('Price ($)', format='%.2f', value=fields['price'], on_change=lambda e: fields.update({'price': float(e.value or 0)})).classes('flex-grow shopez-input')
            stock_in = ui.number('Stock Quantity', value=fields['stock'], step=1, on_change=lambda e: fields.update({'stock': int(e.value or 0)})).classes('w-32 shopez-input')
            
        img_in = ui.input('Image URL', value=fields['img'], on_change=lambda e: fields.update({'img': e.value})).classes('w-full shopez-input')
        cat_in = ui.select(CATEGORIES, value=fields['cat'], on_change=lambda e: fields.update({'cat': e.value})).classes('w-full shopez-input')
        
        def save():
            if not fields['name'] or not fields['desc'] or not fields['img']:
                ui.notify('Please fill out all fields.', type='warning')
                return
            if fields['price'] <= 0:
                ui.notify('Price must be greater than zero.', type='warning')
                return
                
            database.update_product(prod['id'], fields['name'], fields['desc'], fields['price'], fields['img'], fields['cat'], fields['stock'])
            ui.notify('Product updated successfully!', type='positive')
            dialog.close()
            render_products_table.refresh(container)
            
        with ui.row().classes('w-full justify-end gap-2 mt-4'):
            ui.button('Cancel', on_click=dialog.close).classes('btn-secondary px-4')
            ui.button('Save Changes', on_click=save).classes('btn-primary px-4')
            
    dialog.open()

# Delete product check
def delete_prod_confirm(product_id, container):
    with ui.dialog() as dialog, ui.card().classes('shopez-card p-6 w-full max-w-sm gap-4'):
        ui.label('Delete Product?').classes('text-lg font-bold text-white')
        ui.label('Are you sure you want to permanently delete this product? This action is irreversible.').classes('text-sm text-gray-400')
        
        def delete():
            database.delete_product(product_id)
            ui.notify('Product deleted successfully', type='info')
            dialog.close()
            render_products_table.refresh(container)
            
        with ui.row().classes('w-full justify-end gap-2 mt-2'):
            ui.button('Cancel', on_click=dialog.close).classes('btn-secondary px-4')
            ui.button('Delete', on_click=delete).classes('btn-primary bg-red-600 hover:bg-red-700 px-4')
            
    dialog.open()

# Orders table layout
def render_orders_table(orders):
    if not orders:
        with ui.column().classes('w-full items-center justify-center py-12'):
            ui.label('No orders placed yet.').classes('text-gray-400 font-semibold')
        return
        
    with ui.column().classes('w-full gap-4'):
        for order in orders:
            with ui.card().classes('shopez-card p-5 w-full bg-white/5 border border-white/10 rounded-2xl gap-3'):
                # Order summary header
                with ui.row().classes('w-full justify-between items-center flex-wrap gap-2 border-b border-gray-800/60 pb-2'):
                    with ui.row().classes('items-center gap-3'):
                        ui.label(f"Order #{order['id']}").classes('font-mono font-bold text-white text-base')
                        ui.label(f"by {order['username']}").classes('text-xs text-purple-400 font-semibold')
                        
                    with ui.row().classes('items-center gap-2'):
                        ui.label(order['created_at']).classes('text-xs text-gray-500')
                        ui.label(order['status']).classes('text-xs font-bold px-2 py-0.5 rounded-full bg-success/20 text-success border border-success/30')
                
                # Order shipping address
                with ui.row().classes('items-start gap-1 text-xs text-gray-400'):
                    ui.icon('place', size='xs').classes('mt-0.5')
                    ui.label(f"Deliver to: {order['shipping_address']}")
                    
                # Items ordered dropdown / details
                with ui.column().classes('w-full pl-4 border-l-2 border-gray-800 gap-2 mt-1'):
                    for item in order['items']:
                        with ui.row().classes('w-full items-center justify-between gap-4 text-xs'):
                            with ui.row().classes('items-center gap-2'):
                                ui.html(f'<img src="{item["image_url"]}" class="w-8 h-8 object-cover rounded-md" />')
                                ui.label(item['name']).classes('text-gray-200 font-medium')
                                ui.label(f"x{item['quantity']}").classes('text-gray-500 font-bold')
                            ui.label(f"${(item['price'] * item['quantity']):.2f}").classes('text-gray-300 font-bold')
                            
                # Bottom total row
                with ui.row().classes('w-full justify-end items-center mt-2 border-t border-gray-800/40 pt-2'):
                    ui.label('Order Total:').classes('text-xs text-gray-400 mr-2')
                    ui.label(f"${order['total_amount']:.2f}").classes('text-base font-extrabold text-purple-400')
