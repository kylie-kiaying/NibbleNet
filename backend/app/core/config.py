from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI()

    # CORS setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Adjust when deploying
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
