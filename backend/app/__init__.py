from fastapi import FastAPI

app = FastAPI(
    title="AI Engineering Change Assistant API",
    version="0.1.0",
)

@app.get("/")
def root():
    return {
        "message": "AI Engineering Change Assistant backend is running"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }