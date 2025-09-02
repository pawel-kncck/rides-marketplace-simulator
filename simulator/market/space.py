from typing import Dict, Tuple, List, Union
from ..agents.rider.rider import RiderAgent
from ..agents.driver.driver import DriverAgent

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
        self._grid: Dict[Tuple[int, int], List[Union[DriverAgent, RiderAgent]]] = {}

    def get_cell_id(self, location: Tuple[int, int]) -> Tuple[int, int]:
        """
        Converts a location to a cell ID.
        """
        return (
            int(location[0] / self.grid_resolution),
            int(location[1] / self.grid_resolution),
        )

    def add_agent(self, agent: Union[DriverAgent, RiderAgent]):
        """
        Adds an agent to the grid.
        """
        cell_id = self.get_cell_id(agent.location)
        if cell_id not in self._grid:
            self._grid[cell_id] = []
        self._grid[cell_id].append(agent)

    def get_agents_in_cell(self, cell_id: Tuple[int, int]) -> List[Union[DriverAgent, RiderAgent]]:
        """
        Returns the list of agents in a given cell.
        """
        return self._grid.get(cell_id, [])

    def __repr__(self) -> str:
        """
        Provides a developer-friendly representation of the HexGrid object.
        """
        return f"HexGrid(grid_resolution={self.grid_resolution})"
