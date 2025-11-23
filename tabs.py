"""
Tab Implementations
Contains the rendering logic for each tutorial tab
"""

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from scipy import stats
import time
import itertools

from ucb_algorithm import UCBAgent, simulate_ucb_episode, run_multiple_simulations, get_optimal_ctr
from ui_components import (
    render_ad_boxes, render_stats_panel, render_formula_explanation,
    show_success_message, show_warning_message, render_game_scores
)


def render_primer_tab():
    """Render the UCB primer/introduction tab"""
    st.header("📚 Upper Confidence Bound (UCB) Algorithm Primer")
    
    st.markdown("""
    In **Reinforcement Learning**, an agent interacts with the world and learns consequences 
    of actions through **trial and error**.
    
    ### The Multi-Armed Bandit Problem
    
    One classical problem to formalize **decision-making under uncertainty** is the 
    **Multi-Armed Bandit Problem**:
    - Imagine a slot machine with `k` levers (arms). Each lever gives rewards from an unknown distribution.
    - The agent must choose which lever to pull at each time step to **maximize cumulative reward**.
    
    **Real-world example:** Online advertising
    - An advertiser has 3 different ads (actions)
    - Each user visit is a round where one ad is displayed
    - The user may or may not click the ad (reward)
    - The probability of a click is the **true CTR**, which is unknown
    - **Goal:** Identify the best ad to maximize clicks while still learning about all ads
    """)
    
    # Collapsible sections for better organization
    with st.expander("🎯 Action Values and Estimates", expanded=True):
        st.markdown("""
        - **Action-value (true):** $q^*(a)$ — the expected reward for taking action $a$
        - **Estimated value:** $Q_t(a)$ — the agent's estimate of $q^*(a)$ after $t$ rounds
        
        The estimate is updated incrementally using the **sample-average method**:
        """)
        st.latex(r"Q_{t+1}(a) = Q_t(a) + \frac{1}{N_t(a)} (R_t - Q_t(a))")
        st.markdown("""
        where $N_t(a)$ is the number of times action $a$ has been selected so far, 
        and $R_t$ is the observed reward at round $t$.
        """)
    
    with st.expander("⚖️ Exploration vs Exploitation", expanded=True):
        st.markdown("""
        **Greedy Action (Exploitation):** Choose the action with the highest current estimated value $Q_t(a)$
        
        **Exploration:** Occasionally select other actions to improve knowledge about their rewards
        
        **Why balance matters:**
        - Always exploiting may miss the best action
        - Always exploring wastes potential reward
        - UCB provides a principled way to balance both
        """)
    
    with st.expander("🧮 Upper Confidence Bound Formula", expanded=True):
        render_formula_explanation()
    
    # Interactive example
    st.markdown("---")
    st.subheader("💡 Interactive Example: Incremental Updates")
    st.markdown("See how estimated CTR (Q) converges to the true value through incremental updates:")
    
    true_ctr_example = st.slider("True CTR of the ad", 0.0, 1.0, 0.20, 0.05)
    n_impressions = st.slider("Number of impressions to simulate", 5, 50, 10)
    
    if st.button("🎲 Simulate Random Clicks"):
        # Generate random clicks based on true CTR
        clicks = (np.random.rand(n_impressions) < true_ctr_example).astype(int)
        
        Q = 0.0
        table_data = []
        for i, r in enumerate(clicks, start=1):
            N = i
            Q = Q + (r - Q) / N
            table_data.append({
                "Impression": i,
                "Click?": "✅" if r == 1 else "❌",
                "Estimated CTR (Q)": round(Q, 4)
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)
        
        final_q = df.iloc[-1]["Estimated CTR (Q)"]
        error = abs(final_q - true_ctr_example)
        
        st.markdown(f"""
        **Results:**
        - True CTR: {true_ctr_example:.3f}
        - Estimated CTR: {final_q:.3f}
        - Estimation Error: {error:.3f}
        
        💡 With more impressions, the estimate converges to the true value!
        """)


def render_visual_tab(config: dict):
    """Render the visual step-by-step simulation tab"""
    st.header("👁️ Visual Step-by-Step Simulation")
    st.markdown("Watch how UCB explores and exploits to find the best ad!")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_right:
        st.subheader("⚙️ Settings")
        n_rounds = st.number_input(
            "Rounds (impressions)",
            min_value=10,
            max_value=1000,
            value=min(50, config["n_rounds"]),
            help="Number of rounds to simulate"
        )
        c = st.number_input(
            "Exploration parameter (c)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.1,
            format="%.2f",
            help="Higher values encourage more exploration"
        )
        
        st.markdown("**True CTRs:**")
        for i, ctr in enumerate(config["true_ctrs"]):
            st.markdown(f"- Ad {i+1}: {ctr:.3f}")
    
    # Initialize session state for interactive simulation
    if "visual_state" not in st.session_state:
        st.session_state.visual_state = {
            "round": 0,
            "agent": UCBAgent(len(config["true_ctrs"]), c),
            "clicks": [],
            "history": []
        }
    
    state = st.session_state.visual_state
    
    # Control buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("▶️ Next Round"):
            if state["round"] < n_rounds:
                state["round"] += 1
                action = state["agent"].select_action()
                reward = int(np.random.rand() < config["true_ctrs"][action])
                state["agent"].update(action, reward)
                state["clicks"].append(reward)
                state["history"].append({
                    "action": action,
                    "reward": reward,
                    "Q": state["agent"].Q.copy(),
                    "N": state["agent"].N.copy(),
                    "ucb": state["agent"].get_ucb_values().copy()
                })
    
    with col_btn2:
        if st.button("⏩ Auto-play Remaining"):
            with st.spinner("Running simulation..."):
                while state["round"] < n_rounds:
                    state["round"] += 1
                    action = state["agent"].select_action()
                    reward = int(np.random.rand() < config["true_ctrs"][action])
                    state["agent"].update(action, reward)
                    state["clicks"].append(reward)
                    state["history"].append({
                        "action": action,
                        "reward": reward,
                        "Q": state["agent"].Q.copy(),
                        "N": state["agent"].N.copy(),
                        "ucb": state["agent"].get_ucb_values().copy()
                    })
                show_success_message("Simulation complete!")
    
    with col_btn3:
        if st.button("🔄 Reset"):
            st.session_state.visual_state = {
                "round": 0,
                "agent": UCBAgent(len(config["true_ctrs"]), c),
                "clicks": [],
                "history": []
            }
            st.rerun()
    
    # Display current state
    st.subheader(f"Round {state['round']}/{n_rounds}")
    
    if state["round"] > 0:
        last = state["history"][-1]
        render_ad_boxes(
            len(config["true_ctrs"]),
            selected_ad=last["action"],
            reward=last["reward"]
        )
        
        st.markdown("---")
        
        # Show detailed explanation
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("### 📊 Current Estimates")
            for i in range(len(config["true_ctrs"])):
                selected = " ← **Selected**" if i == last["action"] else ""
                st.markdown(f"""
                **Ad {i+1}**{selected}
                - Estimated CTR (Q): {last['Q'][i]:.4f}
                - Times shown (N): {int(last['N'][i])}
                - UCB value: {last['ucb'][i]:.4f if not np.isinf(last['ucb'][i]) else '∞'}
                """)
        
        with col_b:
            st.markdown("### 🎯 Why this ad?")
            action = last["action"]
            
            # Determine if exploration or exploitation
            max_q_idx = np.argmax(last["Q"])
            if action == max_q_idx:
                reason = "**Exploitation**"
                explanation = "This ad has the highest estimated CTR"
            else:
                reason = "**Exploration**"
                explanation = "This ad has high uncertainty (large UCB bonus)"
            
            st.markdown(f"""
            {reason}
            
            {explanation}
            
            **Average CTR so far:** {sum(state['clicks']) / state['round']:.4f}
            """)
    else:
        render_ad_boxes(len(config["true_ctrs"]))
        st.info("👆 Click 'Next Round' to start the simulation!")
    
    # Progress indicator
    if state["round"] > 0:
        progress = state["round"] / n_rounds
        st.progress(progress)


def render_comparison_tab(config: dict):
    """Render the parameter comparison tab"""
    st.header("📈 Compare Different Exploration Parameters")
    st.markdown("See how different `c` values affect learning speed and performance")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_right:
        st.subheader("⚙️ Settings")
        n_rounds_comp = st.number_input(
            "Rounds for comparison",
            min_value=50,
            max_value=5000,
            value=min(500, config["n_rounds"]),
            step=50
        )
        c_list_input = st.text_input(
            "c values (comma-separated)",
            "0.1,0.5,1.0,2.0,4.0",
            help="List of exploration parameters to compare"
        )
        n_runs_comp = st.number_input(
            "Runs per c (for averaging)",
            min_value=1,
            max_value=50,
            value=10
        )
        
        if st.button("📈 Run Comparison"):
            try:
                c_list = sorted([float(x.strip()) for x in c_list_input.split(",") if x.strip()])
                
                with st.spinner("Running simulations..."):
                    progress_bar = st.progress(0.0)
                    
                    # Collect trajectories
                    all_data = []
                    for i, c in enumerate(c_list):
                        for run in range(n_runs_comp):
                            _, trajectory = simulate_ucb_episode(
                                config["true_ctrs"],
                                n_rounds_comp,
                                c,
                                return_trajectory=True
                            )
                            for t, ctr in enumerate(trajectory, 1):
                                all_data.append({
                                    "c": float(c),
                                    "run": run + 1,
                                    "round": t,
                                    "avg_ctr": float(ctr)
                                })
                        progress_bar.progress((i + 1) / len(c_list))
                    
                    st.session_state["comparison_data"] = pd.DataFrame(all_data)
                    show_success_message("Comparison complete!")
                    
            except ValueError:
                st.error("Invalid c values. Use comma-separated numbers (e.g., 0.5,1.0,2.0)")
    
    # Display results if available
    if "comparison_data" in st.session_state:
        df = st.session_state["comparison_data"]
        
        with col_left:
            st.subheader("📊 Learning Curves")
            
            # Create visualizations
            mean_data = df.groupby(["c", "round"], as_index=False)["avg_ctr"].mean()
            
            # Individual traces (faded)
            individual = alt.Chart(df.sample(min(len(df), 1000))).mark_line(
                opacity=0.1,
                strokeWidth=1
            ).encode(
                x=alt.X("round:Q", title="Round"),
                y=alt.Y("avg_ctr:Q", title="Average CTR"),
                detail="run:N",
                color=alt.Color("c:N", title="c value")
            )
            
            # Mean lines (bold)
            mean_lines = alt.Chart(mean_data).mark_line(
                strokeWidth=3
            ).encode(
                x="round:Q",
                y="avg_ctr:Q",
                color=alt.Color("c:N", title="c value"),
                tooltip=["c:N", "round:Q", "avg_ctr:Q"]
            )
            
            # Optimal CTR reference line
            optimal_ctr = get_optimal_ctr(config["true_ctrs"])
            optimal_line = alt.Chart(pd.DataFrame({"y": [optimal_ctr]})).mark_rule(
                strokeDash=[5, 5],
                color="red",
                strokeWidth=2
            ).encode(y="y:Q")
            
            chart = (individual + mean_lines + optimal_line).properties(
                height=400
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)
            
            st.markdown(f"""
            **Red dashed line:** Optimal CTR ({optimal_ctr:.3f}) - achieved by always choosing the best ad
            
            **Interpretation:**
            - Curves closer to the red line perform better
            - Steeper initial slopes indicate faster learning
            - Low c → More exploitation (faster convergence, but might get stuck)
            - High c → More exploration (slower convergence, but more thorough)
            """)
        
        # Final performance table
        st.subheader("🏆 Final Performance Summary")
        final_data = df[df["round"] == df["round"].max()].groupby("c")["avg_ctr"].agg(
            ["mean", "std", "min", "max"]
        ).round(4)
        final_data["optimal_gap"] = (optimal_ctr - final_data["mean"]).round(4)
        
        st.dataframe(
            final_data.sort_values("mean", ascending=False),
            use_container_width=True
        )


def render_statistical_tab(config: dict):
    """Render the statistical analysis tab"""
    st.header("🔬 Statistical Analysis: Finding the Best c")
    st.markdown("""
    Run rigorous statistical tests to determine which exploration parameter performs best.
    We'll use **ANOVA** to test if differences exist, then **pairwise t-tests** to identify them.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("⚙️ Settings")
        n_rounds_stat = st.number_input(
            "Rounds per simulation",
            min_value=50,
            max_value=5000,
            value=min(500, config["n_rounds"])
        )
        c_values_text = st.text_input(
            "c values to test",
            "0.1,0.5,1.0,2.0,4.0"
        )
        n_runs_stat = st.number_input(
            "Simulations per c",
            min_value=10,
            max_value=200,
            value=30,
            help="More simulations = more reliable results"
        )
        
        alpha = st.number_input(
            "Significance level (α)",
            min_value=0.01,
            max_value=0.10,
            value=0.05,
            step=0.01,
            help="Probability threshold for statistical significance"
        )
        
        if st.button("🔬 Run Statistical Analysis"):
            try:
                c_values = [float(x.strip()) for x in c_values_text.split(",") if x.strip()]
                
                with st.spinner("Running simulations and statistical tests..."):
                    results = run_multiple_simulations(
                        config["true_ctrs"],
                        n_rounds_stat,
                        c_values,
                        n_runs_stat
                    )
                    
                    st.session_state["stat_results"] = {
                        "results": results,
                        "c_values": c_values,
                        "alpha": alpha,
                        "n_rounds": n_rounds_stat
                    }
                    
                    show_success_message("Analysis complete!")
                    
            except ValueError:
                st.error("Invalid input. Check your c values.")
    
    # Display results
    if "stat_results" in st.session_state:
        data = st.session_state["stat_results"]
        results = data["results"]
        c_values = data["c_values"]
        alpha = data["alpha"]
        
        with col1:
            # Box plot
            st.subheader("📦 Distribution of CTRs")
            df_long = pd.DataFrame([
                {"c": c, "avg_ctr": ctr}
                for c, ctrs in results.items()
                for ctr in ctrs
            ])
            
            box_chart = alt.Chart(df_long).mark_boxplot(size=50).encode(
                x=alt.X("c:Q", title="c value"),
                y=alt.Y("avg_ctr:Q", title="Average CTR"),
                color=alt.Color("c:Q", legend=None)
            ).properties(height=350)
            
            st.altair_chart(box_chart, use_container_width=True)
        
        # Summary statistics
        st.subheader("📊 Summary Statistics")
        summary_data = []
        for c in c_values:
            ctrs = results[c]
            summary_data.append({
                "c": c,
                "mean": np.mean(ctrs),
                "std": np.std(ctrs),
                "min": np.min(ctrs),
                "max": np.max(ctrs),
                "n": len(ctrs)
            })
        summary_df = pd.DataFrame(summary_data).round(4)
        st.dataframe(summary_df, use_container_width=True)
        
        # ANOVA test
        st.subheader("🧪 ANOVA Test")
        groups = [results[c] for c in c_values]
        f_stat, p_val = stats.f_oneway(*groups)
        
        st.markdown(f"""
        **Null Hypothesis:** All c values have the same mean performance  
        **F-statistic:** {f_stat:.4f}  
        **p-value:** {p_val:.6f}  
        """)
        
        if p_val < alpha:
            show_success_message(
                f"Significant differences found! (p = {p_val:.6f} < {alpha})"
            )
            
            # Pairwise comparisons
            st.subheader("🔍 Pairwise T-Tests (Bonferroni corrected)")
            
            pairs = list(itertools.combinations(c_values, 2))
            n_comparisons = len(pairs)
            bonferroni_alpha = alpha / n_comparisons
            
            comparison_data = []
            for c1, c2 in pairs:
                t_stat, p = stats.ttest_ind(results[c1], results[c2])
                mean_diff = np.mean(results[c1]) - np.mean(results[c2])
                significant = p < bonferroni_alpha
                
                comparison_data.append({
                    "c1": c1,
                    "c2": c2,
                    "mean_diff": round(mean_diff, 5),
                    "t_statistic": round(t_stat, 4),
                    "p_value": f"{p:.6f}",
                    "significant": "✅" if significant else "❌"
                })
            
            comp_df = pd.DataFrame(comparison_data)
            st.dataframe(comp_df, use_container_width=True)
            
            st.markdown(f"*Bonferroni-corrected α = {bonferroni_alpha:.6f}*")
            
            # Find best c
            best_c = max(c_values, key=lambda c: np.mean(results[c]))
            best_mean = np.mean(results[best_c])
            
            st.markdown("---")
            st.markdown(
                f"""
                <div class='success-box'>
                <h3>🏆 Best Performing Parameter</h3>
                <p><strong>c = {best_c}</strong></p>
                <p>Mean CTR: {best_mean:.4f}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            show_warning_message(
                f"No significant differences found (p = {p_val:.6f} ≥ {alpha})"
            )


def render_game_tab():
    """Render the human vs UCB game tab"""
    st.header("🎮 Human vs UCB Challenge")
    
    st.markdown("""
    <div class='info-box'>
    <h3>🎯 Game Rules</h3>
    <ul>
    <li>There are 3 ads with <strong>hidden CTRs</strong></li>
    <li>Each round, you choose one ad to display</li>
    <li>UCB algorithm simultaneously makes its choice</li>
    <li>Both get a random click/no-click based on true CTRs</li>
    <li>Can you beat the algorithm? 🤔</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize game state
    if "game_state" not in st.session_state:
        # Generate random CTRs for the game (hidden from user!)
        true_ctrs_game = sorted(np.random.uniform(0.05, 0.30, 3).tolist())
        
        st.session_state.game_state = {
            "round": 0,
            "max_rounds": 30,
            "true_ctrs": true_ctrs_game,  # HIDDEN!
            "c_param": 2.0,
            "user_clicks": 0,
            "ucb_clicks": 0,
            "ucb_agent": UCBAgent(3, 2.0),
            "user_Q": np.zeros(3),
            "user_N": np.zeros(3),
            "history": [],
            "game_over": False
        }
    
    game = st.session_state.game_state
    
    # Settings sidebar for game
    with st.sidebar:
        st.markdown("### 🎮 Game Settings")
        if st.button("🎲 New Game"):
            # Reset with new random CTRs
            true_ctrs_game = sorted(np.random.uniform(0.05, 0.30, 3).tolist())
            st.session_state.game_state = {
                "round": 0,
                "max_rounds": 30,
                "true_ctrs": true_ctrs_game,
                "c_param": 2.0,
                "user_clicks": 0,
                "ucb_clicks": 0,
                "ucb_agent": UCBAgent(3, 2.0),
                "user_Q": np.zeros(3),
                "user_N": np.zeros(3),
                "history": [],
                "game_over": False
            }
            st.rerun()
    
    # Display scores
    render_game_scores(game["user_clicks"], game["ucb_clicks"], game["round"])
    
    st.markdown(f"### Round {game['round']}/{game['max_rounds']}")
    
    # Game controls
    if not game["game_over"] and game["round"] < game["max_rounds"]:
        st.markdown("#### 👤 Choose your ad:")
        
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        user_choice = None
        with col1:
            if st.button("🎯 Ad 1", use_container_width=True):
                user_choice = 0
        with col2:
            if st.button("🎯 Ad 2", use_container_width=True):
                user_choice = 1
        with col3:
            if st.button("🎯 Ad 3", use_container_width=True):
                user_choice = 2
        with col4:
            if st.button("🏁 End Game Early", type="secondary", use_container_width=True):
                game["game_over"] = True
                st.rerun()
        
        # Process round if user made a choice
        if user_choice is not None:
            game["round"] += 1
            
            # User's turn
            user_reward = int(np.random.rand() < game["true_ctrs"][user_choice])
            game["user_clicks"] += user_reward
            game["user_N"][user_choice] += 1
            game["user_Q"][user_choice] += (user_reward - game["user_Q"][user_choice]) / game["user_N"][user_choice]
            
            # UCB's turn
            ucb_choice = game["ucb_agent"].select_action()
            ucb_reward = int(np.random.rand() < game["true_ctrs"][ucb_choice])
            game["ucb_clicks"] += ucb_reward
            game["ucb_agent"].update(ucb_choice, ucb_reward)
            
            # Record history
            game["history"].append({
                "round": game["round"],
                "user_choice": user_choice,
                "user_reward": user_reward,
                "user_Q": game["user_Q"].copy(),
                "ucb_choice": ucb_choice,
                "ucb_reward": ucb_reward,
                "ucb_Q": game["ucb_agent"].Q.copy()
            })
            
            # Check if game over
            if game["round"] >= game["max_rounds"]:
                game["game_over"] = True
            
            st.rerun()
        
        # Show your estimates
        st.markdown("---")
        st.markdown("#### 📊 Your Estimated CTRs")
        col1, col2, col3 = st.columns(3)
        for i, col in enumerate([col1, col2, col3]):
            with col:
                if game["user_N"][i] > 0:
                    st.metric(
                        f"Ad {i+1}",
                        f"{game['user_Q'][i]:.3f}",
                        f"({int(game['user_N'][i])} tries)"
                    )
                else:
                    st.metric(f"Ad {i+1}", "???", "(not tried)")
    
    else:
        # Game over - show results
        game["game_over"] = True
        
        st.markdown("---")
        st.markdown("## 🏁 Game Over!")
        
        # Determine winner
        if game["user_clicks"] > game["ucb_clicks"]:
            st.balloons()
            st.markdown("""
            <div class='success-box'>
            <h2>🎉 YOU WIN!</h2>
            <p>Your intuition beat the UCB algorithm!</p>
            </div>
            """, unsafe_allow_html=True)
        elif game["user_clicks"] < game["ucb_clicks"]:
            st.markdown("""
            <div class='warning-box'>
            <h2>🤖 UCB WINS!</h2>
            <p>The algorithm outperformed human intuition!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='info-box'>
            <h2>🤝 IT'S A TIE!</h2>
            <p>You matched the algorithm's performance!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Reveal true CTRs
        st.markdown("### 🎭 The Truth Revealed")
        st.markdown("**True CTRs (hidden during the game):**")
        
        col1, col2, col3 = st.columns(3)
        for i, col in enumerate([col1, col2, col3]):
            with col:
                st.metric(
                    f"Ad {i+1}",
                    f"{game['true_ctrs'][i]:.3f}",
                    delta=f"You estimated: {game['user_Q'][i]:.3f}" if game['user_N'][i] > 0 else "Not tried"
                )
        
        # Show game history
        if game["history"]:
            st.markdown("### 📜 Game History")
            history_df = pd.DataFrame([
                {
                    "Round": h["round"],
                    "Your Choice": f"Ad {h['user_choice']+1}",
                    "Your Result": "✅" if h["user_reward"] else "❌",
                    "UCB Choice": f"Ad {h['ucb_choice']+1}",
                    "UCB Result": "✅" if h["ucb_reward"] else "❌",
                }
                for h in game["history"]
            ])
            st.dataframe(history_df, use_container_width=True)
        
        st.markdown("---")
        if st.button("🎲 Play Again", type="primary"):
            # Reset with new random CTRs
            true_ctrs_game = sorted(np.random.uniform(0.05, 0.30, 3).tolist())
            st.session_state.game_state = {
                "round": 0,
                "max_rounds": 30,
                "true_ctrs": true_ctrs_game,
                "c_param": 2.0,
                "user_clicks": 0,
                "ucb_clicks": 0,
                "ucb_agent": UCBAgent(3, 2.0),
                "user_Q": np.zeros(3),
                "user_N": np.zeros(3),
                "history": [],
                "game_over": False
            }
            st.rerun()
