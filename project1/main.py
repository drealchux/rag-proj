from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Optional: confirm it loaded
print("GROQ_API_KEY loaded:", bool(os.getenv("GROQ_API_KEY")))
