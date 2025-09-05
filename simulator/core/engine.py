from typing import List

class Engine:
    """
    The core simulation engine.
    """
    def __init__(self, market, platforms: List):
        """
        Initializes the Engine.

        Args:
            market: The market object.
            platforms: A list of platform objects.
        """
        self.market = market
        self.platforms = platforms

    def run(self, duration_days: int, ticks_per_major: int):
        """
        Runs the simulation.

        Args:
            duration_days: The duration of the simulation in days.
            ticks_per_major: The number of minor ticks per major tick.
        """
        for day in range(duration_days):
            # --- Major Tick Logic ---
            self.market.update_platform_strategies()
            self.market.update_driver_go_online_decisions()
            self.market.update_rider_search_intent()

            for tick in range(ticks_per_major):
                # --- Minor Tick Logic ---
                self.market.process_rider_searches()
                self.market.process_matcher_offers()
                self.market.process_driver_responses()
                self.market.update_agent_locations()
                pass

            print(f"Day {day + 1} complete.")