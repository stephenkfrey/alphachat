import os
import sys
from pathlib import Path
sys.path.append(os.path.dirname(__file__))
# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
