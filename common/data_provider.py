from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np
from fcb_data_providers.database_models import Event, Player, Qualifier
from sqlalchemy import func
from sqlalchemy.orm import Session


def get_all_passes_by_players_count(session: Session, team_id: str) -> List[Tuple]:
    """
    Retrieving all passes by players count

    :param session: Session: Session manager to get the data from database of your choice.
    :param team_id: str: Team ID
    return: List[tuple]: List of tuples, which contain player name and KPI value count.
    """
    result = (
        session.query(Player.match_name, func.count(Event.player_id))
        .join(Qualifier, Event.e_id == Qualifier.event_id)
        .join(Player, Event.player_id == Player.id)
        .filter(
            Event.type_id == 1,
            Event.team_id == team_id,
            ~Qualifier.qualifier_id.in_([2, 107, 123]),
        )
        .group_by(Player.match_name)
        .order_by(Player.match_name)
        .all()
    )

    return result


def get_successfull_passes_by_players_count(
    session: Session, team_id: str
) -> List[Tuple]:
    """
    Retrieving all passes by players count

    :param session: Session: Session manager to get the data from database of your choice.
    :param team_id: str: Team ID
    return: List[tuple]: List of tuples, which contain player name and KPI value count.
    """
    result = (
        session.query(Player.match_name, func.count(Event.player_id))
        .join(Qualifier, Event.e_id == Qualifier.event_id)
        .join(Player, Event.player_id == Player.id)
        .filter(
            Event.type_id == 1,
            Event.outcome == "1",
            Event.team_id == team_id,
            ~Qualifier.qualifier_id.in_([2, 107, 123]),
        )
        .group_by(Player.match_name)
        .order_by(Player.match_name)
        .all()
    )

    return result


def get_key_passes_by_players_count(session: Session, team_id: str) -> List[Tuple]:
    """
    Retrieving all passes by players count

    :param session: Session: Session manager to get the data from database of your choice.
    :param team_id: str: Team ID
    return: List[tuple]: List of tuples, which contain player name and KPI value count.
    """
    result = (
        session.query(Player.match_name, func.count(Event.player_id))
        .join(Qualifier, Event.e_id == Qualifier.event_id)
        .join(Player, Event.player_id == Player.id)
        .filter(
            Event.type_id.in_([13, 14, 15, 60]),  # Multiple type_id values
            Event.team_id == team_id,
            Qualifier.qualifier_id.in_([29, 55]),  # Specific qualifier_id values
        )
        .group_by(Player.match_name)
        .order_by(Player.match_name)
        .all()
    )

    return result


def get_long_passes_by_players_count(session: Session, team_id: str) -> List[Tuple]:
    """
    Retrieving all passes by players count

    :param session: Session: Session manager to get the data from database of your choice.
    :param team_id: str: Team ID
    return: List[tuple]: List of tuples, which contain player name and KPI value count.
    """
    result = (
        session.query(Player.match_name, func.count(Event.player_id))
        .join(Qualifier, Event.e_id == Qualifier.event_id)
        .join(Player, Event.player_id == Player.id)
        .filter(
            Event.type_id == 1,  # Specific event type
            Event.team_id == team_id,  # Specific team ID
            Qualifier.qualifier_id == 1,  # Specific qualifier ID
            ~Qualifier.qualifier_id.in_(
                [2, 107, 123]
            ),  # Exclusion of certain qualifier IDs
        )
        .group_by(Player.match_name)
        .order_by(Player.match_name)
        .all()
    )

    return result


def get_shots_on_goals_by_players_count(session: Session, team_id: str) -> List[Tuple]:
    """
    Retrieving all passes by players count

    :param session: Session: Session manager to get the data from database of your choice.
    :param team_id: str: Team ID
    return: List[tuple]: List of tuples, which contain player name and KPI value count.
    """
    result = (
        session.query(Player.match_name, func.count(Event.player_id))
        .join(Qualifier, Event.e_id == Qualifier.event_id)
        .join(Player, Event.player_id == Player.id)
        .filter(
            Event.type_id.in_([13, 14, 15, 16]),  # Multiple event types
            Event.team_id == team_id,  # Specific team ID
        )
        .group_by(Player.match_name)
        .order_by(Player.match_name)
        .all()
    )

    return result


def get_all_aerials_duels_by_players_count(
    session: Session, team_id: str
) -> List[Tuple]:
    """
    Retrieving all passes by players count

    :param session: Session: Session manager to get the data from database of your choice.
    :param team_id: str: Team ID
    return: List[tuple]: List of tuples, which contain player name and KPI value count.
    """
    result = (
        session.query(Player.match_name, func.count(Event.player_id))
        .join(Qualifier, Event.e_id == Qualifier.event_id)
        .join(Player, Event.player_id == Player.id)
        .filter(
            Event.type_id == 4,  # Specific event type
            Event.team_id == team_id,  # Specific team ID
        )
        .group_by(Player.match_name)
        .order_by(Player.match_name)
        .all()
    )

    return result


def get_successfull_aerials_duels_by_players_count(
    session: Session, team_id: str
) -> List[Tuple]:
    """
    Retrieving all passes by players count

    :param session: Session: Session manager to get the data from database of your choice.
    :param team_id: str: Team ID
    return: List[tuple]: List of tuples, which contain player name and KPI value count.
    """
    result = (
        session.query(Player.match_name, func.count(Event.player_id))
        .join(Qualifier, Event.e_id == Qualifier.event_id)
        .join(Player, Event.player_id == Player.id)
        .filter(
            Event.type_id == 4,  # Specific event type
            Event.team_id == team_id,  # Specific team ID
            Event.outcome == "1",  # Specific outcome condition
        )
        .group_by(Player.match_name)
        .order_by(Player.match_name)
        .all()
    )

    return result


def z_score_normalize_with_scaling(
    data: List[Tuple[str, int]], scale_min: float = 0, scale_max: float = 100
) -> List[Tuple[str, float]]:
    """
    Perform Z-score normalization with optional scaling

    Args:
        data (List[Tuple[str, int]]): List of tuples with (name, value)
        scale_min (float): Minimum of scaling range
        scale_max (float): Maximum of scaling range

    Returns:
        List[Tuple[str, float]]: List of tuples with scaled normalized values
    """
    # Extract values for normalization
    values = [item[1] for item in data]

    # Calculate Z-score
    mean = np.mean(values)
    std = np.std(values)

    # Handle edge case of zero standard deviation
    if std == 0:
        normalized_values = [scale_min] * len(values)
    else:
        # Z-score calculation
        z_scores = [(x - mean) / std for x in values]

        # Optional scaling to desired range
        normalized_values = [
            scale_min
            + (zscore - min(z_scores))
            * (scale_max - scale_min)
            / (max(z_scores) - min(z_scores))
            for zscore in z_scores
        ]

    # Reconstruct the list of tuples with normalized values
    return [
        (name, norm_value) for (name, _), norm_value in zip(data, normalized_values)
    ]


def combine_player_stats(
    *lists: List[Tuple[str, int]], default_value: int = 0
) -> Dict[str, List[int]]:
    """
    Combine multiple lists of player statistics, ensuring consistent player names
    and filling missing values with a default.

    Args:
        *lists: Variable number of lists containing (player_name, value) tuples
        default_value: Value to use when a player is missing from a list

    Returns:
        Dictionary with player names as keys and lists of values from each input list
    """
    # Collect all unique player names
    all_players = set()
    for lst in lists:
        all_players.update(player for player, _ in lst)

    # Create a result dictionary with default structure
    result = {player: [default_value] * len(lists) for player in all_players}

    # Populate the dictionary
    for idx, lst in enumerate(lists):
        for player, value in lst:
            result[player][idx] = value

    return result


def get_all_metrics(session: Session, team_id: str) -> Dict[str, List[int]]:
    """
    Retrieve and combine various player statistics for a given team.

    Args:
        session: SQLAlchemy session
        team_id: Team ID
    """
    # Retrieve statistics
    all_passes = get_all_passes_by_players_count(session, team_id)
    successful_passes = get_successfull_passes_by_players_count(session, team_id)
    key_passes = get_key_passes_by_players_count(session, team_id)
    long_passes = get_long_passes_by_players_count(session, team_id)
    shots_on_goal = get_shots_on_goals_by_players_count(session, team_id)
    all_aerial_duels = get_all_aerials_duels_by_players_count(session, team_id)
    successful_aerial_duels = get_successfull_aerials_duels_by_players_count(
        session, team_id
    )

    return (
        all_passes,
        successful_passes,
        key_passes,
        long_passes,
        shots_on_goal,
        all_aerial_duels,
        successful_aerial_duels,
    )


def get_player_metrics(session: Session, team_id: str) -> Dict[str, List[int]]:
    """
    Retrieve and combine various player statistics for a given team.

    Args:
        session: SQLAlchemy session
        team_id: Team ID
    """
    # Retrieve metrics
    (
        all_passes,
        successful_passes,
        key_passes,
        long_passes,
        shots_on_goal,
        all_aerial_duels,
        successful_aerial_duels,
    ) = get_all_metrics(session, team_id)

    # Combine statistics
    player_metrics = combine_player_stats(
        all_passes,
        successful_passes,
        key_passes,
        long_passes,
        shots_on_goal,
        all_aerial_duels,
        successful_aerial_duels,
    )

    return player_metrics


def get_normalized_player_metrics(
    session: Session, team_id: str
) -> Dict[str, List[int]]:
    """
    Retrieve and normalize various player statistics for a given team.

    Args:
        session: SQLAlchemy session
        team_id: Team ID
    """
    # Retrieve player metrics
    (
        all_passes,
        successful_passes,
        key_passes,
        long_passes,
        shots_on_goal,
        all_aerial_duels,
        successful_aerial_duels,
    ) = get_all_metrics(session, team_id)

    # Normalize metrics
    all_passes = z_score_normalize_with_scaling(all_passes)
    successful_passes = z_score_normalize_with_scaling(successful_passes)
    key_passes = z_score_normalize_with_scaling(key_passes)
    long_passes = z_score_normalize_with_scaling(long_passes)
    shots_on_goal = z_score_normalize_with_scaling(shots_on_goal)
    all_aerial_duels = z_score_normalize_with_scaling(all_aerial_duels)
    successful_aerial_duels = z_score_normalize_with_scaling(successful_aerial_duels)

    # create a dictionary with normalized player metrics
    players_data = combine_player_stats(
        all_passes,
        successful_passes,
        key_passes,
        long_passes,
        shots_on_goal,
        all_aerial_duels,
        successful_aerial_duels,
    )

    return players_data
