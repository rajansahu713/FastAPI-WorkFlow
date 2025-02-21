from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
import dotenv

dotenv.load_dotenv()

host = os.environ.get('DBHOST')
port = os.environ.get('DBPORT')
dbname = os.environ.get('DBNAME')
user = os.environ.get('DBUSER')
password = os.environ.get('DBPASSWORD')

# DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"

DATABASE_URL = f"postgresql+asyncpg://postgres:sahu@localhost:5432/mydb"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Base class for models
class Base(DeclarativeBase):
    pass

# Dependency for session management
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Add this function to override the database dependency in tests
async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session
