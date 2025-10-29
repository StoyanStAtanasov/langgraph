from sqlalchemy import create_engine, text

from dotenv import load_dotenv

load_dotenv()

engine = create_engine("postgresql+asyncpg://postgres:postgres@localhost/postgres", echo=True)


with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    for row in result:
        print(row)

