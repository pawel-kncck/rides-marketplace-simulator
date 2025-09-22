import pytest
from unittest.mock import Mock
from simulator.platform.matcher import Matcher
from simulator.market.space import HexGrid
from simulator.agents.rider.rider import RiderAgent, RiderState
from simulator.agents.driver.driver import DriverAgent, DriverState as DriverStateEnum

@pytest.fixture
def grid():
    """Provides a HexGrid with some agents for tests."""
    grid = HexGrid(grid_resolution=10)
    # Idle driver in the same cell as the rider
    idle_driver = DriverAgent(1, (5, 5), False, 0.5, 0.5, 0.5)
    idle_driver.current_state = DriverStateEnum.IDLE
    grid.add_agent(idle_driver)
    # Busy driver in the same cell
    busy_driver = DriverAgent(2, (6, 6), False, 0.5, 0.5, 0.5)
    busy_driver.current_state = DriverStateEnum.ON_TRIP
    grid.add_agent(busy_driver)
    # Idle driver in a different cell
    other_idle_driver = DriverAgent(3, (25, 25), False, 0.5, 0.5, 0.5)
    other_idle_driver.current_state = DriverStateEnum.IDLE
    grid.add_agent(other_idle_driver)
    return grid

@pytest.fixture
def rider():
    """Provides a RiderAgent for tests."""
    return RiderAgent(101, (5, 5), True, True, 0.5, 0.5, 0.5, 3)

def test_matcher_finds_nearest_idle_drivers(grid, rider):
    """Tests that the matcher can find the closest idle driver."""
    matcher = Matcher(grid)
    idle_drivers = matcher.find_nearest_idle_drivers(rider)
    assert len(idle_drivers) == 1
    assert idle_drivers[0].agent_id == 1

def test_matcher_cycles_to_next_driver_on_rejection(grid, rider):
    """Tests that the matcher tries the next driver if the first one rejects."""
    # Make the first driver reject the ride
    driver1 = grid.get_agents_in_cell(grid.get_cell_id((5,5)))[0]
    driver1.price_sensitivity = 0.1 # Will reject a fare of 10

    # Add another idle driver to the cell who will accept
    driver2 = DriverAgent(4, (7, 7), False, 0.9, 0.5, 0.5)
    driver2.current_state = DriverStateEnum.IDLE
    grid.add_agent(driver2)

    matcher = Matcher(grid)
    matched_driver, status = matcher.process_order(rider, fare=10)

    assert status == "MATCH_SUCCESSFUL"
    assert matched_driver.agent_id == 4

def test_matcher_prioritizes_nearest_driver(grid):
    """Tests that the matcher prioritizes the nearest driver."""
    # Arrange
    rider = RiderAgent(101, (10, 10), True, True, 0.5, 0.5, 0.5, 3)
    grid.add_agent(rider)

    # Create two idle drivers in the same cell, but at different distances
    driver_far = DriverAgent(1, (18, 18), False, 0.9, 0.5, 0.5)
    driver_far.current_state = DriverStateEnum.IDLE
    grid.add_agent(driver_far)

    driver_close = DriverAgent(2, (11, 11), False, 0.9, 0.5, 0.5)
    driver_close.current_state = DriverStateEnum.IDLE
    grid.add_agent(driver_close)

    matcher = Matcher(grid)
    matched_driver, status = matcher.process_order(rider, fare=10, order_id="test_order", day=0, tick=0)

    assert status == "MATCH_SUCCESSFUL"
    assert matched_driver.agent_id == driver_close.agent_id

def test_matcher_unfulfilled_if_no_drivers(rider):
    """Tests that the order is unfulfilled if no drivers are available."""
    empty_grid = HexGrid(grid_resolution=10)
    matcher = Matcher(empty_grid)
    matched_driver, status = matcher.process_order(rider, fare=20, order_id="test_order", day=0, tick=0)

    assert status == "UNFULFILLED_NO_DRIVERS"
    assert matched_driver is None