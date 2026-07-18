import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
DATABASE_PATH = os.path.join(BASE_DIR, 'shopez.db')

# NiceGUI Session Secret
# (In production, this should be loaded from environment variables)
STORAGE_SECRET = 'shopez_super_secure_secret_key_2026_rfv_tgb'

# E-Commerce Configurations
STORE_NAME = 'shopEz'
CATEGORIES = [
    'Electronics',
    'Wearables',
    'Audio',
    'Smart Home',
    'Accessories'
]
