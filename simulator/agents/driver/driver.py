from enum import Enum, auto
from typing import List, Dict, Any, Tuple

class DriverState(Enum):
    """Enumeration for the possible states of a DriverAgent."""
    OFFLINE = auto()            # Not working
    IDLE = auto()               # Online and waiting for an order
    DRIVING_TO_RIDER = auto()   # Accepted an order, driving to pickup
    ON_TRIP = auto()            # With a rider, driving to destination

class DriverAgent:
    """
    Represents a driver in the simulation.
    """
    def __init__(
        self,
        agent_id: int,
        initial_location: Tuple[int, int],
        is_exclusive: bool,
        preference_score: float,
        price_sensitivity: float,
        eta_sensitivity: float
    ):
        """
        Initializes a DriverAgent with its core attributes and default state.
        """
        # --- Core Identity & Attributes ---
        self.agent_id: int = agent_id
        self.is_exclusive: bool = is_exclusive

        # --- Behavioral Properties ---
        self.preference_score: float = preference_score
        self.price_sensitivity: float = price_sensitivity
        self.eta_sensitivity: float = eta_sensitivity

        # --- Dynamic State ---
        self.current_state: DriverState = DriverState.OFFLINE
        self.location: Tuple[int, int] = initial_location
        self.idle_timer: int = 0

    def __repr__(self) -> str:
        """
        Provides a developer-friendly, readable representation of the DriverAgent object.
        """
        return (
            f"DriverAgent(id={self.agent_id}, "
            f"state='{self.current_state.name}', "
            f"pref_score={self.preference_score:.2f})"
        )
