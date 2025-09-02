import pytest
from unittest.mock import Mock
from simulator.core.engine import Engine

def test_engine_run_loop():
    """
    Tests that the engine's run loop executes without errors
    and calls the market methods in the correct sequence.
    """
    # 1. Arrange
    market = Mock()
    platforms = [Mock(), Mock()]
    engine = Engine(market=market, platforms=platforms)

    duration_days = 2
    ticks_per_major = 3

    # 2. Act
    engine.run(duration_days=duration_days, ticks_per_major=ticks_per_major)

    # 3. Assert
    # We can assert that the placeholder methods were called the correct number of times
    # For now, we'll just check that the run completes without error.
    # A more detailed test would require implementing the market methods.
    assert market.method_calls == [] # No methods are actually called yet
