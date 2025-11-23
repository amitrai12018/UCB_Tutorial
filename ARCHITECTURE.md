# 🏗️ UCB Tutorial App - Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                         │
│                    http://localhost:8501                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      STREAMLIT SERVER                        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                      app.py                          │  │
│  │              (Main Entry Point)                      │  │
│  │  • Initialize page config                            │  │
│  │  • Load styling                                      │  │
│  │  • Render sidebar                                    │  │
│  │  • Create 5 tabs                                     │  │
│  └─────────────┬───────────────┬────────────────────────┘  │
│                │               │                            │
│                ▼               ▼                            │
│  ┌─────────────────┐  ┌──────────────────────┐            │
│  │   config.py     │  │  ui_components.py    │            │
│  │                 │  │                      │            │
│  │ • APP_CONFIG    │  │ • setup_page()       │            │
│  │ • STYLES        │  │ • render_sidebar()   │            │
│  │ • COLORS        │  │ • render_ad_boxes()  │            │
│  │ • DEFAULT_PARAMS│  │ • render_stats()     │            │
│  └─────────────────┘  │ • show_messages()    │            │
│                       └──────────────────────┘            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                     tabs.py                          │  │
│  │                (5 Tab Renderers)                     │  │
│  │                                                       │  │
│  │  Tab 1: render_primer_tab()                          │  │
│  │  • Theory & concepts                                 │  │
│  │  • Formula explanations                              │  │
│  │  • Interactive examples                              │  │
│  │                                                       │  │
│  │  Tab 2: render_visual_tab()                          │  │
│  │  • Step-by-step simulation                           │  │
│  │  • Decision explanations                             │  │
│  │  • Real-time statistics                              │  │
│  │                                                       │  │
│  │  Tab 3: render_comparison_tab()                      │  │
│  │  • Multi-parameter comparison                        │  │
│  │  • Learning curves                                   │  │
│  │  • Performance metrics                               │  │
│  │                                                       │  │
│  │  Tab 4: render_statistical_tab()                     │  │
│  │  • ANOVA testing                                     │  │
│  │  • Pairwise comparisons                              │  │
│  │  • Statistical significance                          │  │
│  │                                                       │  │
│  │  Tab 5: render_game_tab()                            │  │
│  │  • Interactive game                                  │  │
│  │  • Hidden CTRs                                       │  │
│  │  • Competition with UCB                              │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│                     ▼                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              ucb_algorithm.py                        │  │
│  │           (Core Algorithm Logic)                     │  │
│  │                                                       │  │
│  │  ┌────────────────────────────────────┐             │  │
│  │  │        UCBAgent Class              │             │  │
│  │  │  • Q: Estimated values             │             │  │
│  │  │  • N: Selection counts             │             │  │
│  │  │  • select_action()                 │             │  │
│  │  │  • update()                        │             │  │
│  │  │  • get_ucb_values()                │             │  │
│  │  └────────────────────────────────────┘             │  │
│  │                                                       │  │
│  │  Functions:                                          │  │
│  │  • simulate_ucb_episode()                            │  │
│  │  • run_multiple_simulations()                        │  │
│  │  • get_optimal_ctr()                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Example: Visual Simulation Tab

```
1. User clicks "Next Round"
   │
   ▼
2. tabs.py:render_visual_tab()
   │
   ├──> Gets config from sidebar
   │
   ├──> Creates/updates UCBAgent
   │    │
   │    └──> ucb_algorithm.py:UCBAgent
   │         • Computes UCB values
   │         • Selects action
   │
   ├──> Generates reward from true CTR
   │
   ├──> Updates agent with reward
   │
   └──> Renders UI
        │
        ├──> ui_components.py:render_ad_boxes()
        ├──> ui_components.py:render_stats_panel()
        └──> Update session state
             │
             └──> Streamlit re-renders page
```

### Example: Game Tab

```
1. Game starts
   │
   ├──> Generate random CTRs (HIDDEN)
   └──> Initialize both agents (user & UCB)
   
2. Each round:
   │
   ├──> User selects ad
   │    │
   │    ├──> Generate reward from true CTR
   │    └──> Update user's estimates
   │
   ├──> UCB agent selects ad
   │    │
   │    ├──> ucb_algorithm.py:UCBAgent.select_action()
   │    ├──> Generate reward from true CTR
   │    └──> Update UCB's estimates
   │
   └──> Update UI with scores
   
3. Game ends
   │
   ├──> Reveal true CTRs
   ├──> Show winner
   └──> Display full history
```

## Module Interactions

```
┌───────────────┐
│   app.py      │  ◄─── Entry point
└───────┬───────┘
        │
        ├─────► config.py           (Loads settings)
        │
        ├─────► ui_components.py    (Sets up page)
        │
        └─────► tabs.py            (Creates content)
                    │
                    ├─────► ucb_algorithm.py  (Simulations)
                    │
                    └─────► ui_components.py  (Renders UI)
```

## Session State Management

```
Session State Structure:
├── visual_state
│   ├── round: int
│   ├── agent: UCBAgent
│   ├── clicks: List[int]
│   └── history: List[dict]
│
├── comparison_data: DataFrame
│   └── {c, run, round, avg_ctr}
│
├── stat_results: dict
│   ├── results: Dict[float, List[float]]
│   ├── c_values: List[float]
│   └── alpha: float
│
└── game_state
    ├── round: int
    ├── max_rounds: int
    ├── true_ctrs: List[float]  ◄─── HIDDEN FROM USER
    ├── user_clicks: int
    ├── ucb_clicks: int
    ├── ucb_agent: UCBAgent
    ├── user_Q: ndarray
    ├── user_N: ndarray
    ├── history: List[dict]
    └── game_over: bool
```

## Component Responsibilities

### app.py
**Role**: Orchestrator
- Initialize application
- Configure Streamlit
- Coordinate tabs
- Apply styling

### config.py
**Role**: Configuration Manager
- Store constants
- Define styling
- Set defaults
- Manage colors

### ucb_algorithm.py
**Role**: Business Logic
- Implement UCB algorithm
- Manage agent state
- Run simulations
- Calculate metrics

### ui_components.py
**Role**: Presentation Layer
- Render UI elements
- Create visualizations
- Handle user input
- Display messages

### tabs.py
**Role**: Feature Modules
- Implement tab logic
- Coordinate components
- Manage tab state
- Process user actions

## Key Design Patterns

### 1. Separation of Concerns
```
UI ──────► Presentation (ui_components.py)
Logic ────► Business (ucb_algorithm.py)
Config ───► Settings (config.py)
Flow ─────► Control (app.py, tabs.py)
```

### 2. Modular Design
```
Each module is:
✓ Independent
✓ Reusable
✓ Testable
✓ Maintainable
```

### 3. State Management
```
Streamlit Session State
├── Persistent across reruns
├── Tab-specific states
└── Game state isolation
```

## Extensibility Points

### Add New Tab
1. Create function in `tabs.py`
2. Add to tab list in `app.py`
3. Use existing UI components
4. Access UCB algorithm

### Add New Algorithm
1. Create class in `ucb_algorithm.py`
2. Implement select_action() and update()
3. Use in tab renderers
4. Compare with UCB

### Customize Styling
1. Edit STYLES in `config.py`
2. Add new CSS classes
3. Use in UI components
4. Instant updates

### Add Visualization
1. Use Altair in `tabs.py`
2. Process data with pandas
3. Apply custom styling
4. Make interactive

## Summary

This architecture provides:

✅ **Modularity**: Easy to understand and modify
✅ **Scalability**: Add features without breaking existing code
✅ **Maintainability**: Clear structure and responsibilities
✅ **Testability**: Each module can be tested independently
✅ **Reusability**: Components used across multiple tabs
✅ **Professionalism**: Industry-standard patterns

The modular design makes it easy to:
- Add new algorithms
- Create new visualizations
- Implement new game modes
- Extend functionality
- Fix bugs
- Improve performance

**Result**: A professional, maintainable, extensible educational platform! 🎯
