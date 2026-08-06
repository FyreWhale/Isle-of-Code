import streamlit as st
from utils.game_logic import get_initial_game_state

# Sets page configuration for the survival management dashboard.
st.set_page_config(
    page_title="Isle of Code",
    page_icon="🏝️",
    layout="wide"
)

# Initializes session state variables for game persistence.
if "game_state" not in st.session_state:
    st.session_state.game_state = get_initial_game_state()

# Renders the main dashboard header and resource status bar.
def render_dashboard() -> None:
    """Renders the primary Streamlit interface including resource trackers and status metrics."""
    st.title("🏝️ Isle of Code")
    st.caption("A text-based survival management RPG.")

    state = st.session_state.game_state
    
    # Display Day and Resource Trackers in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Current Day", value=state["day"])
    with col2:
        st.metric(label="Food Stock", value=state["resources"]["food"])
    with col3:
        st.metric(label="Wood Stock", value=state["resources"]["wood"])

    st.divider()

if __name__ == "__main__":
    render_dashboard()