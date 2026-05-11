def validate_inputs(shock_value):
    """Ensures input parameters are within logical bounds."""
    if not (1.0 <= shock_value <= 5.0):
        raise ValueError("Shock value must be between 1.0 (Normal) and 5.0 (Extreme).")
    return True