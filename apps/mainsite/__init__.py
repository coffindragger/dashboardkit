import sys
import os


__all__ = ['APPS_DIR','TOP_DIR','import_settings']

# assume we are ./apps/mainsite/__init__.py
APPS_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

# Path to the whole project (one level up from apps)
TOP_DIR = os.path.dirname(APPS_DIR)
