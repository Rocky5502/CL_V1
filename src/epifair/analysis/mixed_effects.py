from __future__ import annotations

def fit_action_logit(df, action_col: str, uncertainty_col: str="uncertainty"):
    """Transparent clustered-logit baseline; preregister a GLMM implementation before confirmatory inference."""
    import statsmodels.formula.api as smf
    formula=(f"{action_col} ~ C(cue_variant) * {uncertainty_col} + C(information_state) + C(language) + C(domain) + C(model_id) + C(scenario_family_id)")
    return smf.logit(formula,data=df).fit(disp=False,cov_type="cluster",cov_kwds={"groups":df["scenario_family_id"]})
