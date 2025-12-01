"""
Wrapper to import Cerberus middleware from cerberus-django package.

This file exists because the source package uses 'cerberus-django' (with hyphens)
which cannot be directly imported in Python. We use importlib to load it.
"""
import importlib.util
import sys
import os

# Path to the cerberus-django middleware
CERBERUS_PATH = os.path.expanduser('~/Documents/cerberus/src/cerberus-django/middleware.py')

# Load the middleware module dynamically
spec = importlib.util.spec_from_file_location("cerberus_middleware_module", CERBERUS_PATH)
cerberus_module = importlib.util.module_from_spec(spec)
sys.modules['cerberus_middleware_module'] = cerberus_module
spec.loader.exec_module(cerberus_module)

# Export the middleware class
CerberusMiddleware = cerberus_module.CerberusMiddleware
