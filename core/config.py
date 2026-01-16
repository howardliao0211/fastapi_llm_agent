import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TITLE: str = "GenAI API"
    DESCRIPTION: str = "Blog API Powered by Generative AI"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

settings = Settings()
