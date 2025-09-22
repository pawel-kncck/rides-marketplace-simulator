import logging
from typing import List, Tuple, Optional
from simulator.market.space import HexGrid
from simulator.agents.driver.driver import DriverAgent, DriverState
from simulator.agents.rider.rider import RiderAgent, RiderState
from simulator.agents.driver.logic import calculate_profitability_score
from simulator.utils.time_utils import ticks_to_time_string
from simulator.utils.helpers import calculate_distance

class Matcher:
    """
    The platform's matching engine.
    """
    def __init__(self, grid: HexGrid, max_order_tries: int = 3, ticks_per_major: int = 60):
        """
        Initializes the Matcher.

        Args:
            grid: The HexGrid object.
            max_order_tries: The maximum number of drivers to try for a single order.
        """
        self.grid = grid
        self.max_order_tries = max_order_tries
        self.ticks_per_major = ticks_per_major

    def find_nearest_idle_drivers(self, rider: RiderAgent) -> List[DriverAgent]:
        """
        Finds idle drivers in the rider's cell and sorts them by distance.
        """
        rider_cell = self.grid.get_cell_id(rider.location)
        drivers_in_cell = self.grid.get_agents_in_cell(rider_cell)
        idle_drivers = [d for d in drivers_in_cell if isinstance(d, DriverAgent) and d.current_state == DriverState.IDLE]

        # --- NEW LOGIC: Sort drivers by distance ---
        idle_drivers.sort(key=lambda driver: calculate_distance(driver.location, rider.location))
        
        return idle_drivers

    def process_order(self, rider: RiderAgent, fare: float, order_id: str, day: int, tick: int) -> Tuple[Optional[DriverAgent], str]:
        """
        Processes a ride order from a rider.

        Returns:
            A tuple containing the matched driver (or None) and the outcome status.
        """
        time_str = ticks_to_time_string(day, tick, self.ticks_per_major)
        logging.info(f"MATCHER | ORDER_RECEIVED   | {time_str} | Order {order_id} from Rider {rider.agent_id}. Searching for drivers.")
        idle_drivers = self.find_nearest_idle_drivers(rider)

        if not idle_drivers:
            logging.warning(f"MATCHER | MATCH_FAILED     | {time_str} | Order {order_id}: Failed to match. Reason: UNFULFILLED_NO_DRIVERS.")
            return None, "UNFULFILLED_NO_DRIVERS"

        for i, driver in enumerate(idle_drivers):
            if i >= self.max_order_tries:
                logging.warning(f"MATCHER | MATCH_FAILED     | {time_str} | Order {order_id}: Failed to match. Reason: UNFULFILLED_MAX_TRIES.")
                return None, "UNFULFILLED_MAX_TRIES"

            eta_to_rider = 5 # Simplified ETA
            profitability_score = calculate_profitability_score(driver, fare, eta_to_rider)
            logging.info(f"MATCHER | DRIVER_PROPOSED  | {time_str} | Order {order_id}: Attempting Driver {driver.agent_id} at {driver.location} for Rider {rider.agent_id} at {rider.location} (Profitability Score: {profitability_score:.2f}).")

            if profitability_score > 0:
                logging.info(f"MATCHER | DRIVER_ACCEPTED  | {time_str} | Order {order_id}: Driver {driver.agent_id} ACCEPTED the offer.")
                return driver, "MATCH_SUCCESSFUL"
            else:
                logging.info(f"MATCHER | DRIVER_REJECTED  | {time_str} | Order {order_id}: Driver {driver.agent_id} REJECTED the offer (score {profitability_score:.2f} <= 0).")

        logging.warning(f"MATCHER | MATCH_FAILED     | {time_str} | Order {order_id}: Failed to match after trying all available drivers. Reason: UNFULFILLED_NO_DRIVERS.")
        return None, "UNFULFILLED_NO_DRIVERS"
