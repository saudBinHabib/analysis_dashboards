import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Any
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
            "Number of Passes": 10000,
            "Successful Passes": 9000,
            "Number of Key Passes": 100,
            "Number of Long Passes": 200,
            "Number of Shots on Goal": 1500,
            "Number of Aerial Duels": 250,
            "Aerial Duel Success": 200,
        }

    def scale_data(self, raw_data: Dict[str, List[float]]) -> Dict[str, List[float]]:
        """Scale the raw metrics data for visualization"""
        scaled_data = {}
        for player, values in raw_data.items():
            scaled_values = [
                min(value / self.reference_maxes[metric], 1)
                for metric, value in zip(self.metrics, values)
            ]
            scaled_data[player] = scaled_values
        return scaled_data

    def create_radar_chart(
        self,
        raw_data: Dict[str, List[float]],
        players_to_plot: List[str] = None,
        title: str = "Player Comparison",
    ) -> go.Figure:
        """Create an interactive radar chart using Plotly"""
        if players_to_plot is None:
            players_to_plot = list(raw_data.keys())

        scaled_data = self.scale_data(raw_data)

        fig = go.Figure()

        for player in players_to_plot:
            fig.add_trace(
                go.Scatterpolar(
                    r=scaled_data[player]
                    + [scaled_data[player][0]],  # Complete the circle
                    theta=self.metrics + [self.metrics[0]],  # Complete the circle
                    name=player,
                    fill="toself",
                    opacity=0.6,
                )
            )

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title=dict(text=title, x=0.5, y=0.95),
            height=600,
        )

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
        st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

        # Cache player metrics data
        @st.cache_data
        def get_cached_player_metrics(team_id, match_id):
            return get_player_metrics(session, team_id, match_id)

        metrics_data = get_cached_player_metrics(selected_team_id, selected_match_id)

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
                # Create tabs for different visualizations
                tab1, tab2 = st.tabs(["Radar Chart", "Raw Data"])

                with tab1:
                    # Create and display radar chart using Plotly
                    selected_data = {
                        player: metrics_data[player] for player in selected_players
                    }
                    fig = analyzer.create_radar_chart(
                        selected_data,
                        selected_players,
                        f"{selected_team_name} - Player Comparison",
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with tab2:
                    # Display raw metrics with formatted DataFrame
                    metrics_df = pd.DataFrame(
                        {player: metrics_data[player] for player in selected_players},
                        index=analyzer.metrics,
                    ).T

                    # Format the DataFrame for better readability
                    st.dataframe(
                        metrics_df.style.format("{:.1f}").background_gradient(
                            cmap="YlOrRd", axis=None
                        ),
                        use_container_width=True,
                    )

        else:
            st.warning("No player metrics data available for this selection.")

    except Exception as e:
        logger.error(f"Error in dashboard: {str(e)}")
        st.error("An error occurred while loading the dashboard. Please try again.")


if __name__ == "__main__":
    create_match_dashboard(session, logger)
