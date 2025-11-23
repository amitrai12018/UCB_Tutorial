"""
UCB Algorithm Implementation
Contains core UCB logic and simulation functions
"""

import numpy as np
from typing import List, Tuple, Optional


class UCBAgent:
    """Upper Confidence Bound agent for multi-armed bandit problems"""
    
    def __init__(self, n_arms: int, c: float = 2.0):
        """
        Initialize UCB agent
        
        Args:
            n_arms: Number of arms (actions)
            c: Exploration parameter
        """
        self.n_arms = n_arms
        self.c = c
        self.Q = np.zeros(n_arms)  # Estimated values
        self.N = np.zeros(n_arms)  # Selection counts
        self.t = 0  # Time step
        
    def select_action(self) -> int:
        """
        Select action using UCB strategy
        
        Returns:
            Selected action index
        """
        self.t += 1
        
        # Compute UCB values
        ucb_values = np.zeros(self.n_arms)
        for a in range(self.n_arms):
            if self.N[a] == 0:
                ucb_values[a] = float('inf')
            else:
                exploration_bonus = self.c * np.sqrt(np.log(self.t) / self.N[a])
                ucb_values[a] = self.Q[a] + exploration_bonus
        
        return int(np.argmax(ucb_values))
    
    def update(self, action: int, reward: float) -> None:
        """
        Update estimates after observing reward
        
        Args:
            action: Action taken
            reward: Observed reward
        """
        self.N[action] += 1
        self.Q[action] += (reward - self.Q[action]) / self.N[action]
    
    def get_ucb_values(self) -> np.ndarray:
        """Get current UCB values for all actions"""
        ucb_values = np.zeros(self.n_arms)
        for a in range(self.n_arms):
            if self.N[a] == 0:
                ucb_values[a] = float('inf')
            else:
                ucb_values[a] = self.Q[a] + self.c * np.sqrt(np.log(self.t) / self.N[a])
        return ucb_values
    
    def reset(self) -> None:
        """Reset agent state"""
        self.Q = np.zeros(self.n_arms)
        self.N = np.zeros(self.n_arms)
        self.t = 0


def simulate_ucb_episode(
    true_ctrs: List[float],
    n_rounds: int,
    c: float,
    return_trajectory: bool = False
) -> Tuple[float, Optional[np.ndarray]]:
    """
    Simulate a complete UCB episode
    
    Args:
        true_ctrs: True click-through rates for each ad
        n_rounds: Number of rounds to simulate
        c: Exploration parameter
        return_trajectory: If True, return CTR at each round
        
    Returns:
        Average CTR and optionally trajectory over time
    """
    agent = UCBAgent(len(true_ctrs), c)
    
    total_clicks = 0
    trajectory = [] if return_trajectory else None
    
    for t in range(n_rounds):
        action = agent.select_action()
        reward = int(np.random.rand() < true_ctrs[action])
        agent.update(action, reward)
        
        total_clicks += reward
        
        if return_trajectory:
            trajectory.append(total_clicks / (t + 1))
    
    avg_ctr = total_clicks / n_rounds
    
    if return_trajectory:
        return avg_ctr, np.array(trajectory)
    else:
        return avg_ctr, None


def run_multiple_simulations(
    true_ctrs: List[float],
    n_rounds: int,
    c_values: List[float],
    n_runs: int = 30
) -> dict:
    """
    Run multiple simulations for different c values
    
    Args:
        true_ctrs: True CTRs for each ad
        n_rounds: Rounds per simulation
        c_values: List of c values to test
        n_runs: Number of runs per c value
        
    Returns:
        Dictionary mapping c values to lists of average CTRs
    """
    results = {c: [] for c in c_values}
    
    for c in c_values:
        for _ in range(n_runs):
            avg_ctr, _ = simulate_ucb_episode(true_ctrs, n_rounds, c)
            results[c].append(avg_ctr)
    
    return results


def get_optimal_ctr(true_ctrs: List[float]) -> float:
    """Get the optimal CTR (always choosing best ad)"""
    return max(true_ctrs)
