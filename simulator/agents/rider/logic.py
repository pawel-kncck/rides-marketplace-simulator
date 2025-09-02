from ..rider.rider import RiderAgent

def calculate_utility(
    rider: RiderAgent,
    price: float,
    eta: int,
    preference_score_weight: float
) -> float:
    """
    Calculates the utility for a rider for a given offer.
    """
    utility = (
        (-rider.price_sensitivity * price)
        + (-rider.time_sensitivity * eta)
        + (preference_score_weight * rider.preference_score)
    )
    return utility
