import pytest
from simulator.agents.driver.driver import DriverAgent
from simulator.agents.driver.logic import calculate_profitability_score

@pytest.fixture
def driver_agent():
    """Provides a default DriverAgent for tests."""
    return DriverAgent(
        agent_id=1,
        initial_location=(0, 0),
        is_exclusive=False,
        preference_score=0.0,
        price_sensitivity=0.7,
        eta_sensitivity=0.3
    )

def test_profitability_prefers_higher_fare(driver_agent):
    """Profitability should be higher for a higher fare, all else being equal."""
    score_high_fare = calculate_profitability_score(driver_agent, fare=30, eta_to_rider=5)
    score_low_fare = calculate_profitability_score(driver_agent, fare=20, eta_to_rider=5)
    assert score_high_fare > score_low_fare

def test_profitability_rejects_long_eta(driver_agent):
    """Profitability should be lower for a longer ETA, all else being equal."""
    score_high_eta = calculate_profitability_score(driver_agent, fare=25, eta_to_rider=15)
    score_low_eta = calculate_profitability_score(driver_agent, fare=25, eta_to_rider=5)
    assert score_low_eta > score_high_eta
