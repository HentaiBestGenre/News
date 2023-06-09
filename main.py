import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Routers import gamespot_api

origins = ["*"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def index():
    return {"status_code": 200, "message": "hello world"}


app.include_router(gamespot_api, prefix="/parse/gamespot")


if __name__ == "__main__":
    uvicorn.run(app)
