import os

BASE_DIR = os.getenv('WM_BASE_DIR', os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, '..', 'config', 'templates_field.json')
TEMPLATES_DIR = os.path.join(BASE_DIR, '..', 'jinja_templates')
