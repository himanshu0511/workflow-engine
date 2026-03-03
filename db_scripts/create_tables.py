from multiprocessing import process

from sqlmodel import SQLModel, create_engine
# IMPORTANT: You MUST import your model classes here
# even if you don't use them in the code below.
from models import DAG, DagAudit, Node, NodeDependencies, NodeKeyValue, NodeKeyValueGroup, NodeRequiredParameters, Worker

# Connection String: mysql+mysqlconnector://user:password@host/dbname
DB_USER = process.env.DB_USER
DB_NAME = process.env.DB_NAME
DB_PASS = process.env.DB_PASS

MYSQL_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}"

# echo=True is helpful for debugging; it prints the SQL being executed
engine = create_engine(MYSQL_URL, echo=True)


def sync_schema():
    print("🚀 Initializing database schema...")

    # This single line detects ALL imported models (DAG, Task, etc.)
    # and creates their tables in the correct order (handling foreign keys)
    SQLModel.metadata.create_all(engine)

    print("✅ All tables created successfully.")


if __name__ == "__main__":
    sync_schema()
