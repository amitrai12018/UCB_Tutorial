"""
UI Components
Reusable UI elements for the UCB Tutorial app
"""

import streamlit as st
import numpy as np
from typing import List, Optional
from config import APP_CONFIG, DEFAULT_PARAMS


def setup_page():
    """Configure page settings"""
    st.set_page_config(
        page_title=APP_CONFIG["title"],
        page_icon="🎯",
        layout=APP_CONFIG["layout"],
        initial_sidebar_state=APP_CONFIG["initial_sidebar_state"]
    )


def render_sidebar() -> dict:
    """
    Render sidebar with global settings
    
    Returns:
        Dictionary with configuration values
    """
    st.sidebar.header("⚙️ Global Settings")
    
    # True CTRs input
    true_ctrs_input = st.sidebar.text_input(
        "True CTRs (comma-separated)",
        ",".join(map(str, DEFAULT_PARAMS["true_ctrs"])),
        help="Click-through rates for each ad. These represent the true probabilities."
    )
    
    try:
        true_ctrs = [float(x.strip()) for x in true_ctrs_input.split(",") if x.strip()]
        if len(true_ctrs) < 2:
            st.sidebar.error("⚠️ Provide at least two CTRs")
            true_ctrs = DEFAULT_PARAMS["true_ctrs"]
    except ValueError:
        st.sidebar.error("⚠️ Invalid format. Use comma-separated numbers (e.g., 0.05,0.10,0.20)")
        true_ctrs = DEFAULT_PARAMS["true_ctrs"]
    
    # Default rounds
    n_rounds = st.sidebar.number_input(
        "Default rounds per simulation",
        min_value=DEFAULT_PARAMS["min_rounds"],
        max_value=DEFAULT_PARAMS["max_rounds"],
        value=DEFAULT_PARAMS["n_rounds"],
        step=50,
        help="Number of user visits (impressions) in each simulation"
    )
    
    st.sidebar.markdown("---")
    
    # Info section
    with st.sidebar.expander("ℹ️ About This App"):
        st.markdown("""
        This interactive tutorial helps you understand the **Upper Confidence Bound (UCB)** algorithm 
        for solving multi-armed bandit problems.
        
        **Navigation:**
        - 📚 Learn the basics
        - 👁️ Watch step-by-step
        - 📈 Compare parameters
        - 🔬 Statistical analysis
        - 🎮 Test yourself
        """)
    
    return {
        "true_ctrs": true_ctrs,
        "n_rounds": n_rounds
    }


def render_ad_boxes(
    n_ads: int,
    selected_ad: Optional[int] = None,
    reward: Optional[int] = None,
    labels: Optional[List[str]] = None
) -> None:
    """
    Render ad display boxes
    
    Args:
        n_ads: Number of ads
        selected_ad: Index of selected ad (None if none selected)
        reward: Reward received (1 for click, 0 for no click)
        labels: Optional custom labels for ads
    """
    cols = st.columns(n_ads)
    
    for i, col in enumerate(cols):
        with col:
            label = labels[i] if labels else f"Ad {i+1}"
            
            if selected_ad is not None and i == selected_ad:
                # Selected ad
                reward_text = "✅ Click!" if reward == 1 else "❌ No Click"
                col.markdown(
                    f"""
                    <div class='ad-box-selected'>
                        <h3>🟩 {label}</h3>
                        <p><strong>Displayed</strong></p>
                        <p>{reward_text}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Idle ad
                col.markdown(
                    f"""
                    <div class='ad-box-idle'>
                        <h3>⬜ {label}</h3>
                        <p>Idle</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


def render_stats_panel(
    round_num: int,
    total_rounds: int,
    avg_ctr: float,
    Q: np.ndarray,
    N: np.ndarray,
    ucb_values: Optional[np.ndarray] = None,
    chosen_ad: Optional[int] = None,
    true_ctrs: Optional[List[float]] = None
) -> None:
    """
    Render statistics panel
    
    Args:
        round_num: Current round number
        total_rounds: Total number of rounds
        avg_ctr: Average CTR so far
        Q: Estimated CTRs
        N: Selection counts
        ucb_values: UCB values (optional)
        chosen_ad: Currently chosen ad (optional)
        true_ctrs: True CTRs (optional, for debugging)
    """
    st.markdown(
        f"""
        <div class='stats-panel'>
        <h3>📊 Statistics</h3>
        <p><strong>Round:</strong> {round_num}/{total_rounds}</p>
        <p><strong>Average CTR:</strong> {avg_ctr:.4f}</p>
        """,
        unsafe_allow_html=True
    )
    
    if chosen_ad is not None:
        st.markdown(f"<p><strong>Selected:</strong> Ad {chosen_ad + 1}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"**Estimated CTRs (Q):** {np.round(Q, 4).tolist()}")
    st.markdown(f"**Selections (N):** {N.astype(int).tolist()}")
    
    if ucb_values is not None:
        # Handle infinity values for display
        ucb_display = []
        for val in ucb_values:
            if np.isinf(val):
                ucb_display.append("∞")
            else:
                ucb_display.append(f"{val:.4f}")
        st.markdown(f"**UCB Values:** {ucb_display}")
    
    if true_ctrs is not None:
        st.markdown(f"**True CTRs:** {[f'{ctr:.3f}' for ctr in true_ctrs]}")
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_formula_explanation():
    """Render UCB formula with explanation"""
    st.markdown("""
    ### UCB Formula
    
    The UCB algorithm selects the action (ad) that maximizes:
    """)
    
    st.latex(r"UCB(a) = Q(a) + c \sqrt{\frac{\ln t}{N(a)}}")
    
    st.markdown("""
    **Where:**
    - `Q(a)` = Estimated value (CTR) of action a → **Exploitation term**
    - `c` = Exploration parameter (higher = more exploration)
    - `t` = Current time step (round number)
    - `N(a)` = Number of times action a has been selected → **Uncertainty term**
    
    **Intuition:**
    - The first term `Q(a)` favors actions with high estimated rewards
    - The second term favors actions that haven't been tried much (high uncertainty)
    - As `N(a)` increases, uncertainty decreases, and we rely more on `Q(a)`
    """)


def show_success_message(message: str):
    """Display success message with styling"""
    st.markdown(
        f"<div class='success-box'>✅ {message}</div>",
        unsafe_allow_html=True
    )


def show_warning_message(message: str):
    """Display warning message with styling"""
    st.markdown(
        f"<div class='warning-box'>⚠️ {message}</div>",
        unsafe_allow_html=True
    )


def render_game_scores(user_score: int, ucb_score: int, total_rounds: int):
    """Render game scores in a visual way"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class='game-score user-score'>
                <div>👤 Your Score</div>
                <div style='font-size: 3rem;'>{user_score}</div>
                <div>CTR: {user_score/max(total_rounds, 1):.3f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class='game-score ucb-score'>
                <div>🤖 UCB Score</div>
                <div style='font-size: 3rem;'>{ucb_score}</div>
                <div>CTR: {ucb_score/max(total_rounds, 1):.3f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
