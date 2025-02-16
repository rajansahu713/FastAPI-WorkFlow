from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model import Blog
from schemas import BlogCreate, BlogResponse

async def create_blog(db: AsyncSession, blog: BlogCreate) -> BlogResponse:
    new_blog = Blog(title=blog.title, content=blog.content)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return BlogResponse(id=new_blog.id, title=new_blog.title, content=new_blog.content)

async def get_blog(db: AsyncSession, blog_id: int):
    result = await db.execute(select(Blog).filter(Blog.id == blog_id))
    blog = result.scalars().first()
    return BlogResponse(id=blog.id, title=blog.title, content=blog.content) if blog else None

async def update_blog(db: AsyncSession, blog_id: int, blog: BlogCreate):
    result = await db.execute(select(Blog).filter(Blog.id == blog_id))
    existing_blog = result.scalars().first()
    if not existing_blog:
        return None
    existing_blog.title = blog.title
    existing_blog.content = blog.content
    await db.commit()
    return BlogResponse(id=existing_blog.id, title=existing_blog.title, content=existing_blog.content)

async def delete_blog(db: AsyncSession, blog_id: int):
    result = await db.execute(select(Blog).filter(Blog.id == blog_id))
    blog = result.scalars().first()
    if blog:
        await db.delete(blog)
        await db.commit()
        return True
    return False
