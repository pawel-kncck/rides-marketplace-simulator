from typing import List, Tuple, Optional
from simulator.market.space import HexGrid
from simulator.agents.driver.driver import DriverAgent, DriverState
from simulator.agents.rider.rider import RiderAgent, RiderState
from simulator.agents.driver.logic import calculate_profitability_score

class Matcher:
    """
    The platform's matching engine.
    """
    def __init__(self, grid: HexGrid, max_order_tries: int = 3):
        """
        Initializes the Matcher.

        Args:
            grid: The HexGrid object.
            max_order_tries: The maximum number of drivers to try for a single order.
        """
        self.grid = grid
        self.max_order_tries = max_order_tries

    def find_nearest_idle_drivers(self, rider: RiderAgent) -> List[DriverAgent]:
        """
        Finds the N nearest idle drivers to a rider.
        """
        rider_cell = self.grid.get_cell_id(rider.location)
        # This is a simplified implementation. A real implementation would search
        # neighboring cells in a spiral pattern.
        drivers_in_cell = self.grid.get_agents_in_cell(rider_cell)
        idle_drivers = [d for d in drivers_in_cell if isinstance(d, DriverAgent) and d.current_state == DriverState.IDLE]
        return idle_drivers

    def process_order(self, rider: RiderAgent, fare: float) -> Tuple[Optional[DriverAgent], str]:
        """
        Processes a ride order from a rider.

        Returns:
            A tuple containing the matched driver (or None) and the outcome status.
        """
        idle_drivers = self.find_nearest_idle_drivers(rider)

        for i, driver in enumerate(idle_drivers):
            if i >= self.max_order_tries:
                return None, "UNFULFILLED_MAX_TRIES"

            eta_to_rider = 5 # Simplified ETA
            profitability_score = calculate_profitability_score(driver, fare, eta_to_rider)

            # Simplified acceptance logic
            if profitability_score > 0:
                driver.current_state = DriverState.DRIVING_TO_RIDER
                rider.current_state = RiderState.ORDERED
                return driver, "MATCH_SUCCESSFUL"

        return None, "UNFULFILLED_NO_DRIVERS"
