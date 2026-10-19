from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Engineering Change Assistant API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/api/parts")
def get_parts():
    return [
        {
            "part_number": "BRK-001",
            "name": "ECU Bracket",
            "revision": "A",
            "lifecycle_state": "Released",
        },
        {
            "part_number": "BRK-002",
            "name": "New ECU Bracket",
            "revision": "A",
            "lifecycle_state": "Prototype",
        },
        {
            "part_number": "ECU-100",
            "name": "Main ECU",
            "revision": "C",
            "lifecycle_state": "Released",
        },
        {
            "part_number": "HAR-201",
            "name": "Wiring Harness",
            "revision": "B",
            "lifecycle_state": "Released",
        },
    ]