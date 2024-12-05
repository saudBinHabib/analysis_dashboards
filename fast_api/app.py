import os
# Add project root to Python path
import sys

import pandas as pd
from fastapi import FastAPI

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from typing import Dict, List, Tuple

from common.data_loader import process_and_store_data
from common.data_provider import (
    get_all_aerials_duels_by_players_count, get_all_passes_by_players_count,
    get_key_passes_by_players_count, get_long_passes_by_players_count,
    get_player_metrics, get_shots_on_goals_by_players_count,
    get_successfull_aerials_duels_by_players_count,
    get_successfull_passes_by_players_count)
from common.database import session

app = FastAPI()

team_id = "apoawtpvac4zqlancmvw4nk4o"


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FCB Analytics API!"}


@app.get("/process_data")
async def process_data():
    """
    Process and store data in the database
    return: None
    """
    process_and_store_data()
    return {"message": "Data processed and stored in the database!"}


@app.get("/metrics")
async def get_processed_data():
    """
    Get all passes data
    """
    return get_player_metrics(session, team_id)


@app.get("/all_passes")
async def get_all_passes():
    """
    Get all passes data
    """
    all_passes = get_all_passes_by_players_count(session, team_id)
    return [{pas[0]: pas[1]} for pas in all_passes]


@app.get("/successfull_passes")
async def get_successfull_passes():
    """
    Get successfull passes data
    """
    successfull_passes = get_successfull_passes_by_players_count(session, team_id)
    return [{pas[0]: pas[1]} for pas in successfull_passes]


@app.get("/shots_on_goals")
async def get_shots_on_goals():
    """
    Get shots on goals data
    """
    shots_on_goals = get_shots_on_goals_by_players_count(session, team_id)
    return [{pas[0]: pas[1]} for pas in shots_on_goals]


@app.get("/key_passes")
async def get_key_passes():
    """
    Get key passes data
    """
    key_passes = get_key_passes_by_players_count(session, team_id)
    return [{pas[0]: pas[1]} for pas in key_passes]


@app.get("/successfull_aerials_duels")
async def get_successfull_aerials_duels():
    """
    Get successfull aerials duels data
    """
    successfull_aerials_duels = get_successfull_aerials_duels_by_players_count(
        session, team_id
    )
    return [{pas[0]: pas[1]} for pas in successfull_aerials_duels]


@app.get("/all_aerials_duels")
async def get_all_aerials_duels():
    """
    Get all aerials duels data
    """
    all_aerials_duels = get_all_aerials_duels_by_players_count(session, team_id)
    return [{pas[0]: pas[1]} for pas in all_aerials_duels]


@app.get("/long_passes")
async def get_long_passes():
    """
    Get long passes data
    """
    long_passes = get_long_passes_by_players_count(session, team_id)
    return [{pas[0]: pas[1]} for pas in long_passes]
