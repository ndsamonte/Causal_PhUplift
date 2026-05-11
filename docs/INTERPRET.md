# 🧠 Causal Interpretability Guide (EO 110)

### The DAG (Directed Acyclic Graph)
We explicitly map the **Section 1 Emergency** as a confounder. In the graph:
1. `Global_Oil_Risk` $\rightarrow$ `Stability` (The direct threat).
2. `Global_Oil_Risk` $\rightarrow$ `UPLIFT_Intensity` (The government response).

By identifying the "Backdoor" path from Oil Risk to Stability, the engine mathematically adjusts the results so the Committee sees the **true effectiveness** of the UPLIFT package, independent of the oil crisis.

### Counterfactuals (The Do-Operator)
When we adjust the simulator, we are performing $P(Stability | do(UPLIFT = x))$. This is not a correlation; it is a simulation of a parallel universe where the President mandates a specific intervention level.