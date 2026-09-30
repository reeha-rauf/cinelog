from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.movies.routes import router as movies_router
from app.logs.routes import router as logs_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(logs_router)


@app.get("/")
def read_root():
    return {"status" : "Cinelog is live"}



