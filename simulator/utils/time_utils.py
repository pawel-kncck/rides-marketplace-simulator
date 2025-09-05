# in simulator/utils/time_utils.py
def ticks_to_time_string(day: int, tick: int, ticks_per_major: int, minor_tick_secs: int = 10) -> str:
    """Converts simulation ticks to a formatted time string."""
    total_seconds = (tick * minor_tick_secs) + ((day * 24 * 3600) / (3600 / (ticks_per_major / 360)))

    hours = int((total_seconds % 86400) / 3600)
    minutes = int((total_seconds % 3600) / 60)
    seconds = int(total_seconds % 60)

    return f"Day {day}, {hours:02d}:{minutes:02d}:{seconds:02d}"
