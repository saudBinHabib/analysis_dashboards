import os

from dotenv import load_dotenv
from fcb_data_providers.database import Database

load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:$postgres@postgres:5434/fcb_analytics"
)
DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "data"))
db = Database(DATABASE_URL)
session = db.get_session()
