import pytest
from simulator.market.space import HexGrid
from simulator.agents.rider.rider import RiderAgent

def test_hexgrid_initialization():
    """
    Tests that a HexGrid is initialized with the correct properties.
    """
    # 1. Arrange
    grid_resolution = 5

    # 2. Act
    grid = HexGrid(grid_resolution=grid_resolution)

    # 3. Assert
    assert grid.grid_resolution == grid_resolution
    assert repr(grid) == "HexGrid(grid_resolution=5)"

def test_add_and_get_agents():
    """
    Tests that agents can be added to the grid and retrieved.
    """
    # 1. Arrange
    grid = HexGrid(grid_resolution=10)
    rider1 = RiderAgent(agent_id=1, initial_location=(12, 23), has_app_a=True, has_app_b=True, preference_score=0.5, price_sensitivity=0.5, time_sensitivity=0.5, rides_per_week=3)
    rider2 = RiderAgent(agent_id=2, initial_location=(18, 29), has_app_a=True, has_app_b=True, preference_score=0.5, price_sensitivity=0.5, time_sensitivity=0.5, rides_per_week=3)
    rider3 = RiderAgent(agent_id=3, initial_location=(35, 45), has_app_a=True, has_app_b=True, preference_score=0.5, price_sensitivity=0.5, time_sensitivity=0.5, rides_per_week=3)

    # 2. Act
    grid.add_agent(rider1)
    grid.add_agent(rider2)
    grid.add_agent(rider3)

    # 3. Assert
    cell_1_2 = grid.get_cell_id(rider1.location)
    assert cell_1_2 == (1, 2)
    agents_in_cell_1_2 = grid.get_agents_in_cell(cell_1_2)
    assert len(agents_in_cell_1_2) == 2
    assert rider1 in agents_in_cell_1_2
    assert rider2 in agents_in_cell_1_2

    cell_3_4 = grid.get_cell_id(rider3.location)
    assert cell_3_4 == (3, 4)
    agents_in_cell_3_4 = grid.get_agents_in_cell(cell_3_4)
    assert len(agents_in_cell_3_4) == 1
    assert rider3 in agents_in_cell_3_4

    # Check an empty cell
    empty_cell_agents = grid.get_agents_in_cell((0, 0))
    assert len(empty_cell_agents) == 0
