
from database import engine

try:
    with engine.connect() as connection:
        print("PostgreSQL connection successful!")
        print("Database:", engine.url.database)

except Exception as e:
    print("Database connection failed!")
    print("Error:", e)
