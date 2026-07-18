from nicegui import ui, app
import auth
import database
from views import common

@ui.page('/orders')
def orders_page():
    if not auth.is_logged_in():
        ui.navigate.to('/login')
        return
        
    common.setup_page('shopEz - My Orders')
    common.header_navigation()
    
    user_id = auth.get_current_user_id()
    orders = database.get_orders_by_user(user_id)
    
    with ui.column().classes('w-full max-w-5xl mx-auto px-4 md:px-8 py-8 gap-6'):
        with ui.row().classes('w-full justify-between items-center border-b border-gray-800 pb-4'):
            ui.label('Order History').classes('text-2xl md:text-3xl font-extrabold text-white')
            ui.button('Back to Shop', on_click=lambda: ui.navigate.to('/')).classes('btn-secondary px-4 py-2').props('icon=arrow_back')
            
        if not orders:
            with ui.column().classes('w-full items-center justify-center py-20 text-center gap-4'):
                ui.icon('receipt_long').classes('text-gray-600 text-8xl mb-2')
                ui.label('No Orders Yet').classes('text-2xl font-bold text-white')
                ui.label("You haven't placed any orders yet. Start exploring our premium products!").classes('text-gray-400 max-w-sm')
                ui.button('Start Shopping', on_click=lambda: ui.navigate.to('/')).classes('btn-primary px-8 py-3')
        else:
            with ui.column().classes('w-full gap-6'):
                for order in orders:
                    with ui.card().classes('shopez-card p-5 w-full bg-white/5 border border-white/10 rounded-2xl gap-3'):
                        # Order Header info
                        with ui.row().classes('w-full justify-between items-center flex-wrap gap-2 border-b border-gray-800/60 pb-3'):
                            with ui.row().classes('items-center gap-3'):
                                ui.label(f"Order #{order['id']}").classes('font-mono font-bold text-white text-base')
                                ui.label(order['created_at']).classes('text-xs text-gray-400')
                            
                            # Status Badge
                            status = order['status']
                            status_color = 'success' if status in ('Paid', 'Delivered') else 'warning'
                            ui.label(status).classes(f"text-xs font-bold px-3 py-1 rounded-full bg-{status_color}/20 text-{status_color} border border-{status_color}/30")
                            
                        # Shipping Details
                        with ui.row().classes('items-center gap-2 text-xs text-gray-400'):
                            ui.icon('local_shipping', size='xs')
                            ui.label(f"Shipped to: {order['shipping_address']}")
                            
                        # Items Ordered
                        with ui.column().classes('w-full pl-4 border-l-2 border-purple-500/40 gap-3 mt-2'):
                            for item in order['items']:
                                with ui.row().classes('w-full items-center justify-between gap-4 text-sm'):
                                    with ui.row().classes('items-center gap-3 min-w-0'):
                                        ui.html(f'<img src="{item["image_url"]}" class="w-12 h-12 object-cover rounded-xl bg-white/5 border border-white/10" />')
                                        with ui.column().classes('gap-0.5 min-w-0'):
                                            ui.label(item['name']).classes('text-gray-200 font-semibold line-clamp-1')
                                            ui.label(f"${item['price']:.2f} each").classes('text-xs text-gray-500')
                                    
                                    with ui.row().classes('items-center gap-4'):
                                        ui.label(f"Qty: {item['quantity']}").classes('text-xs text-gray-400 font-bold')
                                        ui.label(f"${(item['price'] * item['quantity']):.2f}").classes('text-sm font-bold text-white w-20 text-right')
                                        
                        # Summary total footer
                        with ui.row().classes('w-full justify-between items-center mt-3 border-t border-gray-800/40 pt-3'):
                            ui.label('Order Summary').classes('text-xs text-gray-500')
                            with ui.row().classes('items-center'):
                                ui.label('Grand Total:').classes('text-xs text-gray-400 mr-2')
                                ui.label(f"${order['total_amount']:.2f}").classes('text-lg font-extrabold text-purple-400')
                                
    common.footer()
