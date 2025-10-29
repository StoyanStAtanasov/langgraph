from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
from uuid import uuid4
import uuid
from fastapi import Depends, FastAPI, UploadFile
from sqlalchemy import ForeignKey, LargeBinary, LargeBinary, select
from sqlalchemy.orm import Session, DeclarativeBase, mapped_column, Mapped, relationship


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    files: Mapped[list["File"]] = relationship(
        "File", back_populates="user", cascade="all, delete-orphan")


class File(Base):
    __tablename__ = 'files'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    filename: Mapped[str]
    file: Mapped[bytes] = mapped_column(LargeBinary)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship("User", back_populates="files")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    # Shutdown code can go here

app = FastAPI(lifespan=lifespan)


@app.get("/users")
async def get_users(session: SessionDependency):
    statement = select(User)
    users = await session.execute(statement)
    return [{"id": str(user.id), "name": user.name} for user in users.scalars().all()]


@app.post("/users")
def create_user(name: str):
    with Session() as session, session.begin():
        new_user = User(name=name)
        session.add(new_user)
        return {"id": str(new_user.id), "name": new_user.name}


@app.patch("/users/{user_id}")
def update_user(user_id: uuid.UUID, name: str):
    with Session() as session, session.begin():
        user = session.get(User, user_id)
        if user:
            user.name = name
            return {"id": str(user.id), "name": user.name}
        return {"error": "User not found"}, 404


@app.delete("/users/{user_id}")
def delete_user(user_id: uuid.UUID):
    with Session() as session, session.begin():
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            return {"message": "User deleted"}
        return {"error": "User not found"}, 404

# create files for a user


@app.post("/users/{user_id}/files")
async def create_user_file(user_id: uuid.UUID, session: SessionDependency, file: UploadFile):
    async with session.begin():
        user = await session.get(User, user_id)
        if user:
            content = await file.read()
            new_file = File(filename=file.filename, file=content, user=user)
            session.add(new_file)
            return {"id": str(new_file.id), "filename": new_file.filename}
        return {"error": "User not found"}, 404


@app.get("/users/{user_id}/files")
def get_user_files(user_id: uuid.UUID):
    with Session() as session:
        user = session.get(User, user_id)
        if user:
            return [{"id": str(file.id), "filename": file.filename} for file in user.files]
        return {"error": "User not found"}, 404


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
