from nicegui import ui, app
import auth
import database
from config import CATEGORIES
from views import common

# State variables for filters (NiceGUI retains state per-connection, but we can bind to UI inputs)
class FilterState:
    def __init__(self):
        self.search_query = ''
        self.category = 'All'

@ui.page('/')
def home_page():
    common.setup_page('shopEz - Shop Smarter, Live Better')
    common.header_navigation()
    
    # Store page-level filter state
    state = FilterState()
    
    with ui.column().classes('w-full max-w-7xl mx-auto px-4 md:px-8 py-8 gap-8'):
        
        # Hero Banner
        with ui.element('div').classes('hero-section flex flex-col md:flex-row justify-between items-center gap-6'):
            with ui.column().classes('max-w-xl'):
                ui.label('Upgrade Your').classes('text-sm uppercase tracking-wider text-purple-400 font-bold')
                ui.label('Smart Lifestyle.').classes('hero-glow-text')
                ui.label('Explore our handpicked collection of premium gadgets, high-fidelity audio, and smart home innovations styled for the future.').classes('hero-subtext')
                with ui.row().classes('gap-4'):
                    ui.button('Shop Collection', on_click=lambda: ui.scroll_to(catalog_section)).classes('btn-primary px-6 py-2')
                    ui.button('Learn More', on_click=lambda: ui.notify('shopEz Version 1.0. Developed in 100% Python!', type='info')).classes('btn-secondary px-6 py-2')
            
            # Interactive visual accent (instead of a static image placeholder)
            with ui.column().classes('items-center justify-center relative w-64 h-64 md:mr-12'):
                # Display a glowing core using custom styling
                ui.html('''
                    <div style="
                        width: 150px; 
                        height: 150px; 
                        background: radial-gradient(circle, rgba(139,92,246,1) 0%, rgba(236,72,153,1) 100%); 
                        border-radius: 50%; 
                        filter: blur(40px);
                        opacity: 0.6;
                        animation: pulse 4s infinite alternate;
                    "></div>
                    <style>
                        @keyframes pulse {
                            0% { transform: scale(0.9); opacity: 0.5; }
                            100% { transform: scale(1.1); opacity: 0.8; }
                        }
                    </style>
                ''').classes('absolute')
                ui.icon('shopping_bag').classes('text-8xl text-purple-300 relative z-10 drop-shadow-[0_0_25px_rgba(139,92,246,0.6)]')
                
        # Catalog Anchor
        catalog_section = ui.element('div').classes('w-full')
        
        # Search and Category Filters
        with ui.column().classes('w-full gap-4'):
            with ui.row().classes('w-full items-center justify-between gap-4'):
                ui.label('Featured Products').classes('text-2xl font-bold text-white border-b-2 border-purple-500 pb-1')
                
                # Search Bar
                search_input = ui.input(
                    placeholder='Search products...', 
                    on_change=lambda e: update_search(e.value)
                ).classes('w-full md:w-80 shopez-input').props('clearable')
                search_input.on('keydown.enter', lambda: update_search(search_input.value))
            
            # Category Chips
            with ui.row().classes('flex-wrap gap-2 py-2'):
                # Add "All" option
                all_chip = ui.button('All Products', on_click=lambda: select_category('All')).classes('category-chip active')
                category_chips = {'All': all_chip}
                
                for cat in CATEGORIES:
                    chip = ui.button(cat, on_click=lambda c=cat: select_category(c)).classes('category-chip')
                    category_chips[cat] = chip
                    
        # Dynamic Product List
        with ui.row().classes('w-full'):
            product_list_container = ui.element('div').classes('w-full')
            with product_list_container:
                product_grid_view()

    # Filter Updates
    def update_search(val):
        state.search_query = val or ''
        refresh_grid()
        
    def select_category(cat):
        state.category = cat
        # Update active states of chips
        for c, chip in category_chips.items():
            if c == cat:
                chip.classes(add='active')
            else:
                chip.classes(remove='active')
        refresh_grid()
        
    def refresh_grid():
        product_list_container.clear()
        with product_list_container:
            product_grid_view(state.search_query, state.category)

    common.footer()

@ui.refreshable
def product_grid_view(search_query='', selected_category='All'):
    if selected_category == 'All' and not search_query:
        products = database.get_all_products()
    else:
        products = database.search_products(search_query, selected_category)
        
    if not products:
        with ui.column().classes('w-full items-center justify-center py-16 text-center'):
            ui.icon('search_off').classes('text-gray-600 text-6xl mb-2')
            ui.label('No products found matching your search.').classes('text-gray-400 font-semibold text-lg')
            ui.label('Try adjusting your keywords or category filters.').classes('text-gray-500 text-sm')
        return
        
    with ui.row().classes('product-grid'):
        for prod in products:
            p_id = prod['id']
            with ui.card().classes('shopez-card product-card'):
                # Product Image
                with ui.element('div').classes('product-image-container cursor-pointer').on('click', lambda pid=p_id: ui.navigate.to(f'/product/{pid}')):
                    ui.html(f'<img src="{prod["image_url"]}" class="product-image" />')
                    ui.label(prod['category']).classes('product-badge')
                    
                # Product Details
                ui.label(prod['name']).classes('text-lg font-bold text-gray-100 line-clamp-1 cursor-pointer mt-2').on('click', lambda pid=p_id: ui.navigate.to(f'/product/{pid}'))
                ui.label(prod['description']).classes('text-xs text-gray-400 line-clamp-2 mt-1 flex-grow')
                
                # Bottom Row
                with ui.row().classes('w-full items-center justify-between mt-4 pt-2 border-t border-gray-800/60'):
                    ui.label(f"{prod['price']:.2f}").classes('product-price')
                    
                    if prod['stock'] <= 0:
                        ui.label('Out of stock').classes('text-error text-xs font-semibold')
                    else:
                        ui.button(
                            icon='add_shopping_cart', 
                            on_click=lambda pid=p_id: handle_add_to_cart(pid)
                        ).classes('btn-primary p-2 min-h-0 size-10').props('round')

def handle_add_to_cart(product_id):
    if not auth.is_logged_in():
        ui.notify('Please sign in to add items to your cart.', type='warning', action='Sign In', on_action=lambda: ui.navigate.to('/login'))
        return
        
    user_id = auth.get_current_user_id()
    success, msg = database.add_to_cart(user_id, product_id, 1)
    if success:
        ui.notify('Added to shopping cart!', type='positive', position='bottom-right')
        # Refresh the home page to update navigation cart badge
        ui.navigate.to('/')
    else:
        ui.notify(msg, type='negative')
