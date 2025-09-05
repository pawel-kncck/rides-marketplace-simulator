# simulator/platform/platform.py
from simulator.platform.matcher import Matcher

class Platform:
    """
    Represents a ride-hailing platform.
    """
    def __init__(self, platform_id: str, matcher: Matcher):
        """
        Initializes a Platform.

        Args:
            platform_id: The unique identifier for the platform (e.g., 'A').
            matcher: The matcher object for this platform.
        """
        self.platform_id = platform_id
        self.matcher = matcher

    def __repr__(self) -> str:
        return f"Platform(id={self.platform_id})"
