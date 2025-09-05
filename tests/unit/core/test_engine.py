import pytest
from unittest.mock import Mock, call
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
    expected_calls = []
    for day in range(duration_days):
        expected_calls.extend([
            call.update_platform_strategies(),
            call.update_driver_go_online_decisions(),
            call.update_rider_search_intent()
        ])
        for tick in range(ticks_per_major):
            expected_calls.extend([
                call.process_rider_searches(),
                call.process_matcher_offers(),
                call.process_driver_responses(),
                call.update_agent_locations()
            ])
    
    assert market.method_calls == expected_calls
