from typing import Dict, Tuple

class HexGrid:
    """
    Represents the hexagonal grid of the simulation environment.
    """
    def __init__(self, grid_resolution: int):
        """
        Initializes the HexGrid.

        Args:
            grid_resolution: The resolution of the grid.
        """
        self.grid_resolution = grid_resolution
        self._grid: Dict[Tuple[int, int], list] = {}

    def __repr__(self) -> str:
        """
        Provides a developer-friendly representation of the HexGrid object.
        """
        return f"HexGrid(grid_resolution={self.grid_resolution})"
