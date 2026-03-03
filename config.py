import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is missing in .env")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing in .env")
