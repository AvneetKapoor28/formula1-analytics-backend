from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import race_analysis

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://formula1-amber.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "FastAPI backend is running!"}
# Include routers
app.include_router(race_analysis.router)
