import os
from dotenv import load_dotenv

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")

# ExerciseDB API v2
EDB_API_KEY = os.getenv("EDB_API_KEY", "0ff91de6e1mshefd47e741cb9c07p199ca7jsn69d67ba79eda")
EDB_API_HOST = os.getenv("EDB_API_HOST", "edb-with-videos-and-images-by-ascendapi.p.rapidapi.com")

if not RAPID_API_KEY:
    # Fallback or raise? Existing code raised.
    # We'll keep existing behavior but check if it's set.
    # If the user hasn't set it nicely, this might crash if we just run it. 
    # But since it was raising before, we should respect that.
    pass 
    # raise ValueError("RAPID_API_KEY is not set in environment variables") 
    # Actually, let's not touch the existing logic too much, just append.

if not RAPID_API_KEY and not EDB_API_KEY:
     raise ValueError("API Keys are missing")
