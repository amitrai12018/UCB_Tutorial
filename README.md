# 🎯 UCB Tutorial - Interactive Learning Platform

A professional, modular Streamlit application for understanding the Upper Confidence Bound (UCB) algorithm through interactive visualizations, statistical analysis, and gamification.

## 📋 Overview

This application provides a comprehensive tutorial on the UCB algorithm for solving multi-armed bandit problems. It's designed for students, researchers, and practitioners who want to understand how UCB balances exploration and exploitation.

## ✨ Features

### 1. 📚 UCB Primer
- Theoretical foundation of the UCB algorithm
- Interactive examples of incremental learning
- Clear explanations of key concepts
- Mathematical formulations with intuitive interpretations

### 2. 👁️ Visual Step-by-Step Simulation
- Watch UCB make decisions round by round
- See real-time updates of estimates and UCB values
- Understand exploration vs exploitation in action
- Control simulation speed and parameters

### 3. 📈 Parameter Comparison
- Compare different exploration parameters (c values)
- Visualize learning curves across multiple runs
- Identify optimal parameter settings
- Interactive charts showing individual runs and mean trends

### 4. 🔬 Statistical Analysis
- Rigorous statistical testing (ANOVA, t-tests)
- Bonferroni correction for multiple comparisons
- Box plots and summary statistics
- Scientifically determine the best parameter

### 5. 🎮 Human vs UCB Challenge
- **Interactive game mode** where you compete against the algorithm
- **Hidden true CTRs** - you must learn through trial and error
- Track your performance vs the algorithm
- Reveals optimal strategies at the end

## 🏗️ Project Structure

```
ucb_tutorial_app/
├── app.py              # Main application entry point
├── config.py           # Configuration and styling
├── ucb_algorithm.py    # Core UCB implementation
├── ui_components.py    # Reusable UI components
├── tabs.py             # Tab-specific rendering logic
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project:**
```bash
cd UCB_TUTORIAL
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Navigation

1. **Configure global settings** in the sidebar (true CTRs, default rounds)
2. **Navigate through tabs** to explore different features
3. **Interact with simulations** using buttons and controls
4. **Adjust parameters** to see how they affect performance

### Tips for Best Experience

- Start with the **UCB Primer** to understand the basics
- Use the **Visual Simulation** to build intuition
- Run **Parameter Comparisons** to see performance differences
- Use **Statistical Analysis** for rigorous evaluation
- Challenge yourself in the **Game Mode**!

## 🎮 Game Mode Features

The Human vs UCB Challenge provides a unique learning experience:

- **Random CTRs**: Each game generates new random CTRs (hidden from you)
- **Fair competition**: Both you and UCB start with no knowledge
- **Learning opportunity**: Track your estimated CTRs as you play
- **Post-game analysis**: See the true CTRs and compare strategies

**Strategy Tips:**
- Balance exploration (trying all ads) with exploitation (choosing the best)
- Keep mental track of click rates
- Don't give up on ads too quickly - small sample sizes can be misleading!

## 🔧 Configuration

### Customizing Parameters

Edit `config.py` to customize:
- Default CTRs
- Default number of rounds
- Color schemes
- UI styling

### Modifying the Algorithm

The UCB implementation in `ucb_algorithm.py` can be extended:
- Add different bandit algorithms (ε-greedy, Thompson Sampling)
- Implement contextual bandits
- Add custom reward functions

## 📊 Understanding the Results

### Key Metrics

- **Q (Estimated CTR)**: Agent's current belief about an ad's performance
- **N (Selection Count)**: How many times an ad has been shown
- **UCB Value**: Combines Q with exploration bonus
- **Average CTR**: Cumulative performance metric

### Interpreting Charts

- **Learning Curves**: Steeper = faster learning
- **Box Plots**: Show distribution and variance
- **Statistical Tests**: p < 0.05 indicates significant differences

## 🤝 Contributing

This is an educational project. Suggestions for improvements:
- Add more bandit algorithms
- Implement non-stationary bandits
- Add more interactive visualizations
- Create additional game modes

## 📚 Educational Use

Perfect for:
- Reinforcement Learning courses
- Decision Theory classes
- Online optimization tutorials
- Self-study and experimentation

## 🐛 Troubleshooting

### Common Issues

**Issue**: Charts not rendering
- **Solution**: Ensure altair is properly installed: `pip install --upgrade altair`

**Issue**: Slow performance with many simulations
- **Solution**: Reduce the number of runs or rounds in settings

**Issue**: Game CTRs seem unfair
- **Solution**: CTRs are randomly generated - try multiple games!

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

Built with:
- Streamlit for the web framework
- NumPy for numerical computations
- Pandas for data manipulation
- Altair for visualizations
- SciPy for statistical tests

## 📧 Support

For questions or issues, please refer to the in-app help text or tooltips.

---

**Happy Learning! 🎓**
