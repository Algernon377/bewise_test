import uvicorn
from DB.DB_manager import engine
from DB.models.base_model import Base
from fastapi import FastAPI
from quiz_app.routers import quiz_app_handlers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DataBaseApi")
# origins = [
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:5000",
#     "http://127.1.1.1:5000"]

app.include_router(quiz_app_handlers.router)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=80)











