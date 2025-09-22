# Developer Guide: The Driver Agent

This document provides a deep dive into the `DriverAgent`. We will methodically analyze its structure, its role within the simulation, and the logic that dictates its behavior. The goal is to provide developers with a clear and comprehensive understanding, enabling them to extend the agent's logic or identify areas for improvement.

Similar to the `RiderAgent`, the `DriverAgent` class in `simulator/agents/driver/driver.py` is primarily a **data container**. The logic that governs its state transitions and decisions is located in other modules, specifically `simulator/market/market.py` and `simulator/platform/matcher.py`.

-----

## 1\. Core Components: The Anatomy of a Driver

We will start by examining the `DriverAgent`'s definition in `simulator/agents/driver/driver.py`.

### **The `DriverState` Enum: A Driver's Work Cycle**

The driver's operational cycle is represented by a state machine. The `DriverState` enum defines the four possible states a driver can be in:

```python
# in simulator/agents/driver/driver.py
class DriverState(Enum):
    """Enumeration for the possible states of a DriverAgent."""
    OFFLINE = auto()            # Not working
    IDLE = auto()               # Online and waiting for an order
    DRIVING_TO_RIDER = auto()   # Accepted an order, driving to pickup
    ON_TRIP = auto()            # With a rider, driving to destination
```

### **The `DriverAgent` Class: Attributes and Properties**

When a `DriverAgent` is created by the `Market`, it is initialized with a set of properties that define its professional profile and economic behavior.

Let's inspect the parameters of the `__init__` method:

  * **Core Identity & Attributes**: These define the driver's relationship with the platforms.

      * `agent_id`: A unique integer identifier.
      * `is_exclusive`: A boolean indicating whether the driver works for only one platform or is a "multi-homer."

  * **Behavioral Properties**: These attributes are the core drivers of a driver's economic decisions.

      * `preference_score`: Similar to the rider, this float models a driver's preference for platform A (positive) or B (negative). (Note: This is not yet used in the core logic).
      * `price_sensitivity`: A float that determines how much a high fare **positively** influences the driver's decision to accept an offer.
      * `eta_sensitivity`: A float that determines how much the unpaid travel time to a rider **negatively** influences the acceptance decision.

  * **Dynamic State**: These attributes change as the driver interacts with the market.

      * `current_state`: Initialized to `DriverState.OFFLINE`, this tracks the agent's current status.
      * `location`: A tuple `(x, y)` for the driver's position.
      * `idle_timer`: A counter (in ticks) for how long a driver has been `IDLE`. Initialized to `0`.

-----

## 2\. Decision-Making Logic: A Step-by-Step Walkthrough

We will now trace the key decisions a driver makes during the simulation, from coming online to accepting a ride.

### **Step 1: The Decision to Go Online or Offline**

This logic is executed once per **Major Tick** in the `update_driver_go_online_decisions` method within `simulator/market/market.py`. The current implementation is a simple probabilistic model.

1.  **Going Online**: For every driver who is `OFFLINE`, a random check is performed. There is a 10% chance each major tick that they will switch their state to `IDLE`.

    ```python
    # in simulator/market/market.py
    if driver.current_state == DriverState.OFFLINE:
        if random.random() < 0.1:
            driver.current_state = DriverState.IDLE
            logging.info(f"{time_str} | Driver {driver.agent_id} is now IDLE.")
    ```

2.  **Going Offline**: Similarly, for every driver who is currently `IDLE`, there is a 5% chance they will switch back to `OFFLINE`.

    ```python
    # in simulator/market/market.py
    elif driver.current_state == DriverState.IDLE:
        if random.random() < 0.05:
            driver.current_state = DriverState.OFFLINE
            logging.info(f"{time_str} | Driver {driver.agent_id} is now OFFLINE.")
    ```

### **Step 2: The Decision to Accept an Offer**

This is the most critical economic decision the driver makes. It occurs during a **Minor Tick** within the `process_order` method of the `Matcher` (`simulator/platform/matcher.py`).

1.  **Receiving an Offer**: The `Matcher` finds an `IDLE` driver and presents them with a potential ride, which includes a `fare` and an `eta_to_rider`.

2.  **Calculating Profitability**: The `Matcher` then calls the `calculate_profitability_score` function from `simulator/agents/driver/logic.py` to evaluate how "good" the offer is for that specific driver.

    ```python
    # in simulator/platform/matcher.py
    profitability_score = calculate_profitability_score(driver, fare, eta_to_rider)
    ```

    Let's look at the calculation itself. The function balances the reward (fare) against the cost (unpaid travel time):

    ```python
    # in simulator/agents/driver/logic.py
    def calculate_profitability_score(
        driver: DriverAgent,
        fare: float,
        eta_to_rider: int
    ) -> float:
        score = (
            (driver.price_sensitivity * fare)
            - (driver.eta_sensitivity * eta_to_rider)
        )
        return score
    ```

      * `(driver.price_sensitivity * fare)`: This term is the **positive** component. A higher fare or a more price-sensitive driver increases the score.
      * `- (driver.eta_sensitivity * eta_to_rider)`: This term is the **negative** component. A longer travel time to the rider or a driver more sensitive to unpaid time decreases the score.

3.  **The Acceptance Threshold**: The decision to accept is based on a simple threshold. If the calculated score is positive, the ride is profitable enough to accept.

    ```python
    # in simulator/platform/matcher.py
    if profitability_score > 0:
        driver.current_state = DriverState.DRIVING_TO_RIDER
        rider.current_state = RiderState.ORDERED
        return driver, "MATCH_SUCCESSFUL"
    ```

    If the driver accepts, both their state and the rider's state are updated, and the match is considered successful. If the score is not greater than 0, the `Matcher` will move on to the next available driver.

-----

## 3\. Analysis and Potential Logical Flaws

This detailed review of the `DriverAgent`'s logic highlights several areas of simplification that are important for developers to recognize:

1.  **Simplistic "Go Online" Logic**: The decision to start or stop working is purely random, based on fixed probabilities (`0.1` and `0.05`). A more sophisticated model would have drivers make this decision based on factors like the time of day, perceived demand, or active incentive campaigns (e.g., bonuses).
2.  **Hardcoded Acceptance Threshold**: The driver accepts any ride with a `profitability_score > 0`. This threshold could be a configurable behavioral attribute of the driver (e.g., some drivers might only accept rides with a score \> 2.0).
3.  **No Multi-Homing Logic**: While drivers have an `is_exclusive` attribute and a `preference_score`, there is currently no logic that uses these properties. A non-exclusive driver does not choose which platform to be active on or switch between apps if they have been idle for a long time. The platform they receive an offer from is determined entirely by the rider's choice.
4.  **Static Behavioral Traits**: Similar to the rider, the driver's `price_sensitivity`, `eta_sensitivity`, and `preference_score` are set at initialization and never change. A more dynamic simulation would have these traits (especially the preference score) evolve based on the driver's earnings and experiences on each platform.