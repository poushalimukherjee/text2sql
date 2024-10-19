import os
import glob
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))

# Search for .db or .sqlite files in the databases folder
database_files = glob.glob(os.path.join(base_dir, '../databases/*.db'))\
      + glob.glob(os.path.join(base_dir, '../databases/*.sqlite'))

# Check if any database files were found
if database_files:
    # Use the first found database file as the database path
    database_path = database_files[0]
else:
    raise FileNotFoundError("No .db or .sqlite files found in the databases folder.")

DATABASE_DIR = os.path.dirname(database_path)
DATABASE_URI = f'sqlite:///{database_path}'
print(DATABASE_URI)

# Create a directory named 'cache' in the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(base_dir, './cache')
os.makedirs(cache_dir, exist_ok=True)
CACHE_DIR = cache_dir

# Get the Hugging Face API key from environment variables
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
