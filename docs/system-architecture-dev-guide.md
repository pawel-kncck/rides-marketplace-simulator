# System Architecture & Developer Guide

## 1\. Introduction

This document provides a technical deep-dive into the architecture and inner workings of the High-Fidelity Ride-Hailing Simulator. It is intended for developers and data scientists who will be maintaining, calibrating, or extending the model.

It assumes the reader is familiar with the project's goals, as outlined in the `README.md`.

-----

## 2\. Architecture Overview

The simulator follows a modular, agent-based architecture designed for clarity, testability, and extensibility. The core design principle is a strict separation of concerns between the simulation engine, the market environment, the platform's "backend," and the agents' individual "brains."

The project is organized into four main source directories:

  * **`core`**: Manages the simulation's clock and main execution loop. It is the heartbeat of the system.
  * **`market`**: Represents the environment. It holds all the agents and the spatial grid they inhabit.
  * **`agents`**: Contains the logic and state for `RiderAgent` and `DriverAgent` classes.
  * **`platform`**: Contains the logic for the ride-hailing platforms, including the matching algorithm and the incentive framework.

-----

## 3\. Core Module Deep Dive

### **The Engine (`engine.py`)**

The Engine drives the simulation forward in time using a **two-level clock**.

  * **Major Ticks:** The outer loop of the simulation (e.g., one hour). Strategic decisions are typically made at this level:
      * Platforms launch or end `Test` campaigns.
      * Drivers decide whether to go online for a "shift."
      * The probability check for riders to initiate a new ride search occurs.
  * **Minor Ticks:** The inner loop (e.g., every 10 seconds). This is where the real-time, operational logic happens:
      * Rider agents who decided to search send requests to the Matcher.
      * The Matcher sends `Order Try` objects to drivers.
      * Drivers accept or reject offers.
      * Agent locations are updated.

<!-- end list -->

```pseudocode
function Engine.run():
  for major_tick in duration:
    # --- Major Tick Logic ---
    market.update_platform_strategies()
    market.update_driver_go_online_decisions()
    market.update_rider_search_intent()

    for minor_tick in ticks_per_major_tick:
      # --- Minor Tick Logic ---
      market.process_rider_searches()
      market.process_matcher_offers()
      market.process_driver_responses()
      market.update_agent_locations()
    log(f"Major Tick {major_tick} complete")
```

-----

## 4\. Market Module Deep Dive

### **The Market (`market.py`)**

The Market is the primary container for the simulation state. Its main responsibilities are:

  * Initializing the agent population based on the `config.yaml` file.
  * Holding the lists of all `RiderAgent`, `DriverAgent`, and `Platform` objects.
  * Exposing methods for the `Engine` to call to advance the state of the world.

### **The Space (`space.py`)**

The Space module implements the **hexagonal grid** that represents the city.

  * **Functionality:** It provides fast, efficient spatial queries. The key function is for the Matcher to find the N nearest available drivers to a given rider's location.
  * **Agent Location:** Each agent has a `cell_id` property, which is used for these fast lookups.

-----

## 5\. Agents Module Deep Dive

### **Rider Agent (`rider/`)**

The rider's goal is to maximize personal utility.

  * **State Machine:** Governed by the `RiderState` enum (`IDLE`, `SEARCHING`, `COMPARING_OFFERS`, etc.). Transitions are event-driven:
      * `IDLE` -\> `SEARCHING` is a probabilistic event based on the agent's `rides_per_week` and any "session uplift" from discounts.
      * `SEARCHING` -\> `ABANDONED_SEARCH` occurs if the agent's `patience_timer` (measured in Minor Ticks) expires.
  * **Utility Function:** The core of the rider's decision-making when comparing offers is the utility score:
    > `Utility = (-w_price * EffectivePrice) + (-w_eta * ETA) + (w_habit * PreferenceScore)`
  * **Preference Score:** A float from -1.0 to +1.0 that evolves slowly with each positive or negative platform experience, modeling **market share inertia**.

### **Driver Agent (`driver/`)**

The driver's goal is to maximize earnings.

  * **State Machine:** Governed by the `DriverState` enum (`OFFLINE`, `IDLE`, `DRIVING_TO_RIDER`, `ON_TRIP`).
  * **Decision Logic:** Drivers make several hierarchical decisions:
    1.  **Go Online:** Based on the `PerceivedValue` of available `BonusQuest` objects.
    2.  **Platform Choice (Multi-homing):** The `preference_score` (driven by `earnings_memory`) determines which app to check first. The `idle_timer` determines when to check the competitor if no rides are forthcoming.
    3.  **Acceptance Decision:** When receiving an `Order Try`, the driver calculates a **Profitability Score** to decide whether to accept:
        > `Profitability = (w_price * OrderPrice) - (w_eta * ETA)`

-----

## 6\. Platform Module Deep Dive

### **The Matcher (`matcher.py`)**

The Matcher is the "backend" of a platform, connecting riders and drivers. It follows a precise **Order Try** flow.

1.  The Matcher receives an `Order` from a rider.
2.  It queries the `Space` to find the N nearest `IDLE` drivers.
3.  It creates an `Order Try` (a single offer to a single driver) and sends it to the nearest driver.
4.  If the try is rejected or times out, a new `Order Try` is created and sent to the next-nearest driver.
5.  This continues until the `max_order_tries` limit is reached (Order `UNFULFILLED`) or a driver accepts (Order `ACTIVE`).

### **The `Test` Framework (`testing/`, `incentives/`)**

This framework manages all A/B testing of incentives, following the **Scenario C** architecture.

  * **`Test` Object:** A generic container that defines the target user type, enrollment criteria, and variant splits (control vs. treatment).
  * **`Campaign` Objects (`RiderDiscount`, `BonusQuest`):** Specialized classes that define the actual incentive for a specific test variant. They are responsible for their own logic (e.g., a `BonusQuest` tracks a driver's progress towards their goal).

-----

## 7\. Development Process

### **Testing**

All new code must be accompanied by tests.

  * **Unit Tests:** New logic functions (e.g., a new bonus calculation, a change to the utility function) must have dedicated unit tests that check their outputs with fixed inputs.
  * **E2E Tests:** Major new features should be accompanied by a new E2E test case. This involves creating a new config file that isolates the feature and generating a "golden master" output file against which future runs can be compared.

### **Logging**

The primary tool for debugging emergent behavior is the structured event log.

  * **Adding Events:** When adding new logic, emit log events at key decision points. Use the standard structured format:
    ```json
    {
      "tick": 1205,
      "agent_id": "driver_78",
      "event": "ORDER_TRY_REJECTED",
      "details": {
        "order_id": "order_abc",
        "profitability_score": -2.5,
        "acceptance_threshold": -1.0
      }
    }
    ```
  * **Debugging:** To debug an issue, filter the main event log for a specific `agent_id` or `order_id` to reconstruct its complete history—its "journal."