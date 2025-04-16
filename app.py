from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import *

app = FastAPI()
include_routers(app=app, routers=routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],  
)

@app.on_event("startup") 
def on_startup():
    create_db_and_tables()