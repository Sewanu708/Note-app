from fastapi import FastAPI
from .routes import users
from .routes import notes
app = FastAPI()

app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Note API 🚀"}