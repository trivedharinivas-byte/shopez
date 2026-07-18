from nicegui import ui, app
import auth
import database
from views import common

@ui.page('/cart')
def cart_page():
    if not auth.is_logged_in():
        ui.navigate.to('/login')
        return
        
    common.setup_page('shopEz - Shopping Cart')
    common.header_navigation()
    
    with ui.column().classes('w-full max-w-6xl mx-auto px-4 md:px-8 py-8 gap-6'):
        ui.label('Your Shopping Cart').classes('text-2xl md:text-3xl font-extrabold text-white border-b-2 border-purple-500 pb-1 align-self-start')
        
        # We put the interactive cart contents inside a refreshable container
        cart_content_container = ui.element('div').classes('w-full')
        with cart_content_container:
            render_cart_view(cart_content_container)
            
    common.footer()

@ui.refreshable
def render_cart_view(parent_container):
    user_id = auth.get_current_user_id()
    items = database.get_cart_items(user_id)
    
    if not items:
        with ui.column().classes('w-full items-center justify-center py-20 text-center gap-4'):
            ui.icon('shopping_cart_checkout').classes('text-gray-600 text-8xl mb-2')
            ui.label('Your Cart is Empty').classes('text-2xl font-bold text-white')
            ui.label('Browse our catalog and add items to your cart to begin shopping.').classes('text-gray-400 max-w-sm')
            ui.button('Start Shopping', on_click=lambda: ui.navigate.to('/')).classes('btn-primary px-8 py-2')
        return
        
    # Cart details layout: Grid with Left = items table, Right = summary card
    with ui.row().classes('w-full gap-8 md:flex-nowrap flex-wrap'):
        
        # Left Panel: Cart items
        with ui.column().classes('w-full md:w-2/3 gap-4'):
            for item in items:
                p_id = item['id']
                price = item['price']
                quantity = item['quantity']
                stock = item['stock']
                item_total = price * quantity
                
                with ui.card().classes('shopez-card p-4 flex flex-row items-center gap-4 w-full justify-between'):
                    # Product Thumbnail
                    with ui.element('div').classes('w-20 h-20 rounded-xl overflow-hidden bg-white/5 border border-white/10 flex-shrink-0 cursor-pointer').on('click', lambda pid=p_id: ui.navigate.to(f'/product/{pid}')):
                        ui.html(f'<img src="{item["image_url"]}" class="w-full h-full object-cover" />')
                        
                    # Product Details & Info
                    with ui.column().classes('flex-grow gap-0.5 min-w-0'):
                        ui.label(item['name']).classes('text-base font-bold text-white line-clamp-1 cursor-pointer').on('click', lambda pid=p_id: ui.navigate.to(f'/product/{pid}'))
                        ui.label(item['category']).classes('text-xs text-purple-400 font-semibold uppercase tracking-wider')
                        ui.label(f"${price:.2f} each").classes('text-xs text-gray-400')
                        
                    # Quantity controls & Subtotal
                    with ui.row().classes('items-center gap-4 flex-shrink-0'):
                        # Quantity control box
                        with ui.row().classes('items-center border border-gray-700 rounded-lg overflow-hidden bg-black/20'):
                            def update_qty(pid, new_qty):
                                if new_qty <= 0:
                                    database.remove_from_cart(user_id, pid)
                                else:
                                    success, msg = database.update_cart_quantity(user_id, pid, new_qty)
                                    if not success:
                                        ui.notify(msg, type='warning')
                                        return
                                render_cart_view.refresh(parent_container)
                                
                            ui.button('-', on_click=lambda pid=p_id, q=quantity: update_qty(pid, q-1)).props('flat text-color=white size=sm').classes('px-1 min-h-0')
                            ui.label(str(quantity)).classes('px-2 text-xs text-white font-bold')
                            ui.button('+', on_click=lambda pid=p_id, q=quantity: update_qty(pid, q+1)).props('flat text-color=white size=sm').classes('px-1 min-h-0')
                        
                        # Total price
                        ui.label(f"${item_total:.2f}").classes('text-sm font-bold text-white w-20 text-right')
                        
                        # Remove button
                        ui.button(
                            icon='delete_outline', 
                            on_click=lambda pid=p_id: [database.remove_from_cart(user_id, pid), render_cart_view.refresh(parent_container), ui.notify('Item removed', type='info')]
                        ).props('flat round color=red size=sm')
                        
        # Right Panel: Order Summary
        with ui.column().classes('w-full md:w-1/3'):
            with ui.card().classes('shopez-card p-6 w-full gap-4 bg-white/5 border border-white/10 rounded-2xl'):
                ui.label('Order Summary').classes('text-lg font-bold text-white border-b border-gray-800 pb-2')
                
                # Pricing breakdown
                subtotal = sum(item['price'] * item['quantity'] for item in items)
                shipping = 0.0 if subtotal >= 150 else 9.99
                tax = subtotal * 0.08  # 8% Tax
                grand_total = subtotal + shipping + tax
                
                with ui.row().classes('justify-between w-full text-sm text-gray-400'):
                    ui.label('Subtotal')
                    ui.label(f"${subtotal:.2f}").classes('text-white font-semibold')
                    
                with ui.row().classes('justify-between w-full text-sm text-gray-400'):
                    ui.label('Estimated Shipping')
                    if shipping == 0:
                        ui.label('FREE').classes('text-success font-bold')
                    else:
                        ui.label(f"${shipping:.2f}").classes('text-white font-semibold')
                        
                with ui.row().classes('justify-between w-full text-sm text-gray-400'):
                    ui.label('Tax (8%)')
                    ui.label(f"${tax:.2f}").classes('text-white font-semibold')
                    
                ui.element('div').classes('w-full h-px bg-gray-800 my-1')
                
                with ui.row().classes('justify-between w-full text-base font-bold'):
                    ui.label('Grand Total')
                    ui.label(f"${grand_total:.2f}").classes('text-purple-400')
                    
                # Checkout buttons
                ui.button(
                    'Proceed to Checkout', 
                    on_click=lambda: ui.navigate.to('/checkout')
                ).classes('btn-gradient-glow w-full py-3 mt-2').props('icon=payment')
                
                ui.button(
                    'Clear All Items', 
                    on_click=lambda: [database.clear_cart(user_id), render_cart_view.refresh(parent_container), ui.notify('Cart cleared', type='info')]
                ).classes('btn-secondary w-full py-2').props('icon=delete_sweep')
                
                # Promo alert
                if subtotal < 150:
                    rem = 150 - subtotal
                    with ui.row().classes('items-center bg-purple-500/10 border border-purple-500/20 p-2.5 rounded-lg gap-2 mt-2 w-full'):
                        ui.icon('local_offer', size='xs', color='secondary')
                        ui.label(f'Add ${rem:.2f} more to unlock FREE shipping!').classes('text-xs text-purple-300 font-semibold')
