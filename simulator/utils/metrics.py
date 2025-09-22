# simulator/utils/metrics.py

class SimulationMetrics:
    def __init__(self):
        self.online_drivers = set()
        self.active_drivers = set()
        self.searching_riders = set()
        self.riders_with_completed_trips = set()
        self.total_completed_trips = 0

    def track_driver_online(self, driver_id: int):
        self.online_drivers.add(driver_id)

    def track_rider_search(self, rider_id: int):
        self.searching_riders.add(rider_id)

    def track_completed_trip(self, driver_id: int, rider_id: int):
        self.total_completed_trips += 1
        self.active_drivers.add(driver_id)
        self.riders_with_completed_trips.add(rider_id)

    def print_summary(self):
        print("\n--- Simulation Summary ---")
        print(f"Unique drivers who went online: {len(self.online_drivers)}")
        print(f"Unique active drivers (completed a trip): {len(self.active_drivers)}")
        print(f"Unique riders who searched: {len(self.searching_riders)}")
        print(f"Unique riders who completed a trip: {len(self.riders_with_completed_trips)}")
        print(f"Total completed trips: {self.total_completed_trips}")
        print("------------------------\n")
