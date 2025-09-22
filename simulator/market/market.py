import random
import logging
from typing import Dict, List
from simulator.market.space import HexGrid
from simulator.agents.rider.rider import RiderAgent, RiderState
from simulator.agents.driver.driver import DriverAgent, DriverState
from simulator.platform.platform import Platform
from simulator.utils.time_utils import ticks_to_time_string

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
        self.config = config
        self.engine = None # Will be set later
        self.ticks_per_major = self.config['simulation']['ticks_per_major']
        self.grid = HexGrid(config['market']['grid_resolution'])
        self.platforms: List[Platform] = []
        self.riders: List[RiderAgent] = []
        self.drivers: List[DriverAgent] = []

        self._create_riders(config)
        self._create_drivers(config)

    def set_engine(self, engine):
        """Links the market to the simulation engine and schedules initial events."""
        self.engine = engine
        self._schedule_initial_events()

    def set_platforms(self, platforms: List[Platform]):
        """Sets the platforms for the market."""
        self.platforms = platforms

    def _schedule_initial_events(self):
        """Schedules the first evaluation event for all agents."""
        for rider in self.riders:
            initial_tick = random.randint(0, self.ticks_per_major)
            self.engine.schedule_event(
                initial_tick,
                {"action": "EVALUATE_RIDER_SEARCH_INTENT", "agent_id": rider.agent_id}
            )
        for driver in self.drivers:
            initial_tick = random.randint(0, self.ticks_per_major)
            self.engine.schedule_event(
                initial_tick,
                {"action": "EVALUATE_DRIVER_GO_ONLINE", "agent_id": driver.agent_id}
            )

    def _create_riders(self, config: Dict):
        """
        Creates the rider population.
        """
        rider_config = config['market']['rider_population']
        for i in range(config['market']['initial_riders']):
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

    def handle_event(self, event: Dict, current_tick: int):
        action = event.get("action")
        agent_id = event.get("agent_id")
        time_str = ticks_to_time_string(current_tick // self.ticks_per_major, current_tick % self.ticks_per_major, self.ticks_per_major)

        if action == "EVALUATE_DRIVER_GO_ONLINE":
            driver = next((d for d in self.drivers if d.agent_id == agent_id), None)
            if driver and driver.current_state == DriverState.OFFLINE:
                if random.random() < 0.1:  # Simplified probability
                    driver.current_state = DriverState.IDLE
                    logging.info(f"{time_str} | Driver {driver.agent_id} is now IDLE at location {driver.location}.")
            
            if driver:
                # Schedule next evaluation
                next_evaluation_tick = current_tick + 360  # Approx. 1 hour later
                self.engine.schedule_event(
                    next_evaluation_tick,
                    {"action": "EVALUATE_DRIVER_GO_ONLINE", "agent_id": agent_id}
                )

        elif action == "EVALUATE_RIDER_SEARCH_INTENT":
            rider = next((r for r in self.riders if r.agent_id == agent_id), None)
            if rider and rider.current_state == RiderState.IDLE:
                # Probability of searching in this evaluation interval
                prob = rider.rides_per_week / (7 * 24 * 4) # Assuming evaluation every 15 mins
                if random.random() < prob:
                    rider.current_state = RiderState.SEARCHING
                    rider.patience_timer = 180  # 30 minutes
                    logging.info(f"{time_str} | Rider {rider.agent_id} is now SEARCHING.")

            if rider:
                # Schedule next evaluation with some randomness
                interval = random.expovariate(1.0 / 90.0) # Average 15 mins (90 ticks)
                next_evaluation_tick = current_tick + int(interval)
                self.engine.schedule_event(
                    next_evaluation_tick,
                    {"action": "EVALUATE_RIDER_SEARCH_INTENT", "agent_id": agent_id}
                )

    def update_platform_strategies(self, day: int):
        pass

    def process_rider_searches(self, day: int, tick: int):
        time_str = ticks_to_time_string(day, tick, self.ticks_per_major)
        for rider in self.riders:
            if rider.current_state == RiderState.SEARCHING:
                order_id = f"order_{rider.agent_id}_{day}_{tick}"
                logging.info(f"{time_str} | Rider {rider.agent_id} is now SEARCHING with Order {order_id}.")
                logging.info(f"Rider {rider.agent_id} starting search for Order {order_id} from location {rider.location}.")

                chosen_platform_id = None
                if rider.has_app_a and rider.preference_score > 0:
                    chosen_platform_id = 'A'
                elif rider.has_app_b and rider.preference_score <= 0:
                    chosen_platform_id = 'B'
                elif rider.has_app_a:
                    chosen_platform_id = 'A'
                elif rider.has_app_b:
                    chosen_platform_id = 'B'

                if chosen_platform_id:
                    chosen_platform = next((p for p in self.platforms if p.platform_id == chosen_platform_id), None)
                    
                    if chosen_platform:
                        driver, status = chosen_platform.matcher.process_order(rider, 20.0, order_id)
                        if status == "MATCH_SUCCESSFUL":
                            rider.current_state = RiderState.ORDERED
                            driver.current_state = DriverState.DRIVING_TO_RIDER
                            match_info = {"driver_id": driver.agent_id, "rider_id": rider.agent_id, "platform_id": chosen_platform.platform_id, "order_id": order_id}
                            rider.match = match_info
                            driver.match = match_info
                            logging.info(f"{time_str} | Match successful for Order {order_id} (Rider {rider.agent_id} and Driver {driver.agent_id} on Platform {chosen_platform.platform_id})")
                        else:
                            rider.patience_timer -= 1
                            if rider.patience_timer <= 0:
                                rider.current_state = RiderState.ABANDONED_SEARCH
                                logging.info(f"{time_str} | Rider {rider.agent_id} ABANDONED SEARCH for Order {order_id}.")
                    else:
                        rider.patience_timer -= 1
                        if rider.patience_timer <= 0:
                            rider.current_state = RiderState.ABANDONED_SEARCH
                            logging.info(f"{time_str} | Rider {rider.agent_id} ABANDONED SEARCH for Order {order_id}.")

    def process_matcher_offers(self, day: int, tick: int):
        pass

    def process_driver_responses(self, day: int, tick: int):
        pass
    
    def update_agent_locations(self, day: int, tick: int):
        time_str = ticks_to_time_string(day, tick, self.ticks_per_major)
        current_tick = day * self.ticks_per_major + tick
        
        for driver in self.drivers:
            if driver.current_state == DriverState.DRIVING_TO_RIDER:
                # The driver object has the match info
                rider_id = driver.match['rider_id']
                rider = next((r for r in self.riders if r.agent_id == rider_id), None)

                if rider and rider.current_state == RiderState.ORDERED:
                    # Simulate instantaneous trip completion
                    new_location = (random.randint(0, 10000), random.randint(0, 10000))
                    driver.location = new_location
                    rider.location = new_location

                    driver.current_state = DriverState.IDLE
                    rider.current_state = RiderState.IDLE
                    driver.match = None
                    rider.match = None
                    
                    logging.info(f"{time_str} | Trip completed for Rider {rider.agent_id} and Driver {driver.agent_id}.")

                    # Schedule next evaluations
                    self.engine.schedule_event(
                        current_tick + 1,
                        {"action": "EVALUATE_DRIVER_GO_ONLINE", "agent_id": driver.agent_id}
                    )
                    self.engine.schedule_event(
                        current_tick + 1,
                        {"action": "EVALUATE_RIDER_SEARCH_INTENT", "agent_id": rider.agent_id}
                    )
