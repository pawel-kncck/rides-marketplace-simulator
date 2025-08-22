# tests/unit/agents/test_rider.py

import pytest
from simulator.agents.rider.rider import RiderAgent, RiderState

def test_rider_initialization():
    """
    Tests that a RiderAgent is initialized with the correct properties
    and that its state defaults to the expected initial values.
    """
    # 1. Arrange: Define the specific inputs for creating the agent.
    # These are the values we expect the object to hold after creation.
    agent_id = 101
    initial_location = (10, 20)
    has_app_a = True
    has_app_b = False
    preference_score = 0.8
    price_sensitivity = 0.9
    time_sensitivity = 0.4
    rides_per_week = 2.5

    # 2. Act: Create an instance of the RiderAgent using the defined inputs.
    rider = RiderAgent(
        agent_id=agent_id,
        initial_location=initial_location,
        has_app_a=has_app_a,
        has_app_b=has_app_b,
        preference_score=preference_score,
        price_sensitivity=price_sensitivity,
        time_sensitivity=time_sensitivity,
        rides_per_week=rides_per_week
    )

    # 3. Assert: Verify that every property on the created object has the correct value.
    # We check both the properties we passed in...
    assert rider.agent_id == agent_id
    assert rider.location == initial_location
    assert rider.has_app_a is True
    assert rider.has_app_b is False
    assert rider.preference_score == preference_score
    assert rider.price_sensitivity == price_sensitivity
    assert rider.time_sensitivity == time_sensitivity
    assert rider.rides_per_week == rides_per_week

    # ...and the properties that should have a default initial value.
    assert rider.current_state == RiderState.IDLE
    assert rider.patience_timer == 0
    assert rider.active_discounts == []
    assert rider.enrolled_tests == {}

    # It's also good practice to test the __repr__ for consistent debugging output.
    expected_repr = "RiderAgent(id=101, state='IDLE', pref_score=0.80)"
    assert repr(rider) == expected_repr