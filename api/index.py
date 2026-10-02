import sys
import os

# Add project root to path so all modules resolve correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

# Vercel expects a WSGI app exported as `app`
