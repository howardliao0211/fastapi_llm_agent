import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TITLE: str = "GenAI API"
    DESCRIPTION: str = "Blog API Powered by Generative AI"
    VERSION: str = "1.0.0"
    
    # Postgre Database
    DATABASE_URL: str = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    
    # VLLM (for running LLM inference)
    VLLM_BASE_URL: str = os.getenv("VLLM_BASE_URL")
    VLLM_MODEL: str = os.getenv("VLLM_MODEL")

    # JWT authorization
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"

settings = Settings()
