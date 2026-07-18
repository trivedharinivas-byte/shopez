from nicegui import ui, app
import auth
import database
from views import common

@ui.page('/checkout')
def checkout_page():
    if not auth.is_logged_in():
        ui.navigate.to('/login')
        return
        
    user_id = auth.get_current_user_id()
    items = database.get_cart_items(user_id)
    
    if not items:
        ui.navigate.to('/cart')
        return
        
    common.setup_page('shopEz - Checkout')
    common.header_navigation()
    
    # Financial calculations
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    shipping = 0.0 if subtotal >= 150 else 9.99
    tax = subtotal * 0.08
    grand_total = subtotal + shipping + tax
    
    # Form states
    form_data = {
        'fullname': '',
        'street': '',
        'city': '',
        'zipcode': '',
        'country': 'United States',
        'cardname': '',
        'cardnum': '',
        'cardexp': '',
        'cardcvv': ''
    }
    
    with ui.column().classes('w-full max-w-6xl mx-auto px-4 md:px-8 py-8 gap-6'):
        ui.label('Safe Checkout').classes('text-2xl md:text-3xl font-extrabold text-white border-b-2 border-purple-500 pb-1 align-self-start')
        
        # Back to cart
        with ui.row().classes('items-center cursor-pointer text-gray-400 hover:text-white transition-colors').on('click', lambda: ui.navigate.to('/cart')):
            ui.icon('arrow_back').classes('mr-1')
            ui.label('Back to Shopping Cart').classes('text-sm font-semibold')
            
        with ui.row().classes('w-full gap-8 md:flex-nowrap flex-wrap'):
            # Left panel: Shipping & Payment forms
            with ui.column().classes('w-full md:w-2/3 gap-6'):
                
                # Shipping Address
                with ui.card().classes('shopez-card p-6 w-full gap-4'):
                    with ui.row().classes('items-center gap-2 border-b border-gray-800 pb-2 w-full'):
                        ui.icon('local_shipping', color='purple').classes('text-xl')
                        ui.label('1. Shipping Address').classes('text-lg font-bold text-white')
                        
                    with ui.column().classes('w-full gap-3'):
                        fullname_input = ui.input(
                            'Full Name', 
                            on_change=lambda e: form_data.update({'fullname': e.value})
                        ).classes('w-full shopez-input').props('required label-color=purple')
                        
                        street_input = ui.input(
                            'Street Address', 
                            on_change=lambda e: form_data.update({'street': e.value})
                        ).classes('w-full shopez-input').props('required label-color=purple')
                        
                        with ui.row().classes('w-full gap-4'):
                            city_input = ui.input(
                                'City', 
                                on_change=lambda e: form_data.update({'city': e.value})
                            ).classes('flex-grow shopez-input').props('required label-color=purple')
                            
                            zip_input = ui.input(
                                'ZIP / Postal Code', 
                                on_change=lambda e: form_data.update({'zipcode': e.value})
                            ).classes('w-32 shopez-input').props('required label-color=purple')
                            
                            country_input = ui.select(
                                ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'India', 'Australia'], 
                                value='United States',
                                on_change=lambda e: form_data.update({'country': e.value})
                            ).classes('w-44 shopez-input').props('required label-color=purple')
                
                # Payment details (Mock)
                with ui.card().classes('shopez-card p-6 w-full gap-4'):
                    with ui.row().classes('items-center gap-2 border-b border-gray-800 pb-2 w-full'):
                        ui.icon('credit_card', color='purple').classes('text-xl')
                        ui.label('2. Mock Credit Card Payment').classes('text-lg font-bold text-white')
                        
                    ui.label('Do not enter real credit card details. Enter dummy details for demo testing.').classes('text-xs text-warning bg-warning/5 border border-warning/20 p-2 rounded-lg w-full')
                    
                    with ui.column().classes('w-full gap-3'):
                        cardname_input = ui.input(
                            'Cardholder Name', 
                            on_change=lambda e: form_data.update({'cardname': e.value})
                        ).classes('w-full shopez-input').props('required label-color=purple')
                        
                        cardnum_input = ui.input(
                            'Card Number', 
                            placeholder='1111-2222-3333-4444',
                            on_change=lambda e: form_data.update({'cardnum': e.value})
                        ).classes('w-full shopez-input').props('required label-color=purple mask="####-####-####-####"')
                        
                        with ui.row().classes('w-full gap-4'):
                            cardexp_input = ui.input(
                                'Expiration Date', 
                                placeholder='MM/YY',
                                on_change=lambda e: form_data.update({'cardexp': e.value})
                            ).classes('flex-grow shopez-input').props('required label-color=purple mask="##/##"')
                            
                            cardcvv_input = ui.input(
                                'CVV / Security Code', 
                                placeholder='123',
                                on_change=lambda e: form_data.update({'cardcvv': e.value})
                            ).classes('w-32 shopez-input').props('required label-color=purple mask="###"')
            
            # Right panel: Order review
            with ui.column().classes('w-full md:w-1/3 gap-4'):
                with ui.card().classes('shopez-card p-6 w-full gap-4'):
                    ui.label('Review Order').classes('text-lg font-bold text-white border-b border-gray-800 pb-2')
                    
                    # Cart summary listing
                    with ui.column().classes('w-full gap-3 max-h-60 overflow-y-auto pr-1'):
                        for item in items:
                            with ui.row().classes('w-full items-center justify-between gap-2'):
                                with ui.row().classes('items-center gap-2 min-w-0'):
                                    ui.html(f'<img src="{item["image_url"]}" class="w-10 h-10 object-cover rounded-lg flex-shrink-0" />')
                                    with ui.column().classes('min-w-0 gap-0.5'):
                                        ui.label(item['name']).classes('text-xs font-bold text-white line-clamp-1')
                                        ui.label(f"Qty: {item['quantity']}").classes('text-[10px] text-gray-400')
                                ui.label(f"${(item['price'] * item['quantity']):.2f}").classes('text-xs font-bold text-gray-300 flex-shrink-0')
                                
                    ui.element('div').classes('w-full h-px bg-gray-800')
                    
                    # Totals
                    with ui.row().classes('justify-between w-full text-xs text-gray-400'):
                        ui.label('Subtotal')
                        ui.label(f"${subtotal:.2f}").classes('text-white font-semibold')
                        
                    with ui.row().classes('justify-between w-full text-xs text-gray-400'):
                        ui.label('Shipping')
                        if shipping == 0:
                            ui.label('FREE').classes('text-success font-bold')
                        else:
                            ui.label(f"${shipping:.2f}").classes('text-white font-semibold')
                            
                    with ui.row().classes('justify-between w-full text-xs text-gray-400'):
                        ui.label('Estimated Tax (8%)')
                        ui.label(f"${tax:.2f}").classes('text-white font-semibold')
                        
                    ui.element('div').classes('w-full h-px bg-gray-800')
                    
                    with ui.row().classes('justify-between w-full text-base font-bold'):
                        ui.label('Total Amount')
                        ui.label(f"${grand_total:.2f}").classes('text-purple-400')
                        
                    # Place order trigger
                    def handle_place_order():
                        # Validate shipping details
                        if not form_data['fullname'] or not form_data['street'] or not form_data['city'] or not form_data['zipcode']:
                            ui.notify('Please fill out all shipping details.', type='warning')
                            return
                        # Validate payment details
                        if not form_data['cardname'] or not form_data['cardnum'] or not form_data['cardexp'] or not form_data['cardcvv']:
                            ui.notify('Please fill out all credit card credentials.', type='warning')
                            return
                            
                        shipping_addr = f"{form_data['fullname']}, {form_data['street']}, {form_data['city']}, {form_data['zipcode']}, {form_data['country']}"
                        
                        order_id, msg = database.create_order(user_id, shipping_addr)
                        
                        if order_id:
                            ui.notify('Payment processed and order placed!', type='positive')
                            ui.navigate.to(f'/order-success/{order_id}')
                        else:
                            ui.notify(msg, type='negative')
                            
                    ui.button(
                        'Confirm & Place Order', 
                        on_click=handle_place_order
                    ).classes('btn-gradient-glow w-full py-3 mt-2').props('icon=check_circle')
                    
    common.footer()

@ui.page('/order-success/{order_id}')
def order_success_page(order_id: int):
    if not auth.is_logged_in():
        ui.navigate.to('/login')
        return
        
    common.setup_page(f"shopEz - Order #{order_id} Success")
    common.header_navigation()
    
    with ui.column().classes('w-full max-w-lg mx-auto px-4 py-16 items-center justify-center text-center gap-6'):
        # Success animated icon (glowing)
        with ui.element('div').classes('rounded-full bg-success/10 border border-success/30 p-4 drop-shadow-[0_0_20px_rgba(16,185,129,0.3)]'):
            ui.icon('verified', color='success').classes('text-6xl')
            
        ui.label('Thank You for Your Order!').classes('text-3xl font-extrabold text-white')
        
        with ui.column().classes('w-full bg-white/5 border border-white/10 p-5 rounded-2xl gap-3 text-left'):
            with ui.row().classes('justify-between w-full'):
                ui.label('Order ID:').classes('text-xs text-gray-400 font-medium')
                ui.label(f"#{order_id}").classes('text-xs text-white font-bold')
                
            with ui.row().classes('justify-between w-full'):
                ui.label('Status:').classes('text-xs text-gray-400 font-medium')
                ui.label('Paid & Confirmed').classes('text-xs text-success font-bold')
                
            ui.label('Estimated Delivery: 3-5 Business Days').classes('text-xs text-purple-300 font-semibold bg-purple-500/10 p-2 rounded-lg text-center w-full mt-1')
            
        ui.label('A confirmation receipt and tracking updates have been sent to your registered email address.').classes('text-sm text-gray-400 leading-relaxed')
        
        with ui.row().classes('gap-4 mt-2'):
            ui.button('Back to Catalog', on_click=lambda: ui.navigate.to('/')).classes('btn-primary px-6 py-2')
            ui.button('View Orders', on_click=lambda: ui.navigate.to('/admin') if auth.is_admin() else ui.navigate.to('/orders')).classes('btn-secondary px-6 py-2')
            
    common.footer()
