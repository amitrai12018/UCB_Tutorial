"""
Configuration and styling for the UCB Tutorial app
"""

# Application configuration
APP_CONFIG = {
    "title": "UCB Tutorial & Parameter Selection",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Default parameters
DEFAULT_PARAMS = {
    "true_ctrs": [0.05, 0.10, 0.20],
    "n_rounds": 500,
    "c_value": 2.0,
    "min_rounds": 50,
    "max_rounds": 20000,
}

# Styling
STYLES = """
<style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Info boxes */
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #1e3a8a;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        color: #854d0e;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Ad display boxes */
    .ad-box-selected {
        border: 3px solid #2ecc71;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        background: linear-gradient(135deg, #f0fff5 0%, #e8f5e9 100%);
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
        transition: all 0.3s ease;
    }
    
    .ad-box-idle {
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        background: #fafafa;
        transition: all 0.3s ease;
    }
    
    .ad-box-idle:hover {
        background: #f0f0f0;
        border-color: #bdbdbd;
    }
    
    /* Stats panel */
    .stats-panel {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Game section */
    .game-score {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .user-score {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .ucb-score {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    /* Tooltips and help text */
    .help-text {
        font-size: 0.9rem;
        color: #666;
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
</style>
"""

# Color schemes
COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#2ecc71",
    "warning": "#f39c12",
    "danger": "#e74c3c",
    "info": "#3498db",
}
