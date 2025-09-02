import pytest
from simulator.market.market import Market

@pytest.fixture
def config():
    """Provides a default config for tests."""
    return {
        'market': {
            'grid_resolution': 10,
            'initial_riders': 5,
            'initial_drivers': 2,
            'rider_population': {
                'price_sensitivity_dist': [0.5, 0.2],
                'time_sensitivity_dist': [0.5, 0.2],
                'preference_score_dist': [0.0, 0.3]
            },
            'driver_population': {
                'price_sensitivity_dist': [0.7, 0.1],
                'eta_sensitivity_dist': [0.3, 0.1],
                'preference_score_dist': [0.0, 0.2]
            }
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

def test_agent_properties_are_set(config):
    """Tests that agent properties are set from the config."""
    # 1. Act
    market = Market(config)

    # 2. Assert
    # Check a sample rider
    rider = market.riders[0]
    assert isinstance(rider.price_sensitivity, float)
    assert isinstance(rider.time_sensitivity, float)
    assert isinstance(rider.preference_score, float)

    # Check a sample driver
    driver = market.drivers[0]
    assert isinstance(driver.price_sensitivity, float)
    assert isinstance(driver.eta_sensitivity, float)
    assert isinstance(driver.preference_score, float)
