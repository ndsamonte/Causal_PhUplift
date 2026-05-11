import streamlit as st
import plotly.express as px
from src.data_manager import generate_crisis_data, load_context
from src.causal_engine import UpliftCausalEngine
from src.mcda_engine import run_committee_mcda
from src.validator import validate_shock_input
import sys
from pathlib import Path

# Adds the parent directory of 'src' to the search path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

# NOW imports will work
from src.data_manager import generate_crisis_data, load_context

# UI Setup
st.set_page_config(page_title="UPLIFT Causal Pro", layout="wide")
ctx = load_context()

st.title(f"🚦 {ctx['package_definition']['description']}")
st.caption(f"Ref: Executive Order No. 110 (Technical Secretariat Support)")

# Sidebar: Sec 1 Risk
st.sidebar.header("Section 1: Emergency Risk")
shock = st.sidebar.slider("Geopolitical Shock Severity", 1.0, 4.0, 1.8)

if st.button("Execute Committee Decision Logic"):
    validate_shock_input(shock)
    
    # 1. Causal Brain
    data = generate_crisis_data(shock)
    engine = UpliftCausalEngine(data)
    ate = engine.estimate_causal_lift()
    
    # 2. Counterfactual Simulation (Sec 2)
    scenarios = []
    for lvl, label in zip([0.0, 0.5, 0.95], ["Status Quo", "Moderate Response", "Max UPLIFT"]):
        pred = engine.do_calculus_simulation(lvl)
        scenarios.append({"scenario": label, "intensity": lvl, "stability_pred": pred})
    
    # 3. MCDA Consensus (Sec 3)
    ranked_df, current_weights = run_committee_mcda(scenarios, shock)
    best = ranked_df.iloc[0]

    # --- UI DISPLAY ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Causal Impact Identification")
        st.metric("Sec 2 Package ATE", f"+{round(ate, 2)} pts")
        
        # Radar Plot
        radar_df = ranked_df.melt(id_vars=["scenario"], value_vars=["n_M_Stability", "n_M_Welfare", "n_M_Fiscal"])
        fig = px.line_polar(radar_df, r="value", theta="variable", color="scenario", line_close=True)
        st.plotly_chart(fig)

    with col2:
        st.subheader("Committee Recommendation")
        st.success(f"**Recommended Action: {best['scenario']}**")
        st.info(f"**Directives Triggered:**\n- {ctx['mandates']['DOTr']}\n- {ctx['mandates']['DSWD']}\n- {ctx['mandates']['DBM']}")
        st.table(ranked_df[["scenario", "MCDA_Score", "stability_pred"]])