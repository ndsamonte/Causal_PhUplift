import statsmodels.api as sm
from dowhy import CausalModel
from src.config import Config
from src.logger import get_logger

log = get_logger(__name__)

class UpliftCausalEngine:
    def __init__(self, data):
        self.data = data
        self.learner = None

    def estimate_causal_lift(self):
        # EXPLICIT DAG: Mapping the narrative of EO 110
        causal_graph = f"""
        digraph {{
            {Config.CONFOUNDER} -> {Config.TREATMENT};
            {Config.CONFOUNDER} -> {Config.OUTCOME};
            {Config.MEDIATOR} -> {Config.OUTCOME};
            {Config.TREATMENT} -> {Config.OUTCOME};
        }}
        """
        
        log.info("Identifying Causal Effect using Explicit EO 110 DAG.")
        model = CausalModel(
            data=self.data,
            treatment=Config.TREATMENT,
            outcome=Config.OUTCOME,
            graph=causal_graph.replace("\n", " ")
        )
        
        # Step 2: Identification (Finds Backdoor Criterion)
        estimand = model.identify_effect()
        
        # Step 3: Estimation (Isolates Section 2 Effectiveness)
        estimate = model.estimate_effect(estimand, method_name="backdoor.linear_regression")

        # Explicit transparent learner
        X = self.data[
            [Config.CONFOUNDER,
            Config.MEDIATOR,
            Config.TREATMENT]
        ]

        X = sm.add_constant(X)

        y = self.data[Config.OUTCOME]

        self.learner = sm.OLS(y, X).fit()

        return estimate.value

    def do_calculus_simulation(self, intensity_level):
        """Perform do(UPLIFT=x) counterfactual simulation."""
        cf_df = self.data.copy()
        cf_df[Config.TREATMENT] = intensity_level
        
        # Prepare features for the linear learner
        features = [Config.CONFOUNDER, Config.MEDIATOR, Config.TREATMENT]
        X = sm.add_constant(cf_df[features], has_constant='add')
        
        return self.learner.predict(X).mean()