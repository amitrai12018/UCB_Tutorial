# 🚀 Quick Start Guide

Get up and running with the UCB Tutorial in 3 easy steps!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Run the Application

### On macOS/Linux:
```bash
./run.sh
```

### On Windows:
```bash
run.bat
```

### Manual Start:
```bash
streamlit run app.py
```

## Step 3: Open Your Browser

The app will automatically open at: **http://localhost:8501**

## 📖 First-Time User Guide

### Recommended Learning Path:

1. **📚 Start with Tab 1**: "UCB Primer"
   - Learn the theory and concepts
   - Understand the formula
   - Try the interactive example

2. **👁️ Move to Tab 2**: "Visual Simulation"
   - Watch UCB work step-by-step
   - See how exploration and exploitation balance
   - Experiment with different `c` values

3. **📈 Explore Tab 3**: "Compare Parameters"
   - Run multiple simulations
   - Compare different exploration parameters
   - See how `c` affects learning speed

4. **🔬 Dive into Tab 4**: "Statistical Analysis"
   - Run rigorous statistical tests
   - Find the best parameter scientifically
   - Understand statistical significance

5. **🎮 Challenge Yourself in Tab 5**: "Human vs UCB"
   - Test your intuition against the algorithm
   - Learn through competition
   - See if you can beat UCB!

## 🎯 Quick Tips

- **Adjust the sidebar**: Change true CTRs and default rounds
- **Start small**: Use fewer rounds (~50-100) for faster experimentation
- **Increase for accuracy**: Use more runs (30+) for statistical analysis
- **Game mode**: CTRs are hidden - this is intentional for realistic learning!

## ⚙️ Configuration

### Change True CTRs
In the sidebar, modify the comma-separated values:
```
Example: 0.05,0.10,0.20
```

### Adjust Exploration
- Low `c` (0.1-0.5): More exploitation, faster convergence
- Medium `c` (1.0-2.0): Balanced approach (recommended)
- High `c` (3.0-10.0): More exploration, thorough search

## 🆘 Need Help?

- Look for the ℹ️ icons and tooltips in the app
- Check the full README.md for detailed documentation
- Each tab has explanatory text to guide you

## 🎓 Learning Objectives

By the end of this tutorial, you should understand:
- ✅ What the multi-armed bandit problem is
- ✅ How UCB balances exploration and exploitation
- ✅ The effect of the exploration parameter `c`
- ✅ How to evaluate bandit algorithms statistically
- ✅ When UCB performs well (and when it doesn't)

---

**Enjoy learning! 🎉**
