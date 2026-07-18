from nicegui import ui, app
import auth
from views import common

class LoginState:
    def __init__(self):
        self.mode = 'login' # 'login' or 'register'
        self.username = ''
        self.email = ''
        self.password = ''

@ui.page('/login')
def login_page():
    if auth.is_logged_in():
        ui.navigate.to('/')
        return
        
    common.setup_page('shopEz - Authentication')
    common.header_navigation()
    
    state = LoginState()
    
    with ui.column().classes('w-full items-center justify-center py-16 px-4'):
        # Glassmorphic auth card
        auth_container = ui.element('div').classes('w-full max-w-md')
        with auth_container:
            render_auth_form(auth_container, state)
            
    common.footer()

@ui.refreshable
def render_auth_form(parent, state):
    with ui.card().classes('shopez-card p-8 w-full gap-6 bg-white/5 border border-white/10 rounded-2xl shadow-2xl'):
        # Logo or Title header
        with ui.column().classes('w-full items-center mb-2'):
            ui.label('shopEz').classes('shopez-logo text-center text-4xl')
            ui.label('Your Ultimate Digital Mall').classes('text-xs text-gray-500 font-semibold tracking-wide uppercase mt-1')
            
        # Toggle tabs
        with ui.row().classes('w-full bg-black/30 p-1 rounded-xl border border-gray-800/80 mb-2'):
            login_tab_btn = ui.button(
                'Sign In', 
                on_click=lambda: switch_mode('login')
            ).classes(f"flex-grow py-2 rounded-lg text-sm capitalize {'btn-primary' if state.mode == 'login' else 'bg-transparent text-gray-400'}")
            login_tab_btn.props('flat' if state.mode != 'login' else '')
            
            register_tab_btn = ui.button(
                'Create Account', 
                on_click=lambda: switch_mode('register')
            ).classes(f"flex-grow py-2 rounded-lg text-sm capitalize {'btn-primary' if state.mode == 'register' else 'bg-transparent text-gray-400'}")
            register_tab_btn.props('flat' if state.mode != 'register' else '')
            
        # Form inputs
        with ui.column().classes('w-full gap-4'):
            username_input = ui.input(
                'Username', 
                value=state.username,
                on_change=lambda e: setattr(state, 'username', e.value)
            ).classes('w-full shopez-input').props('required icon=person label-color=purple')
            
            if state.mode == 'register':
                email_input = ui.input(
                    'Email Address', 
                    value=state.email,
                    on_change=lambda e: setattr(state, 'email', e.value)
                ).classes('w-full shopez-input').props('required type=email icon=email label-color=purple')
                
            password_input = ui.input(
                'Password', 
                password=True, 
                value=state.password,
                on_change=lambda e: setattr(state, 'password', e.value)
            ).classes('w-full shopez-input').props('required icon=lock label-color=purple')
            password_input.on('keydown.enter', lambda: submit_form())
            
        # Error / Info section
        action_btn_text = 'Sign In' if state.mode == 'login' else 'Register & Sign In'
        ui.button(
            action_btn_text, 
            on_click=lambda: submit_form()
        ).classes('btn-gradient-glow w-full py-3 mt-4').props('icon=login' if state.mode == 'login' else 'icon=person_add')
        
        # Test Credentials helper
        if state.mode == 'login':
            with ui.column().classes('w-full bg-purple-500/5 border border-purple-500/10 p-3 rounded-lg text-xs text-gray-400 gap-1 mt-2'):
                ui.label('Demo Admin credentials (if DB is freshly initialized):').classes('font-bold text-purple-300')
                ui.label('Register the very first user (it automatically becomes the Administrator).').classes('italic')
                ui.label('Subsequent registered users are standard Customers.').classes('italic')

    def switch_mode(mode):
        state.mode = mode
        render_auth_form.refresh(parent, state)
        
    def submit_form():
        if state.mode == 'login':
            success, msg = auth.login_user(state.username, state.password)
            if success:
                ui.notify(msg, type='positive')
                ui.navigate.to('/')
            else:
                ui.notify(msg, type='negative')
        else:
            success, msg = auth.register_user(state.username, state.email, state.password)
            if success:
                ui.notify(msg, type='positive')
                # Auto-login
                auth.login_user(state.username, state.password)
                ui.navigate.to('/')
            else:
                ui.notify(msg, type='negative')
