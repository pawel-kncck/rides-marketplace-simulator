import pytest
from simulator.market.space import HexGrid

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
