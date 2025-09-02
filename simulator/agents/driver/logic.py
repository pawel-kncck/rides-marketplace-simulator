from ..driver.driver import DriverAgent

def calculate_profitability_score(
    driver: DriverAgent,
    fare: float,
    eta_to_rider: int
) -> float:
    """
    Calculates the profitability score for a driver for a given offer.
    """
    score = (
        (driver.price_sensitivity * fare)
        - (driver.eta_sensitivity * eta_to_rider)
    )
    return score
