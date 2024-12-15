import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import streamlit as st
from sqlalchemy.orm.session import Session

from common.data_provider import (
    get_normalized_player_metrics,
    get_player_metrics,
    get_matches_from_events,
)
from common.database import session, logger

# Define the performance metrics consistently
METRICS = [
    "Number of Passes",
    "Successful Passes",
    "Number of Key Passes",
    "Number of Long Passes",
    "Number of Shots on Goal",
    "Number of Aerial Duels",
    "Aerial Duel Success",
]


def create_radar_chart(player_metrics, metrics=METRICS):
    """
    Create an interactive radar chart for a specific player

    Args:
        player_metrics (list): Performance metrics for the player
        metrics (list): Metric names

    Returns:
        Plotly figure object
    """
    fig = go.Figure(
        data=go.Scatterpolar(
            r=player_metrics,
            theta=metrics,
            fill="toself",
            line_color="rgb(51, 153, 255)",  # Vibrant blue
            fillcolor="rgba(51, 153, 255, 0.4)",  # Transparent blue
        )
    )

    # Enhanced layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],  # Fixed range for consistent comparison
                ticksuffix="%",
                tickmode="linear",
                tick0=0,
                dtick=20,
            )
        ),
        title={
            "text": f"Performance Metrics Analysis",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=20),
        },
        width=700,
        height=700,
    )

    return fig


def main(
    session: Session,
):
    """
    Main application function to display player performance analytics
    :param normalized_data: Dict[str, List[int]]: Player metrics
    :param metrics_data: Dict[str, List[int]]: Player metrics
    """

    # Page configuration
    st.set_page_config(
        page_title="Player Performance Radar Chart", page_icon="⚽", layout="wide"
    )

    # Title and description
    st.title("🏆 Bundesliga Player Performance Analytics")
    st.markdown("### Visualize and Compare Player Metrics")

    matches = get_matches_from_events(session, logger)
    match_names = [match["name"] for match in matches]
    selected_match_name = st.selectbox("Select a Match:", options=match_names)
    selected_match_index = match_names.index(selected_match_name)
    selected_match_id = matches[selected_match_index]["match_id"]

    # Get match details
    # match_details = get_match_details_from_view_by_match_id(
    #     session, selected_match_id, logger
    # )
    winner = matches[selected_match_index]["winner"]
    match_date = matches[selected_match_index]["match_date"]
    match_length_min = matches[selected_match_index]["match_length_min"]
    col1, col2, col3 = st.columns([1, 2, 3])
    with col1:
        st.markdown(f"**Match Date:** {match_date}")
    with col2:
        st.markdown(f"**Winner:** {winner}")
    with col3:
        st.markdown(f"**Match Length:** {match_length_min} minutes")

    teams = matches[selected_match_index]["teams"]

    match_names = [team["team_name"] for team in teams]
    selected_team_name = st.selectbox("Select a Team:", options=match_names)
    selected_team_id = next(
        team["team_id"] for team in teams if team["team_name"] == selected_team_name
    )

    # # # Data type selection
    # data_type = st.radio(
    #     "Select Data Type:",
    #     options=["Z Score Normalized Metrics", "Normal Metrics"],
    # )

    # # Load the appropriate data based on user selection
    # if data_type == "Z Score Normalized Metrics":
    #     normalized_data = get_normalized_player_metrics(
    #         session, selected_team_id, selected_match_id
    #     )
    #     player_df = pd.DataFrame(normalized_data, index=METRICS).T
    # else:
    metrics_data = get_player_metrics(session, selected_team_id, selected_match_id)
    player_df = pd.DataFrame(metrics_data, index=METRICS).T

    if len(player_df) > 0:
        # Create columns for layout
        col4, col5 = st.columns([4, 5])

        # Player selection dropdown
        with col4:
            selected_player = st.selectbox(
                "Select a Player", options=player_df.index.tolist()
            )

        # Get selected player's metrics
        player_metrics = player_df.loc[selected_player].tolist()

        # Radar Chart
        with col5:
            radar_chart = create_radar_chart(player_metrics)
            st.plotly_chart(radar_chart, use_container_width=True)

        # Detailed Metrics Table
        st.subheader(f"{selected_player} - Detailed Performance Metrics")
        metrics_df = pd.DataFrame({"Metric": METRICS, "Value": player_metrics})
        metrics_df["Value"] = metrics_df["Value"].apply(lambda x: f"{x}")
        st.dataframe(metrics_df, use_container_width=True)

        # Optional: Comparative Insights
        st.markdown("### Comparative Insights")
        comparison_df = player_df.copy()
        comparison_df["Avg Performance"] = comparison_df.mean(axis=1)
        st.dataframe(
            comparison_df.sort_values("Avg Performance", ascending=False),
            use_container_width=True,
        )


if __name__ == "__main__":

    main(session)
