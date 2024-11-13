import os
import sys
from dotenv import load_dotenv

def load_env():
    """
    Loads environment variables from a .env file and adds PYTHONPATH.
    """
    load_dotenv()
    python_path = os.getenv("PYTHONPATH")
    if python_path:
        sys.path.append(python_path)
