import pandas as pd
import numpy as np
import json
from src.config import Config

def load_context():
    with open('data/eo_context.json', 'r') as f:
        return json.load(f)

def generate_crisis_data(shock_level):
    """Generates synthetic data based on the EO 110 Sec 1 & 5 narrative."""
    np.random.seed(Config.SEED)
    n = Config.N_SAMPLES
    
    # Sec 1: Global Risk
    oil_risk = np.random.normal(50, 15, n) * shock_level
    # Sec 5: DOE Optimization
    doe_buffer = np.random.normal(60, 10, n)
    
    # Sec 2: Policy Response (Confounded by Risk)
    policy_raw = (0.45 * oil_risk) + np.random.normal(0, 10, n)
    uplift = (policy_raw - policy_raw.min()) / (policy_raw.max() - policy_raw.min())
    
    # Sec 4: Outcome
    # True Causal Effect of UPLIFT is coded as +25.0
    stability = (120 - (0.8 * oil_risk) + (0.3 * doe_buffer) + (25 * uplift) + np.random.normal(0, 5, n))
    
    return pd.DataFrame({
        Config.CONFOUNDER: oil_risk,
        Config.MEDIATOR: doe_buffer,
        Config.TREATMENT: uplift,
        Config.OUTCOME: stability
    })