import pandas as pd
from src.config import Config

def run_committee_mcda(scenarios, current_shock):
    """
    Ref: Section 3 Consensus.
    Simulates agency trade-offs between DOE, DSWD, and DBM.
    """
    df = pd.DataFrame(scenarios)
    
    # 1. Map Criteria to Mandates
    df["M_Stability"] = df["stability_pred"]     # Sec 5 (DOE)
    df["M_Welfare"] = df["intensity"] * 100      # Sec 6a/b (DSWD/DOTr)
    df["M_Fiscal"] = 100 - (df["intensity"] * 100) # Sec 9 (DBM/DOF)
    
    # 2. Normalization
    for c in ["M_Stability", "M_Welfare", "M_Fiscal"]:
        df[f"n_{c}"] = (df[c] - df[c].min()) / (df[c].max() - df[c].min() + 1e-6)
    
    # 3. Dynamic Weighting Logic
    if current_shock > Config.EMERGENCY_THRESHOLD:
        # Emergency Mode: Prioritize Stability and Welfare
        weights = {"n_M_Stability": 0.45, "n_M_Welfare": 0.45, "n_M_Fiscal": 0.10}
    else:
        # Prudence Mode: Prioritize Fiscal health
        weights = {"n_M_Stability": 0.30, "n_M_Welfare": 0.20, "n_M_Fiscal": 0.50}
        
    df["MCDA_Score"] = sum(df[k] * v for k, v in weights.items())
    return df.sort_values("MCDA_Score", ascending=False), weights