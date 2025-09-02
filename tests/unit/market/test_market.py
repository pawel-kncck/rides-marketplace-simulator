import pytest
from simulator.market.market import Market

@pytest.fixture
def config():
    """Provides a default config for tests."""
    return {
        'market': {
            'grid_resolution': 10,
            'initial_riders': 5,
            'initial_drivers': 2
        }
    }

def test_market_initialization(config):
    """Tests that the Market is initialized with the correct properties."""
    # 1. Act
    market = Market(config)

    # 2. Assert
    assert market.grid.grid_resolution == 10
    assert len(market.riders) == 5
    assert len(market.drivers) == 2

    # Check that agents were added to the grid
    # A simple check is to see if the grid has agents in the cell for location (0,0)
    cell_0_0 = market.grid.get_cell_id((0,0))
    agents_in_cell = market.grid.get_agents_in_cell(cell_0_0)
    assert len(agents_in_cell) == 7 # 5 riders + 2 drivers
