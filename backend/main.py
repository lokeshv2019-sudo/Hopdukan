from fastapi import FastAPI

app = FastAPI(title="HopDukan API", description="भारत का रेट कार्ड")

@app.get("/")
def read_root():
    return {"message": "Welcome to HopDukan API"}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running perfectly"}
