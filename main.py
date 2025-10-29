from uuid import uuid4
from sqlalchemy import UUID, String, create_engine, text
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, mapped_column

from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    "postgresql://postgres:postgres@localhost/postgres", echo=True)


# with engine.connect() as connection:
#     result = connection.execute(text("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));"))
#     result = connection.execute(text("INSERT INTO test_table (name) VALUES (:name)"), [{"name": "Alice"}, {"name": "Bob"}])
#     connection.commit()
#     # for row in result:
#     #     print(row)

# with engine.begin() as connection:
#     result = connection.execute(text("INSERT INTO test_table (name) VALUES (:name)"), [{"name": "Charlie"}, {"name": "Diana"}])


# with engine.connect() as connection:
#     result = connection.execute(text("SELECT * FROM test_table;"))
#     for row in result:
#         print(f"id: {row.id}, name: {row.name}")

# with Session(engine) as session:
#     result = session.execute(text("SELECT * FROM test_table;"))
#     for row in result:
#         print(f"id: {row.id}, name: {row.name}")

Session = sessionmaker(bind=engine)

# with Session() as session, session.begin():
#     result = session.execute(text("INSERT INTO test_table (name) VALUES (:name)"), [{"name": "Alice"}, {"name": "Bob"}])


# with Session() as session:
#     result = session.execute(text("SELECT * FROM test_table;"))
#     for row in result:
#         print(f"id: {row.id}, name: {row.name}")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    name = mapped_column(String)


Base.metadata.create_all(engine)

# with Session() as session:
#     session.add(User(id=uuid4(), name="Alice"))
#     session.commit()

with Session() as session:
    users = session.query(User).all()
    for user in users:
        print(f"id: {user.id}, name: {user.name}")