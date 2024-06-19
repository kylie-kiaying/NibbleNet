from fastapi import FastAPI
from .routers.auth import router as auth_router
from .routers.user import router as user_router
from .routers.food_listing import router as food_listing_router

app = FastAPI()

app.include_router(auth_router, prefix="/users", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(food_listing_router, prefix="/listings", tags=["listings"])

@app.get("/")
async def root():
  return {"message": "Hello World"}
