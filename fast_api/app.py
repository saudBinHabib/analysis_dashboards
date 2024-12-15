import os
from datetime import date

# Add project root to Python path
import sys

import pandas as pd
from fastapi import FastAPI

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from typing import Dict, List, Tuple

from common.data_loader import process_and_store_data
from common.data_provider import (
    get_matches_from_events,
    get_all_aerials_duels_by_players_count,
    get_all_passes_by_players_count,
    get_key_passes_by_players_count,
    get_long_passes_by_players_count,
    get_player_metrics,
    get_shots_on_goals_by_players_count,
    get_successfull_aerials_duels_by_players_count,
    get_successfull_passes_by_players_count,
)
from common.database import session, logger

app = FastAPI()


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


@app.get("/all_matches")
async def get_all_matches() -> List[Dict]:
    """
    Get all matches data

    :return: List[Dict[str, str | int | date]]

    """
    matches = get_matches_from_events(session, logger)
    logger.info("Matches data retrieved successfully")
    logger.info(matches)
    return matches


@app.get("/metrics")
async def get_metrics(team_id: str, match_id: str) -> Dict[str, List[int]]:
    """
    Get all metrics data

    Sequence of those metrics:
    "Number of Passes",
    "Successful Passes",
    "Number of Key Passes",
    "Number of Long Passes",
    "Number of Shots on Goal",
    "Number of Aerial Duels",
    "Aerial Duel Success",

    :param team_id: str
    :param match_id: str
    :return: Dict[str, List[int]]


    """
    return get_player_metrics(session, team_id, match_id)


@app.get("/all_passes")
async def get_all_passes(team_id: str, match_id: str) -> List[Dict[str, int]]:
    """
    Get all passes data

    :param team_id: str
    :param match_id: str
    :return: Dict[str, List[int]]

    """
    all_passes = get_all_passes_by_players_count(session, team_id, match_id)
    return [{pas[0]: pas[1]} for pas in all_passes]


@app.get("/successfull_passes")
async def get_successfull_passes(team_id: str, match_id: str) -> List[Dict[str, int]]:
    """
    Get successfull passes data

    :param team_id: str
    :param match_id: str
    :return: Dict[str, List[int]]

    """
    successfull_passes = get_successfull_passes_by_players_count(
        session, team_id, match_id
    )
    return [{pas[0]: pas[1]} for pas in successfull_passes]


@app.get("/shots_on_goals")
async def get_shots_on_goals(team_id: str, match_id: str) -> List[Dict[str, int]]:
    """
    Get shots on goals data

    :param team_id: str
    :param match_id: str
    :return: Dict[str, List[int]]

    """
    shots_on_goals = get_shots_on_goals_by_players_count(session, team_id, match_id)
    return [{pas[0]: pas[1]} for pas in shots_on_goals]


@app.get("/key_passes")
async def get_key_passes(team_id: str, match_id: str) -> List[Dict[str, int]]:
    """
    Get key passes data

    :param team_id: str
    :param match_id: str
    :return: Dict[str, List[int]]

    """
    key_passes = get_key_passes_by_players_count(session, team_id, match_id)
    return [{pas[0]: pas[1]} for pas in key_passes]


@app.get("/successfull_aerials_duels")
async def get_successfull_aerials_duels(
    team_id: str, match_id: str
) -> List[Dict[str, int]]:
    """
    Get successfull aerials duels data

    :param team_id: str
    :param match_id: str
    :return: Dict[str, List[int]]

    """
    successfull_aerials_duels = get_successfull_aerials_duels_by_players_count(
        session, team_id, match_id
    )
    return [{pas[0]: pas[1]} for pas in successfull_aerials_duels]


@app.get("/all_aerials_duels")
async def get_all_aerials_duels(team_id: str, match_id: str) -> List[Dict[str, int]]:
    """
    Get all aerials duels data

    :param team_id: str
    :param match_id: str
    :return: Dict[str, List[int]]

    """
    all_aerials_duels = get_all_aerials_duels_by_players_count(
        session, team_id, match_id
    )
    return [{pas[0]: pas[1]} for pas in all_aerials_duels]


@app.get("/long_passes")
async def get_long_passes(team_id: str, match_id: str) -> List[Dict[str, int]]:
    """
    Get long passes data

    :param team_id: str
    :param match_id: str
    :return: Dict[str, List[int]]

    """
    long_passes = get_long_passes_by_players_count(session, team_id, match_id)
    return [{pas[0]: pas[1]} for pas in long_passes]
