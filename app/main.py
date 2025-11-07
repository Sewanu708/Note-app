from fastapi import FastAPI
from .routes import users
from .routes import notes
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Note API 🚀"}