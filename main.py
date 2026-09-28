from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.movies.routes import router as movies_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(movies_router)

@app.get("/")
def read_root():
    return {"status" : "Cinelog is live"}



