import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the directory of the current file
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the SQLite database file
database_path = os.path.join(base_dir, '../databases/movie.sqlite')

# Define the DATABASE_URI using the relative path
DATABASE_URI = f'sqlite:///{database_path}'
print(DATABASE_URI)

# Create a directory named 'cache' in the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(base_dir, '../cache')
os.makedirs(cache_dir, exist_ok=True)
CACHE_DIR = cache_dir

# Get the Hugging Face API key from environment variables
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
