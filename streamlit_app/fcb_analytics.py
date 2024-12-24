import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Any
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common.database import session, logger
from common.data_provider import (
    get_player_metrics,
    get_matches_from_events,
)


class MatchAnalyzer:
    def __init__(self):
        self.metrics = [
            "Number of Passes",
            "Successful Passes",
            "Number of Key Passes",
            "Number of Long Passes",
            "Number of Shots on Goal",
            "Number of Aerial Duels",
            "Aerial Duel Success",
        ]

        self.reference_maxes = {
            "Number of Passes": 8000,
            "Successful Passes": 7000,
            "Number of Key Passes": 100,
            "Number of Long Passes": 200,
            "Number of Shots on Goal": 1500,
            "Number of Aerial Duels": 250,
            "Aerial Duel Success": 200,
        }

    def scale_data(
        self, raw_data: Dict[str, List[float]]
    ) -> Dict[str, Dict[str, float]]:
        """Scale the raw metrics data for visualization"""
        scaled_data = {}
        for player, values in raw_data.items():
            scaled_values = {}
            for metric, value in zip(self.metrics, values):
                scaled_values[metric] = min(value / self.reference_maxes[metric], 1)
            scaled_data[player] = scaled_values
        return scaled_data

    def plot_radar(
        self,
        raw_data: Dict[str, List[float]],
        players_to_plot: List[str] = None,
        title: str = "Player Comparison",
    ) -> plt.Figure:
        """Generate radar plot for selected players"""
        scaled_data = self.scale_data(raw_data)

        if players_to_plot is None:
            players_to_plot = list(raw_data.keys())

        angles = np.linspace(0, 2 * np.pi, len(self.metrics), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection="polar"))

        colors = plt.cm.rainbow(np.linspace(0, 1, len(players_to_plot)))
        for player, color in zip(players_to_plot, colors):
            values = [scaled_data[player][metric] for metric in self.metrics]
            values = np.concatenate((values, [values[0]]))

            ax.plot(angles, values, "o-", linewidth=2, label=player, color=color)
            ax.fill(angles, values, alpha=0.25, color=color)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.metrics, size=8)
        plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))
        plt.title(title, size=20, y=1.05)
        ax.grid(True)

        return fig


def create_match_dashboard(session, logger):
    """Main function to create the Streamlit dashboard"""

    # Page configuration
    st.set_page_config(
        page_title="Player Performance Radar Chart", page_icon="⚽", layout="wide"
    )

    # Title and description
    st.title("🏆 Bundesliga Player Performance Analytics")
    st.markdown("### Visualize and Compare Player Metrics")

    # Initialize components
    analyzer = MatchAnalyzer()

    try:
        # Sidebar for player selection
        st.sidebar.header("Selection Area")
        # Get matches data
        matches = get_matches_from_events(session, logger)
        match_names = [match["name"] for match in matches]

        # Match selection
        selected_match_name = st.sidebar.selectbox(
            "Select a Match:", options=match_names
        )
        selected_match_index = match_names.index(selected_match_name)
        selected_match_id = matches[selected_match_index]["match_id"]

        # Display match details
        st.subheader("Match Information")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown(
                f"**Match Date:** {matches[selected_match_index]['match_date']}"
            )
        with col2:
            st.markdown(f"**Winner:** {matches[selected_match_index]['winner']}")
        with col3:
            st.markdown(
                f"**Match Length:** {matches[selected_match_index]['match_length_min']} minutes"
            )

        # Team selection
        teams = matches[selected_match_index]["teams"]
        match_names = [team["team_name"] for team in teams]
        selected_team_name = st.sidebar.selectbox("Select a Team:", options=match_names)
        selected_team_id = next(
            team["team_id"] for team in teams if team["team_name"] == selected_team_name
        )

        # Get player metrics
        metrics_data = get_player_metrics(session, selected_team_id, selected_match_id)

        if metrics_data:
            # Player selection
            available_players = list(metrics_data.keys())
            selected_players = st.sidebar.multiselect(
                "Select Players to Compare:",
                available_players,
                default=(
                    available_players[:2]
                    if len(available_players) > 1
                    else available_players[:1]
                ),
            )

            if selected_players:
                # Create and display radar chart

                selected_data = {
                    player: metrics_data[player] for player in selected_players
                }
                fig = analyzer.plot_radar(
                    selected_data,
                    selected_players,
                    f"{selected_team_name} - Player Comparison",
                )

                st.subheader("Player Performance Comparison")
                st.markdown(
                    "The radar chart below shows the comparison of player metrics for the selected players."
                )
                col1, col2, col3 = st.columns([2, 3, 2])
                with col2:
                    fig_container = st.container()
                    with fig_container:
                        st.pyplot(fig, use_container_width=True)

                st.subheader("Raw Metrics")
                metrics_df = pd.DataFrame(
                    {player: metrics_data[player] for player in selected_players},
                    index=analyzer.metrics,
                ).T
                st.dataframe(metrics_df)

        else:
            st.warning("No player metrics data available for this selection.")

    except Exception as e:
        logger.error(f"Error in dashboard: {str(e)}")
        st.error("An error occurred while loading the dashboard. Please try again.")


if __name__ == "__main__":
    create_match_dashboard(session, logger)
