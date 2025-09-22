import time
from typing import List
from collections import defaultdict

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
        self.event_schedule = defaultdict(list)
        self.current_tick = 0

    def schedule_event(self, tick, event):
        self.event_schedule[tick].append(event)

    def run(self, duration_days: int, ticks_per_major: int):
        """
        Runs the simulation.

        Args:
            duration_days: The duration of the simulation in days.
            ticks_per_major: The number of minor ticks per major tick.
        """
        total_ticks = duration_days * ticks_per_major
        for self.current_tick in range(total_ticks):
            day = self.current_tick // ticks_per_major
            tick_in_day = self.current_tick % ticks_per_major

            # --- Event-Driven Logic ---
            events = self.event_schedule.get(self.current_tick, [])
            for event in events:
                self.market.handle_event(event, self.current_tick)

            # --- Minor Tick Logic (remains the same) ---
            self.market.process_rider_searches(day, tick_in_day)
            self.market.process_matcher_offers(day, tick_in_day)
            self.market.process_driver_responses(day, tick_in_day)
            self.market.update_agent_locations(day, tick_in_day)

            # --- Major Tick Logic (simplified) ---
            if self.current_tick % ticks_per_major == 0:
                self.market.update_platform_strategies(day)
                print(f"Day {day + 1} complete.")
                time.sleep(0.1)