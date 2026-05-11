class Config:
    PROJECT_NAME = "UPLIFT Policy Decision Simulator"
    VERSION = "2026.1.0"
    
    # Simulation Parameters
    DEFAULT_N = 1000
    SEED = 42
    
    # MCDA Thresholds
    # When the shock exceeds this, the system prioritizes welfare over fiscal health (Sec 1 vs Sec 9)
    CRISIS_MODE_THRESHOLD = 2.2 
    
    # Causal Graph Constants
    TREATMENT = "UPLIFT_Intensity"
    OUTCOME = "Stability_Index"
    CONFOUNDER = "Global_Oil_Risk"
    MEDIATOR = "DOE_Energy_Buffer"