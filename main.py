from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from contextlib import asynccontextmanager
from database import engine, Base, get_db
from schemas import BlogCreate, BlogResponse
from crud import create_blog, get_blog, update_blog, delete_blog

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

app = FastAPI(lifespan=lifespan)

@app.post("/blogs/", response_model=BlogResponse)
async def create_blog_api(blog: BlogCreate, db: AsyncSession = Depends(get_db)):
    return await create_blog(db, blog)

@app.get("/blogs/{blog_id}", response_model=BlogResponse)
async def read_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await get_blog(db, blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.put("/blogs/{blog_id}", response_model=BlogResponse)
async def update_blog_api(blog_id: int, blog: BlogCreate, db: AsyncSession = Depends(get_db)):
    updated_blog = await update_blog(db, blog_id, blog)
    if updated_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return updated_blog

@app.delete("/blogs/{blog_id}")
async def delete_blog_api(blog_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_blog(db, blog_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}
