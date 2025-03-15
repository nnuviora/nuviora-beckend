from sqlalchemy.sql import text
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db_setup import get_db

app = FastAPI()

@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    row = result.scalar() 
    return {"status": "Database connected", "result": row}