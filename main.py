from fastapi import FastAPI
from typing import Dict

app: FastAPI = FastAPI(title="GenAI Blog API", description="API Powered by GenAI", version="1.0.0")

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Hello World"}
