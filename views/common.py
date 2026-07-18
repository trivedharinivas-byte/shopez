from nicegui import ui, app
import auth
import database

def setup_page(title="shopEz"):
    ui.page_title(title)
    # Inject stylesheets and custom google fonts
    ui.add_head_html('<link rel="stylesheet" href="/static/styles.css">')
    ui.add_head_html('<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">')

def header_navigation():
    # Make sure database is loaded to compute cart count
    cart_count = 0
    if auth.is_logged_in():
        user_id = auth.get_current_user_id()
        items = database.get_cart_items(user_id)
        cart_count = sum(item['quantity'] for item in items)
        
    with ui.header().classes('shopez-header items-center justify-between'):
        # Logo
        with ui.row().classes('items-center cursor-pointer').on('click', lambda: ui.navigate.to('/')):
            ui.label('shopEz').classes('shopez-logo')
            
        # Navigation Actions
        with ui.row().classes('items-center gap-6'):
            ui.button('Home', on_click=lambda: ui.navigate.to('/')).props('flat color=white').classes('text-sm text-gray-300 hover:text-white capitalize')
            
            if auth.is_admin():
                ui.button('Admin', on_click=lambda: ui.navigate.to('/admin')).props('flat color=secondary').classes('text-sm text-purple-400 hover:text-purple-300 capitalize')
                
            # Shopping Cart icon + badge
            with ui.row().classes('relative items-center cursor-pointer p-2').on('click', lambda: ui.navigate.to('/cart')):
                ui.icon('shopping_cart').classes('text-white text-2xl')
                if cart_count > 0:
                    ui.label(str(cart_count)).classes('badge-count')
            
            # Auth options
            if auth.is_logged_in():
                with ui.row().classes('items-center gap-2 border-l border-gray-700 pl-4'):
                    ui.icon('account_circle').classes('text-white text-xl')
                    ui.label(auth.get_current_username()).classes('text-white text-sm font-semibold')
                    ui.button('My Orders', on_click=lambda: ui.navigate.to('/orders')).props('flat color=white').classes('text-xs text-gray-300 hover:text-white capitalize ml-2')
                    ui.button(icon='logout', on_click=lambda: handle_logout()).props('flat round color=white size=sm')
            else:
                ui.button('Sign In', on_click=lambda: ui.navigate.to('/login')).classes('btn-secondary px-4 py-1 text-xs')

def handle_logout():
    auth.logout_user()
    ui.notify('Logged out successfully', type='info')
    ui.navigate.to('/')

def footer():
    with ui.footer().classes('bg-[#070913] border-t border-gray-800 text-center py-6 text-sm text-gray-500 mt-12 w-full'):
        ui.label('© 2026 shopEz E-Commerce. Made with 100% Python and NiceGUI.').classes('font-medium')
