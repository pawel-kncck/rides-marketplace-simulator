# Developer Guide: The Rider Agent

This document provides an in-depth analysis of the `RiderAgent`. Its purpose is to detail the agent's structure, its behavioral logic, and how its state is managed throughout the simulation. We will proceed step-by-step to build a clear picture of the implementation, which is essential for identifying potential logical flaws or areas for future improvement.

It is critical to understand that the `RiderAgent` class in `simulator/agents/rider/rider.py` is primarily a **data container**. The logic that reads its properties and triggers state changes is located in other modules, most notably `simulator/market/market.py` and `simulator/agents/rider/logic.py`.

-----

## 1\. Core Components: The Anatomy of a Rider

Let's begin by examining the definition of the `RiderAgent` in `simulator/agents/rider/rider.py`.

### **The `RiderState` Enum: A Rider's Lifecycle**

A rider's journey through the simulation is defined by a state machine. The `RiderState` enum provides a clear and safe way to represent every possible state:

```python
# in simulator/agents/rider/rider.py
class RiderState(Enum):
    """Enumeration for the possible states of a RiderAgent."""
    IDLE = auto()               # Not looking for a ride
    SEARCHING = auto()          # Actively searching on a platform
    COMPARING_OFFERS = auto()   # Has at least one offer, checking competitor
    ORDERED = auto()            # Accepted an offer, waiting for driver
    ON_TRIP = auto()            # In a vehicle, on the way to destination
    ABANDONED_SEARCH = auto()   # Gave up searching for a ride
```

### **The `RiderAgent` Class: Attributes and Properties**

When the `Market` creates a `RiderAgent`, it initializes it with a set of properties that define its identity and behavior. These are set once and, for the most part, do not change during the simulation.

Let's break down the `__init__` method's parameters:

  * **Behavioral Properties**: These attributes are the core drivers of a rider's decisions.

      * `preference_score`: A float ranging from **-1.0 (total preference for platform B)** to **+1.0 (total preference for platform A)**. This is a crucial variable for modeling brand loyalty and market inertia.
      * `price_sensitivity` & `time_sensitivity`: These floats determine how strongly price and ETA will negatively affect a rider's evaluation of an offer.
      * `rides_per_week`: This float represents the agent's baseline demand and is the key input for determining when they start looking for a ride.

  * **Dynamic State**: These attributes are designed to change as the simulation progresses.

      * `current_state`: Initialized to `RiderState.IDLE`, this tracks the agent's position in the state machine.
      * `patience_timer`: A countdown timer (in ticks) that models how long a rider will wait before abandoning their search. It is initialized to `0`.

-----

## 2\. Decision-Making Logic: A Step-by-Step Walkthrough

Now, we will trace the journey of a rider from `IDLE` to completing or abandoning a trip, referencing the code that executes each step.

### **Step 1: The Decision to Search for a Ride**

This logic resides in `simulator/market/market.py` and is executed once per **Major Tick**.

1.  **Condition Check**: The code iterates through all riders and only considers those in the `IDLE` state.

2.  **Probability Calculation**: For each `IDLE` rider, a probability of searching is calculated. The logic converts their weekly ride frequency into an hourly probability.

    ```python
    # in simulator/market/market.py, inside update_rider_search_intent
    prob = rider.rides_per_week / (7 * 24)
    if random.random() < prob:
        # ... transition to SEARCHING
    ```

3.  **State Transition**: If the random check passes, two crucial state changes occur:

      * The rider's state is updated: `rider.current_state = RiderState.SEARCHING`.
      * The rider's `patience_timer` is activated with a hardcoded value: `rider.patience_timer = 180`.

### **Step 2: Choosing a Platform to Search On**

This logic is found in `simulator/market/market.py` and is executed for every `SEARCHING` rider during each **Minor Tick**.

The platform choice logic is a simple, deterministic set of rules based on app ownership and the static `preference_score`.

```python
# in simulator/market/market.py, inside process_rider_searches
if rider.has_app_a and rider.preference_score > 0:
    chosen_platform_id = 'A'
elif rider.has_app_b and rider.preference_score <= 0:
    chosen_platform_id = 'B'
elif rider.has_app_a:
    chosen_platform_id = 'A'
elif rider.has_app_b:
    chosen_platform_id = 'B'
```

After this block, the chosen platform's `matcher.process_order` method is called, which attempts to find a driver for the rider.

### **Step 3: The Patience Timer and Search Abandonment**

If the `matcher.process_order` call in the previous step does not result in a successful match (`status != "MATCH_SUCCESSFUL"`), the rider's patience begins to wane.

```python
# in simulator/market/market.py, inside process_rider_searches
if not match_successful:
    rider.patience_timer -= 1
    if rider.patience_timer <= 0:
        rider.current_state = RiderState.ABANDONED_SEARCH
        logging.info(f"{time_str} | Rider {rider.agent_id} ABANDONED SEARCH.")
```

This logic decrements the timer on every unsuccessful minor tick. If the timer reaches zero, the rider's state is set to `ABANDONED_SEARCH`, and they stop looking for a ride for this session.

### **Step 4: The (Currently Unused) Utility Function**

The file `simulator/agents/rider/logic.py` contains the economic core of the rider's decision-making, the `calculate_utility` function. **It is crucial to note that this function is not currently called anywhere in the main simulation loop.** It exists with corresponding unit tests but is not yet integrated.

The function's purpose is to calculate a single numerical score representing how "good" an offer is for a particular rider.

```python
# in simulator/agents/rider/logic.py
def calculate_utility(
    rider: RiderAgent,
    price: float,
    eta: int,
    preference_score_weight: float
) -> float:
    utility = (
        (-rider.price_sensitivity * price)
        + (-rider.time_sensitivity * eta)
        + (preference_score_weight * rider.preference_score)
    )
    return utility
```

  * `(-rider.price_sensitivity * price)`: This term calculates the "pain" from the price. The higher the price or the rider's sensitivity, the more negative this term becomes.
  * `(-rider.time_sensitivity * eta)`: Similarly, this calculates the "pain" from the wait time.
  * `(preference_score_weight * rider.preference_score)`: This term introduces the rider's bias. A positive score for platform A will increase the utility of an offer from that platform.

-----

## 3\. Analysis and Potential Logical Flaws

This deliberate, step-by-step review uncovers several important simplifications and areas where the model's logic could be extended or refined:

1.  **No True Offer Comparison**: The most significant logical gap is that the `calculate_utility` function is never used. A rider with both apps (`multi-homer`) makes a deterministic choice based on `preference_score` and never gets to compare competing offers on price and ETA.
2.  **Static Behavioral Traits**: The `preference_score` is a powerful concept, but it is static. It's set at the beginning of the simulation and never changes. A more dynamic model would have this score evolve based on the rider's experiences (e.g., a successful, quick, and cheap ride should slightly increase the preference for that platform).
3.  **Hardcoded Patience**: The `patience_timer` is always set to `180` ticks. This is a missed opportunity for heterogeneity. A more realistic simulation would draw this value from a distribution in the config, just like the sensitivity parameters.
4.  **No Feedback from Abandonment**: When a rider's search is abandoned, it is a significant negative event. Currently, this only results in a log entry. There is no feedback mechanism; it does not decrease their `preference_score` for the platform they were searching on, nor does it make them less likely to search again soon.