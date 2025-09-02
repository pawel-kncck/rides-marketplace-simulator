import pytest
from simulator.agents.driver.driver import DriverAgent, DriverState

def test_driver_initialization():
    """
    Tests that a DriverAgent is initialized with the correct properties
    and that its state defaults to the expected initial values.
    """
    # 1. Arrange: Define the specific inputs for creating the agent.
    agent_id = 201
    initial_location = (30, 40)
    is_exclusive = False
    preference_score = -0.5
    price_sensitivity = 0.7
    eta_sensitivity = 0.6

    # 2. Act: Create an instance of the DriverAgent.
    driver = DriverAgent(
        agent_id=agent_id,
        initial_location=initial_location,
        is_exclusive=is_exclusive,
        preference_score=preference_score,
        price_sensitivity=price_sensitivity,
        eta_sensitivity=eta_sensitivity
    )

    # 3. Assert: Verify that every property on the created object has the correct value.
    assert driver.agent_id == agent_id
    assert driver.location == initial_location
    assert driver.is_exclusive is False
    assert driver.preference_score == preference_score
    assert driver.price_sensitivity == price_sensitivity
    assert driver.eta_sensitivity == eta_sensitivity

    # ...and the properties that should have a default initial value.
    assert driver.current_state == DriverState.OFFLINE
    assert driver.idle_timer == 0

    # Test the __repr__ for consistent debugging output.
    expected_repr = "DriverAgent(id=201, state='OFFLINE', pref_score=-0.50)"
    assert repr(driver) == expected_repr
