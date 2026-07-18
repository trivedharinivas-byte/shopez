import os
import mimetypes
from nicegui import ui, app
import config
import database

# Explicitly register SVG MIME type for Windows systems
mimetypes.add_type('image/svg+xml', '.svg')

# Initialize Database and Seed Data
database.init_db()

# Serve CSS stylesheet from /static/styles.css
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.add_static_files('/static', static_dir)

# Import views to trigger page route registrations
import views.home
import views.product
import views.cart
import views.checkout
import views.login
import views.admin
import views.orders

# Configure default page styles (removes default NiceGUI borders/padding if necessary)
# and injects global styles
@app.middleware
async def middleware(request, call_next):
    # Standard FastAPI middleware to add headers if desired
    response = await call_next(request)
    return response

# Start the Application
if __name__ in {"__main__", "__mp_main__"}:
    print(f"Starting {config.STORE_NAME} server...")
    ui.run(
        title=config.STORE_NAME,
        host='127.0.0.1',
        port=8080,
        storage_secret=config.STORAGE_SECRET,
        reload=True,
        dark=True
    )
