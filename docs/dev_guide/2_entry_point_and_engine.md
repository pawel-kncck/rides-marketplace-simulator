# Developer Guide: Entry Point & Engine

This document provides a step-by-step guide to the simulator's startup process (`main.py`) and its core execution loop (`core/engine.py`).

-----

## 1\. The Entry Point: `main.py`

Every simulation run begins with the execution of `main.py`. This script is responsible for setting up the entire simulation environment based on a configuration file.

### **Step 1: Parsing Configuration**

The script first uses Python's `argparse` library to read a command-line argument, `--config`, which specifies the path to a `.yaml` configuration file. This file contains all the necessary parameters for the simulation run.

```python
# in main.py
parser = argparse.ArgumentParser(description="Ride-hailing simulator.")
parser.add_argument('--config', type=str, required=True, help='Path to the configuration file.')
args = parser.parse_args()

with open(args.config, 'r') as f:
    config = yaml.safe_load(f)
```

### **Step 2: Initializing the World**

Once the configuration is loaded, the script initializes the core components of the simulation in a specific order:

1.  **The `Market` is created.** This object serves as the container for all agents and the spatial grid. The agent populations (riders and drivers) are generated during its initialization.
2.  **The `Platforms` are created.** The script iterates through the `platforms` section of the config file. For each platform, it creates a `Matcher` instance and then a `Platform` instance, passing the `Matcher` to it.
3.  **The `Engine` is created.** Finally, the `Engine` is initialized, and the `Market` and list of `Platforms` are passed to it.

<!-- end list -->

```python
# in main.py
market = Market(config)

platforms = []
for platform_id, platform_config in config['platforms'].items():
    # ... (matcher creation)
    platform = Platform(platform_id, matcher)
    platforms.append(platform)

market.set_platforms(platforms)
engine = Engine(market, platforms)
```

### **Step 3: Launching the Simulation**

With all components initialized and linked, the `engine.run()` method is called. This action starts the main simulation loop and begins the progression of time within the simulated world.

```python
# in main.py
engine.run(
    duration_days=config['simulation']['duration_days'],
    ticks_per_major=config['simulation']['ticks_per_major']
)
```

-----

## 2\. The Simulation Engine: `core/engine.py`

The `Engine` is the "heartbeat" of the simulator. It uses a **two-level clock** to manage the flow of time and orchestrate the sequence of events.

### **The Two-Level Clock**

The `run` method consists of two nested loops:

  * **Major Ticks (Outer Loop):** Represents a large, strategic time step (e.g., an hour).
  * **Minor Ticks (Inner Loop):** Represents a small, operational time step (e.g., 10 seconds).

This structure allows the simulator to efficiently model both long-term strategic decisions and near-instantaneous market dynamics.

```python
# in simulator/core/engine.py
def run(self, duration_days: int, ticks_per_major: int):
    for day in range(duration_days):
        # --- Major Tick Logic ---
        ...
        for tick in range(ticks_per_major):
            # --- Minor Tick Logic ---
            ...
```

### **Major Tick Logic**

At the beginning of each major tick, the engine calls a series of methods on the `Market` object to handle less frequent, higher-level decisions:

1.  `market.update_platform_strategies(day)`: (Currently a placeholder) Intended for updating platform-level strategies.
2.  `market.update_driver_go_online_decisions(day)`: Simulates drivers deciding to come online or go offline for a "shift".
3.  `market.update_rider_search_intent(day)`: Determines if any idle riders will begin searching for a ride during this major tick.

### **Minor Tick Logic**

For every minor tick within the major tick, a different set of methods is called to process the real-time interactions of the marketplace:

1.  `market.process_rider_searches(day, tick)`: Riders who are in the `SEARCHING` state choose a platform and request a ride.
2.  `market.process_matcher_offers(day, tick)`: (Currently a placeholder) Intended for the `Matcher` to process offers to drivers.
3.  `market.process_driver_responses(day, tick)`: (Currently a placeholder) Intended for drivers to accept or reject the offers they receive.
4.  `market.update_agent_locations(day, tick)`: Simulates the movement of agents, including the completion of trips.