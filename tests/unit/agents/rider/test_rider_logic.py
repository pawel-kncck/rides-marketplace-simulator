import pytest
from simulator.agents.rider.rider import RiderAgent
from simulator.agents.rider.logic import calculate_utility

@pytest.fixture
def rider_agent():
    """Provides a default RiderAgent for tests."""
    return RiderAgent(
        agent_id=1,
        initial_location=(0, 0),
        has_app_a=True,
        has_app_b=True,
        preference_score=0.2,  # Slight preference for platform A
        price_sensitivity=0.8,
        time_sensitivity=0.6,
        rides_per_week=3
    )

def test_utility_prefers_lower_price(rider_agent):
    """Utility should be higher for a lower price, all else being equal."""
    utility_high_price = calculate_utility(rider_agent, price=20, eta=5, preference_score_weight=0.5)
    utility_low_price = calculate_utility(rider_agent, price=15, eta=5, preference_score_weight=0.5)
    assert utility_low_price > utility_high_price

def test_utility_prefers_lower_eta(rider_agent):
    """Utility should be higher for a lower ETA, all else being equal."""
    utility_high_eta = calculate_utility(rider_agent, price=15, eta=10, preference_score_weight=0.5)
    utility_low_eta = calculate_utility(rider_agent, price=15, eta=5, preference_score_weight=0.5)
    assert utility_low_eta > utility_high_eta

def test_utility_respects_preference(rider_agent):
    """A positive preference score should increase utility."""
    utility_with_pref = calculate_utility(rider_agent, price=15, eta=5, preference_score_weight=0.5)
    rider_agent.preference_score = -0.2 # Change preference to B
    utility_without_pref = calculate_utility(rider_agent, price=15, eta=5, preference_score_weight=0.5)
    assert utility_with_pref > utility_without_pref
