import random
from typing import Dict, List
from simulator.market.space import HexGrid
from simulator.agents.rider.rider import RiderAgent, RiderState
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
            # Logic for app ownership based on config probabilities
            app_roll = random.random()
            has_app_a, has_app_b = False, False
            if app_roll < rider_config['pct_with_app_a_only']:
                has_app_a = True
            elif app_roll < (rider_config['pct_with_app_a_only'] + rider_config['pct_with_app_b_only']):
                has_app_b = True
            else:
                has_app_a, has_app_b = True, True

            rider = RiderAgent(
                agent_id=i,
                initial_location=(random.randint(0, 10000), random.randint(0, 10000)),
                has_app_a=has_app_a,
                has_app_b=has_app_b,
                preference_score=random.normalvariate(*rider_config['preference_score_dist']),
                price_sensitivity=random.normalvariate(*rider_config['price_sensitivity_dist']),
                time_sensitivity=random.normalvariate(*rider_config['time_sensitivity_dist']),
                rides_per_week=max(0, random.normalvariate(*rider_config['rides_per_week_dist']))
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
                initial_location=(random.randint(0, 10000), random.randint(0, 10000)),
                is_exclusive=(random.random() < driver_config['pct_exclusive']),
                preference_score=random.normalvariate(*driver_config['preference_score_dist']),
                price_sensitivity=random.normalvariate(*driver_config['price_sensitivity_dist']),
                eta_sensitivity=random.normalvariate(*driver_config['eta_sensitivity_dist'])
            )
            self.drivers.append(driver)
            self.grid.add_agent(driver)

    def update_platform_strategies(self):
        pass

    def update_driver_go_online_decisions(self):
        """
        Decide which OFFLINE drivers should come online for a "shift."
        """
        for driver in self.drivers:
            if driver.current_state == DriverState.OFFLINE:
                if random.random() < 0.1:
                    driver.current_state = DriverState.IDLE

    def update_rider_search_intent(self):
        """
        Determine which IDLE riders decide to start looking for a ride.
        """
        for rider in self.riders:
            if rider.current_state == RiderState.IDLE:
                prob = rider.rides_per_week / (7 * 24)
                if random.random() < prob:
                    rider.current_state = RiderState.SEARCHING

    def process_rider_searches(self):
        pass

    def process_matcher_offers(self):
        pass

    def process_driver_responses(self):
        pass

    def update_agent_locations(self):
        pass
