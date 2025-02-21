from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import race_analysis

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(race_analysis.router)
