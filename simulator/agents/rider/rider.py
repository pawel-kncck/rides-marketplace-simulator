# simulator/agents/rider/rider.py

from enum import Enum, auto
from typing import List, Dict, Any, Tuple

# We define the possible states for a RiderAgent using an Enum.
# This makes the code clearer, safer, and easier to debug than using simple strings.
class RiderState(Enum):
    """Enumeration for the possible states of a RiderAgent."""
    IDLE = auto()               # Not looking for a ride
    SEARCHING = auto()          # Actively searching on a platform
    COMPARING_OFFERS = auto()   # Has at least one offer, checking competitor
    ORDERED = auto()            # Accepted an offer, waiting for driver
    ON_TRIP = auto()            # In a vehicle, on the way to destination
    ABANDONED_SEARCH = auto()   # Gave up searching for a ride

class RiderAgent:
    """
    Represents a rider in the simulation.

    This class holds the state and properties of a single rider agent.
    All decision-making logic will be handled by other modules to keep this class
    as a clean data container.
    """
    def __init__(
        self,
        agent_id: int,
        initial_location: Tuple[int, int],
        has_app_a: bool,
        has_app_b: bool,
        preference_score: float,
        price_sensitivity: float,
        time_sensitivity: float,
        rides_per_week: float
    ):
        """
        Initializes a RiderAgent with its core attributes and default state.
        """
        # --- Core Identity & Attributes ---
        self.agent_id: int = agent_id
        self.has_app_a: bool = has_app_a
        self.has_app_b: bool = has_app_b

        # --- Behavioral Properties ---
        # A score from -1.0 (total preference for B) to +1.0 (total for A).
        self.preference_score: float = preference_score
        self.price_sensitivity: float = price_sensitivity
        self.time_sensitivity: float = time_sensitivity
        # Determines the agent's base probability of initiating a search.
        self.rides_per_week: float = rides_per_week

        # --- Dynamic State ---
        # All riders start in the IDLE state.
        self.current_state: RiderState = RiderState.IDLE
        self.location: Tuple[int, int] = initial_location
        # The countdown timer used during a search to model patience.
        self.patience_timer: int = 0
        self.match: Dict[str, Any] = None

        # --- Incentives & Testing ---
        # A list to store any active discounts offered to this rider.
        self.active_discounts: List[Dict[str, Any]] = []
        # A dictionary to track which A/B tests the rider is enrolled in.
        # Format: {test_id: variant_id}
        self.enrolled_tests: Dict[str, str] = {}

    def __repr__(self) -> str:
        """
        Provides a developer-friendly, readable representation of the RiderAgent object,
        which is very useful for logging and debugging.
        """
        return (
            f"RiderAgent(id={self.agent_id}, "
            f"state='{self.current_state.name}', "
            f"pref_score={self.preference_score:.2f})"
        )