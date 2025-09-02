import random
from typing import Dict, List
from simulator.market.space import HexGrid
from simulator.agents.rider.rider import RiderAgent
from simulator.agents.driver.driver import DriverAgent, DriverState

class Market:
    """
    The central market module.
    """
    def __init__(self, config: Dict):
        """
        Initializes the Market.

        Args:
            config: The simulation configuration.
        """
        self.grid = HexGrid(config['market']['grid_resolution'])
        self.riders: List[RiderAgent] = []
        self.drivers: List[DriverAgent] = []

        self._create_riders(config)
        self._create_drivers(config)

    def _create_riders(self, config: Dict):
        """
        Creates the rider population.
        """
        rider_config = config['market']['rider_population']
        for i in range(config['market']['initial_riders']):
            rider = RiderAgent(
                agent_id=i,
                initial_location=(0, 0), # Placeholder
                has_app_a=True, # Placeholder
                has_app_b=True, # Placeholder
                preference_score=random.normalvariate(*rider_config['preference_score_dist']), # Placeholder
                price_sensitivity=random.normalvariate(*rider_config['price_sensitivity_dist']), # Placeholder
                time_sensitivity=random.normalvariate(*rider_config['time_sensitivity_dist']), # Placeholder
                rides_per_week=3 # Placeholder
            )
            self.riders.append(rider)
            self.grid.add_agent(rider)

    def _create_drivers(self, config: Dict):
        """
        Creates the driver population.
        """
        driver_config = config['market']['driver_population']
        for i in range(config['market']['initial_drivers']):
            driver = DriverAgent(
                agent_id=i + config['market']['initial_riders'],
                initial_location=(0, 0), # Placeholder
                is_exclusive=False, # Placeholder
                preference_score=random.normalvariate(*driver_config['preference_score_dist']), # Placeholder
                price_sensitivity=random.normalvariate(*driver_config['price_sensitivity_dist']), # Placeholder
                eta_sensitivity=random.normalvariate(*driver_config['eta_sensitivity_dist']) # Placeholder
            )
            self.drivers.append(driver)
            self.grid.add_agent(driver)

    def update_platform_strategies(self):
        pass

    def update_driver_go_online_decisions(self):
        pass

    def update_rider_search_intent(self):
        pass

    def process_rider_searches(self):
        pass

    def process_matcher_offers(self):
        pass

    def process_driver_responses(self):
        pass

    def update_agent_locations(self):
        pass
