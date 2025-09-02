import argparse
import yaml
from simulator.market.market import Market
from simulator.platform.matcher import Matcher
from simulator.core.engine import Engine

def main():
    """Main entry point for the simulator."""
    parser = argparse.ArgumentParser(description="Ride-hailing simulator.")
    parser.add_argument('--config', type=str, required=True, help='Path to the configuration file.')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    market = Market(config)
    # For now, we'll use a single matcher for all platforms
    matcher = Matcher(market.grid)
    platforms = [] # Placeholder for platform objects

    engine = Engine(market, platforms)

    engine.run(
        duration_days=config['simulation']['duration_days'],
        ticks_per_major=config['simulation']['ticks_per_major']
    )

if __name__ == "__main__":
    main()
