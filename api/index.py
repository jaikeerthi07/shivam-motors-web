from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from database import init_db
import bikes
import valuations

app = FastAPI(title="Shivam Motors API")

# Initialize database tables
@app.on_event("startup")
def startup_event():
    init_db()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin login endpoint (Directly in main as it's small)
@app.post("/api/admin/login")
async def admin_login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    
    if username == "admin" and password == "shivadmin123":
        return {"token": "shivadmin_secret_token_2026"}
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid credentials. Access denied.")

# Include routers
app.include_router(bikes.router, prefix="/api")
app.include_router(valuations.router, prefix="/api")

# Static files are handled by Vercel's CDN (configured in vercel.json)
# sm_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sm"))
# app.mount("/", StaticFiles(directory=sm_dir, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("index:app", host="0.0.0.0", port=3000, reload=True)
