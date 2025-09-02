This is designed to be a "living document"—a single source of truth that should be updated as the simulator evolves. It provides a scannable overview of every component, its status, and where to find it in the configuration and code.

-----

# Feature & Parameter Reference

This document serves as a central registry for all features, mechanics, and configurable parameters within the High-Fidelity Ride-Hailing Simulator. Its purpose is to provide a quick reference for what the simulator is capable of, what is currently being built, and where to find the relevant settings and code.

### Status Legend

  * `[IMPLEMENTED ✅]` - The feature is complete and tested.
  * `[IN DEVELOPMENT 🚧]` - The feature is actively being built.
  * `[PLANNED 📝]` - The feature is designed but not yet implemented.

-----

## Core & Market

| Feature Name | Description | Status | YAML Parameter(s) | Code Location(s) |
| :--- | :--- | :--- | :--- | :--- |
| **Simulation Engine** | The core discrete-time clock that advances the simulation through Major and Minor Ticks. | `[IMPLEMENTED ✅]` | `simulation.duration_days` | `simulator/core/engine.py` |
| **Reproducibility** | Ensures that a simulation with the same configuration and seed produces identical results. | `[IMPLEMENTED ✅]` | `simulation.random_seed` | `simulator/core/engine.py` |
| **Multi-Currency** | Supports a local currency for simulation and EUR for reporting, using a fixed exchange rate. | `[IMPLEMENTED ✅]` | `market.local_currency`\<br\>`market.eur_fx_rate` | `simulator/utils/currency.py` |
| **Hexagonal Grid** | The spatial environment for the simulation, providing efficient proximity queries for the Matcher. | `[IN DEVELOPMENT 🚧]` | `market.grid_resolution` | `simulator/market/space.py` |

-----

## Rider Agent

| Feature Name | Description | Status | YAML Parameter(s) | Code Location(s) |
| :--- | :--- | :--- | :--- | :--- |
| **Base Agent State** | Core properties of a rider, including app ownership and behavioral sensitivities. | `[IMPLEMENTED ✅]` | `market.rider_population.*` | `simulator/agents/rider/rider.py` |
| **State Machine**| Manages the rider's current state (`IDLE`, `SEARCHING`, `ON_TRIP`, etc.). | `[IN DEVELOPMENT 🚧]` | (N/A) | `simulator/agents/rider/rider.py` |
| **Ride Frequency**| A probabilistic model that determines when an `IDLE` rider decides to initiate a search. | `[IN DEVELOPMENT 🚧]` | `market.rider_population.rides_per_week_dist` | `simulator/agents/rider/logic.py` |
| **Utility Function** | The core logic a rider uses to evaluate and compare offers based on price, ETA, and habit. | `[IN DEVELOPMENT 🚧]` | `market.rider_population.price_sensitivity_dist`\<br\>`market.rider_population.time_sensitivity_dist` | `simulator/agents/rider/logic.py` |
| **Preference Score** | A dynamic score that evolves with user experience, modeling habit and **market share inertia**. | `[IN DEVELOPMENT 🚧]` | `market.rider_population.preference_score_dist` | `simulator/agents/rider/logic.py` |
| **Patience Timer** | A countdown timer that causes a rider to abandon their search if it takes too long. | `[IN DEVELOPMENT 🚧]` | `rider.patience_ticks_dist` | `simulator/agents/rider/rider.py` |
| **App Download** | A low-probability event for a rider to download a competitor's app after a poor experience. | `[PLANNED 📝]` | `rider.app_download_probability` | `simulator/agents/rider/logic.py` |

-----

## Driver Agent

| Feature Name | Description | Status | YAML Parameter(s) | Code Location(s) |
| :--- | :--- | :--- | :--- | :--- |
| **Base Agent State** | Core properties of a driver, including exclusivity and behavioral sensitivities. | `[IN DEVELOPMENT 🚧]` | `market.driver_population.*` | `simulator/agents/driver/driver.py` |
| **State Machine** | Manages the driver's current state (`OFFLINE`, `IDLE`, `ON_TRIP`, etc.). | `[IN DEVELOPMENT 🚧]` | (N/A) | `simulator/agents/driver/driver.py` |
| **Preference Score** | A dynamic score that evolves based on recent earnings, guiding which platform a driver prefers. | `[IN DEVELOPMENT 🚧]` | `market.driver_population.preference_score_dist` | `simulator/agents/driver/logic.py` |
| **Dynamic Switching** | Logic that allows an idle multi-homing driver to check the competitor app if they aren't receiving orders. | `[IN DEVELOPMENT 🚧]` | `driver.idle_switch_threshold_ticks` | `simulator/agents/driver/logic.py` |
| **Profitability Score** | The core logic a driver uses to decide whether to accept or reject an `Order Try`, balancing the fare against the unpaid ETA. | `[IN DEVELOPMENT 🚧]` | `market.driver_population.price_sensitivity_dist`\<br\>`market.driver_population.eta_sensitivity_dist` | `simulator/agents/driver/logic.py` |

-----

## Platform & Incentives

| Feature Name | Description | Status | YAML Parameter(s) | Code Location(s) |
| :--- | :--- | :--- | :--- | :--- |
| **Matcher** | The platform's core algorithm for connecting riders with the nearest available drivers using an `Order Try` flow to improve **liquidity**. | `[IN DEVELOPMENT 🚧]` | `platform.max_order_tries` | `simulator/platform/matcher.py` |
| **A/B Test Framework** | A generic `Test` object that manages user targeting, enrollment, and control/treatment splitting for all incentives. | `[IN DEVELOPMENT 🚧]` | `incentives[].test.*` | `simulator/platform/testing/test.py` |
| **Rider Discounts** | The `DiscountCampaign` class and associated logic for offering targeted price reductions to riders. | `[IN DEVELOPMENT 🚧]` | `incentives[].campaign.type: RiderDiscount` | `simulator/platform/incentives/rider_discount.py` |
| **Driver Bonuses** | The `BonusQuest` class and logic for offering performance-based quests to drivers, including dynamic re-evaluation of success probability. | `[IN DEVELOPMENT 🚧]` | `incentives[].campaign.type: BonusQuest` | `simulator/platform/incentives/driver_bonus.py` |
| **Surge Pricing** | A dynamic pricing model based on the real-time supply/demand ratio in a hex cell. | `[PLANNED 📝]`| `platform.surge_multiplier_max`| `simulator/platform/matcher.py` |