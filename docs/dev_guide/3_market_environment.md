# Developer Guide: The Market Environment

This document explains how the simulation's "world" is created and managed. It covers the `Market` class, which is responsible for creating the agent population, and the `HexGrid` class, which represents the city's physical space.

-----

## 1\. Market Initialization (`market/market.py`)

The `Market` class is the central container for the simulation's state. When a `Market` object is created, it immediately proceeds to build the world and populate it with agents based on the provided configuration file.

### **Step 1: Initializing the Container**

The `__init__` method sets up the main components of the market:

1.  An instance of `HexGrid` is created, using the `grid_resolution` from the config.
2.  Empty lists are created to hold the `platforms`, `riders`, and `drivers`.
3.  The private methods `_create_riders` and `_create_drivers` are called to generate the agent populations.

<!-- end list -->

```python
# in simulator/market/market.py
def __init__(self, config: Dict):
    self.grid = HexGrid(config['market']['grid_resolution'])
    self.platforms: List[Platform] = []
    self.riders: List[RiderAgent] = []
    self.drivers: List[DriverAgent] = []

    self._create_riders(config)
    self._create_drivers(config)
```

### **Step 2: Creating the Rider Population**

The `_create_riders` method iterates from 0 to the `initial_riders` count specified in the config. In each iteration, it creates a single `RiderAgent` with unique properties:

  * **App Ownership:** It uses `random.random()` to determine which app(s) the rider has, based on the percentages (`pct_with_app_a_only`, `pct_with_app_b_only`) from the config.
  * **Behavioral Traits:** Properties like `preference_score`, `price_sensitivity`, and `time_sensitivity` are set by drawing a random value from a normal distribution (`random.normalvariate`), using the `[mean, std_dev]` pairs provided in the config (e.g., `price_sensitivity_dist`).

Finally, each new `RiderAgent` is appended to the `self.riders` list and added to the `HexGrid`.

### **Step 3: Creating the Driver Population**

The `_create_drivers` method works similarly. It iterates up to the `initial_drivers` count and creates a `DriverAgent` in each loop.

  * **Exclusivity:** The `is_exclusive` boolean property is determined by comparing `random.random()` to the `pct_exclusive` value in the config.
  * **Behavioral Traits:** `preference_score`, `price_sensitivity`, and `eta_sensitivity` are drawn from their respective normal distributions defined in the config.

Each new `DriverAgent` is then added to the `self.drivers` list and the `HexGrid`.

-----

## 2\. The Spatial Grid (`market/space.py`)

The `HexGrid` class provides an efficient way to organize agents in a 2D space, making proximity-based queries (like finding the nearest driver) much faster. It is not a true hexagonal grid but simulates one by discretizing the space into square cells.

### **Core Structure**

The grid is implemented as a Python dictionary (`_grid`) where:

  * **Keys** are tuples representing a cell's ID, e.g., `(10, 25)`.
  * **Values** are lists containing all the agent objects currently located within that cell.

### **Key Methods**

  * **`get_cell_id(location)`**: This method converts a continuous coordinate location (e.g., `(1234, 5678)`) into a discrete cell ID. It does this through simple integer division of the coordinates by the grid's `resolution`.

    ```python
    # in simulator/market/space.py
    def get_cell_id(self, location: Tuple[int, int]) -> Tuple[int, int]:
        return (
            int(location[0] / self.grid_resolution),
            int(location[1] / self.grid_resolution),
        )
    ```

  * **`add_agent(agent)`**: To add an agent to the grid, this method first determines the agent's `cell_id` using `get_cell_id`. It then appends the agent to the list associated with that key in the `_grid` dictionary. If the key does not yet exist, it initializes an empty list first.

  * **`get_agents_in_cell(cell_id)`**: This method simply retrieves and returns the list of agents for a given `cell_id`. It uses `.get()` with a default empty list `[]` to safely handle queries for empty cells.