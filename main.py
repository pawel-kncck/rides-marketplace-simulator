import argparse
import yaml
from simulator.market.market import Market
from simulator.platform.matcher import Matcher
from simulator.platform.platform import Platform
from simulator.core.engine import Engine

def main():
    """Main entry point for the simulator."""
    parser = argparse.ArgumentParser(description="Ride-hailing simulator.")
    parser.add_argument('--config', type=str, required=True, help='Path to the configuration file.')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    market = Market(config)
    
    # Create platforms based on the config file
    platforms = []
    for platform_id, platform_config in config['platforms'].items():
        matcher_config = platform_config['matcher']
        matcher = Matcher(
            grid=market.grid,
            max_order_tries=matcher_config['max_order_tries']
        )
        platform = Platform(platform_id, matcher)
        platforms.append(platform)

    market.set_platforms(platforms)
    engine = Engine(market, platforms)

    engine.run(
        duration_days=config['simulation']['duration_days'],
        ticks_per_major=config['simulation']['ticks_per_major']
    )

if __name__ == "__main__":
    main()
