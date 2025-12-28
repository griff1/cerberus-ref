"""
Wrapper to import Cerberus middleware from cerberus_django package.

This file adds the cerberus/src directory to the Python path so the
cerberus_django package can be imported.
"""
import sys
import os

# Path to the cerberus/src directory (relative to this file)
# This file is in cerberus-ref/cerberus_ref/
# Middleware package is in cerberus/src/cerberus_django/
_this_dir = os.path.dirname(os.path.abspath(__file__))
_cerberus_src_dir = os.path.abspath(os.path.join(_this_dir, '..', '..', 'cerberus', 'src'))

# Add the src directory to Python path so we can import cerberus_django
if _cerberus_src_dir not in sys.path:
    sys.path.insert(0, _cerberus_src_dir)

# Import the cerberus_django package (normal import now that the name is valid)
from cerberus_django import CerberusMiddleware

# Re-export for backward compatibility
__all__ = ['CerberusMiddleware']
