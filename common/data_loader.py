from fcb_data_providers.providers import StatsPerformProvider

from common.database import DATA_DIR, DATABASE_URL


def process_and_store_data() -> None:
    """
    Process and store data in the database
    return: None
    """
    provider = StatsPerformProvider(data_path=DATA_DIR, database_url=DATABASE_URL)
    provider.process_data()
