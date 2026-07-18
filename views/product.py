from nicegui import ui, app
import auth
import database
from views import common

@ui.page('/product/{product_id}')
def product_detail_page(product_id: int):
    # Fetch product from DB
    product = database.get_product_by_id(product_id)
    
    if not product:
        common.setup_page('Product Not Found')
        common.header_navigation()
        with ui.column().classes('w-full items-center justify-center py-20 text-center gap-4'):
            ui.icon('warning', color='warning').classes('text-7xl')
            ui.label('Product Not Found').classes('text-2xl font-bold text-white')
            ui.label('The product you are looking for does not exist or has been removed.').classes('text-gray-400')
            ui.button('Back to Catalog', on_click=lambda: ui.navigate.to('/')).classes('btn-primary px-6 py-2')
        common.footer()
        return

    common.setup_page(f"shopEz - {product['name']}")
    common.header_navigation()
    
    # Page state
    qty_state = {'qty': 1}
    
    with ui.column().classes('w-full max-w-6xl mx-auto px-4 md:px-8 py-8 gap-8'):
        
        # Back button
        with ui.row().classes('items-center cursor-pointer text-gray-400 hover:text-white transition-colors').on('click', lambda: ui.navigate.to('/')):
            ui.icon('arrow_back').classes('mr-1')
            ui.label('Back to Products').classes('text-sm font-semibold')
            
        # Product Grid details
        with ui.row().classes('w-full gap-8 md:flex-nowrap flex-wrap'):
            # Left: Image
            with ui.column().classes('w-full md:w-1/2'):
                with ui.element('div').classes('shopez-card p-4 w-full flex items-center justify-center bg-white/5 border border-white/10 rounded-2xl overflow-hidden aspect-video md:aspect-square'):
                    ui.html(f'<img src="{product["image_url"]}" class="w-full h-full object-cover rounded-xl shadow-2xl transition-transform duration-500 hover:scale-105" />')
            
            # Right: Info
            with ui.column().classes('w-full md:w-1/2 gap-4 justify-between'):
                with ui.column().classes('gap-2'):
                    # Category
                    ui.label(product['category'].upper()).classes('text-xs font-bold tracking-widest text-purple-400')
                    
                    # Title
                    ui.label(product['name']).classes('text-3xl md:text-4xl font-extrabold text-white leading-tight')
                    
                    # Mock Star Ratings for Premium Feel
                    with ui.row().classes('items-center gap-1'):
                        for _ in range(4):
                            ui.icon('star', color='warning').classes('text-sm')
                        ui.icon('star_half', color='warning').classes('text-sm')
                        ui.label('(4.8/5 rating from 24 customers)').classes('text-xs text-gray-400 ml-1')
                    
                    # Divider
                    ui.element('div').classes('w-full h-px bg-gray-800 my-2')
                    
                    # Price
                    ui.label(f"{product['price']:.2f}").classes('text-3xl font-extrabold text-purple-400 product-price')
                    
                    # Description
                    ui.label('Product Overview').classes('text-sm font-bold text-gray-200 mt-2')
                    ui.label(product['description']).classes('text-sm text-gray-400 leading-relaxed')
                    
                    # Stock info
                    stock_qty = product['stock']
                    if stock_qty <= 0:
                        ui.label('Out of Stock').classes('text-error font-bold text-sm mt-2')
                    elif stock_qty < 5:
                        ui.label(f'Only {stock_qty} left in stock - order soon!').classes('text-warning font-bold text-xs mt-2')
                    else:
                        ui.label(f'In Stock ({stock_qty} available)').classes('text-success font-medium text-xs mt-2')
                
                # Actions container
                if stock_qty > 0:
                    with ui.card().classes('bg-white/5 border border-white/10 p-4 rounded-xl w-full gap-4'):
                        with ui.row().classes('items-center justify-between w-full'):
                            ui.label('Quantity:').classes('text-sm text-gray-300 font-semibold')
                            
                            # Custom incrementer buttons
                            with ui.row().classes('items-center border border-gray-700 rounded-lg overflow-hidden bg-black/20'):
                                def dec_qty():
                                    if qty_state['qty'] > 1:
                                        qty_state['qty'] -= 1
                                        qty_label.set_text(str(qty_state['qty']))
                                        
                                def inc_qty():
                                    if qty_state['qty'] < stock_qty:
                                        qty_state['qty'] += 1
                                        qty_label.set_text(str(qty_state['qty']))
                                
                                ui.button('-', on_click=dec_qty).props('flat text-color=white size=sm').classes('px-2 min-h-0')
                                qty_label = ui.label(str(qty_state['qty'])).classes('px-3 text-sm text-white font-bold')
                                ui.button('+', on_click=inc_qty).props('flat text-color=white size=sm').classes('px-2 min-h-0')
                        
                        # Add to Cart Button
                        ui.button(
                            'Add to Shopping Cart', 
                            on_click=lambda: add_to_cart_detail(product['id'], qty_state['qty'])
                        ).classes('btn-gradient-glow w-full py-3').props('icon=add_shopping_cart')
                else:
                    ui.button('Temporarily Out of Stock').props('disabled').classes('w-full py-3 bg-gray-800 text-gray-500 rounded-xl')
                    
                # Specs List Accordion/Tabs Mock
                with ui.column().classes('w-full mt-4 bg-black/10 p-4 rounded-xl border border-gray-900/60'):
                    ui.label('Shipping & Return Details').classes('text-xs font-bold text-gray-300 uppercase tracking-wider')
                    with ui.row().classes('items-center text-xs text-gray-400 gap-2 mt-1'):
                        ui.icon('local_shipping', size='xs')
                        ui.label('Free express shipping on orders over $150')
                    with ui.row().classes('items-center text-xs text-gray-400 gap-2 mt-1'):
                        ui.icon('assignment_return', size='xs')
                        ui.label('30-day hassle-free returns & full warranty support')

    common.footer()

def add_to_cart_detail(product_id, quantity):
    if not auth.is_logged_in():
        ui.notify('Please sign in to add items to your cart.', type='warning', action='Sign In', on_action=lambda: ui.navigate.to('/login'))
        return
        
    user_id = auth.get_current_user_id()
    success, msg = database.add_to_cart(user_id, product_id, quantity)
    if success:
        ui.notify(f'Added {quantity} item(s) to shopping cart!', type='positive', position='bottom-right')
        # Redirect to cart
        ui.navigate.to('/cart')
    else:
        ui.notify(msg, type='negative')
