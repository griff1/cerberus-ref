"""
Wrapper to import Cerberus middleware from cerberus-django package.

This file exists because the source package uses 'cerberus-django' (with hyphens)
which cannot be directly imported in Python. We add the package directory to
sys.path and import it.
"""
import importlib
import sys
import os

# Path to the cerberus/src directory (relative to this file)
# This file is in cerberus-ref/cerberus_ref/
# Middleware package is in cerberus/src/cerberus-django/
_this_dir = os.path.dirname(os.path.abspath(__file__))
_cerberus_src_dir = os.path.abspath(os.path.join(_this_dir, '..', '..', 'cerberus', 'src'))

# Add the src directory to Python path so we can import cerberus-django
if _cerberus_src_dir not in sys.path:
    sys.path.insert(0, _cerberus_src_dir)

# Import the cerberus-django package
# We use importlib because the package name has hyphens
cerberus_django = importlib.import_module('cerberus-django')

# Re-export the middleware class (already exported by __init__.py)
CerberusMiddleware = cerberus_django.CerberusMiddleware
