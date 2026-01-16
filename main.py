from fastapi import FastAPI
from typing import Dict
from apis.main import api_router


app: FastAPI = FastAPI(title="GenAI Blog API", description="API Powered by GenAI", version="1.0.0")
app.include_router(api_router)

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Hello World"}
