# High-Fidelity Ride-Hailing Simulator

An agent-based model (ABM) designed to simulate the competitive dynamics of a duopoly ride-hailing market. This tool serves as a strategic digital twin, allowing us to test hypotheses and quantify the impact of investment decisions in a complex, non-linear environment.

-----

## The Challenge: The Market Share Elasticity Conundrum

Traditional linear models for forecasting market share are helpful but fundamentally limited. They often fail to capture the complex realities of ride-hailing competition because market share dynamics are shaped by two powerful, interacting forces:

1.  **Competitive Investments:** Short-term changes driven by rider discounts, driver bonuses, and relative pricing.
2.  **Marketplace Network Effects:** The long-term, self-reinforcing advantage that comes from being the larger platform. Higher market share leads to better liquidity, which improves the user experience for both riders (shorter ETAs) and drivers (higher utilization), creating a powerful competitive moat.

This creates the **Market Share Elasticity Conundrum**: both the dominant market leader and the smaller challenger can appear to have low elasticity to investments, but for entirely different reasons (diminishing returns vs. network barriers). This simulator is designed to untangle these effects.

-----

## Our Solution: An Agent-Based Model

Instead of top-down statistical modeling, this simulator takes a bottom-up approach. It models a population of thousands of individual **Rider Agents** and **Driver Agents**, each with their own unique properties, preferences, and decision-making logic.

  * **Riders** seek to maximize their personal utility by weighing price, wait time, and platform preference.
  * **Drivers** seek to maximize their earnings by evaluating fares, bonuses, and their likelihood of success.

Macro-level outcomes like **market share, GMV, and investment ROI** are not pre-programmed; they are **emergent properties** that arise from the collective interactions of all agents within the simulated marketplace. This allows us to capture the non-linear dynamics, feedback loops, and inertia that define real-world competition.

-----

## Core Capabilities

This simulator is designed to answer critical strategic questions that are difficult to tackle with other methods:

  * **Quantify Non-Linear ROI:** Measure how the effectiveness of a discount or bonus changes at different levels of market share.
  * **Model Market Inertia:** Understand the long-term, delayed impact of sustained investment on market share.
  * **Test Competitive Scenarios:** Simulate game-theoretic scenarios like price wars, promotional blitzes, and defensive reactions.
  * **Analyze Supply-Side Dynamics:** Assess the impact of driver exclusivity, bonus structures, and acceptance behavior on marketplace health.
  * **Calibrate with Real-World Data:** Use a built-in `Test` framework to calibrate agent behaviors against the results of real-world A/B tests.

-----

## Getting Started

### Prerequisites

  * Python 3.9+
  * `pip` and `venv`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd ride_hailing_simulator
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Tests

To ensure the environment is set up correctly and the simulator is functioning as expected:

```bash
pytest
```

### Running a Simulation

To run a simulation using a specific configuration file:

```bash
python main.py --config configs/warsaw_base.yaml
```

-----

## Documentation

For more detailed information, please refer to the following documents:

  * **[User Guide & Scenario Cookbook](https://www.google.com/search?q=./docs/USER_GUIDE.md):** For analysts and strategists. Learn how to configure and run scenarios.
  * **[System Architecture & Developer Guide](https://www.google.com/search?q=./docs/DEVELOPER_GUIDE.md):** For developers. A technical deep-dive into the simulator's code.
  * **[Feature & Parameter Reference](https://www.google.com/search?q=./docs/FEATURE_REFERENCE.md):** A living document tracking all features, their status, and configuration parameters.

-----

## Feature Roadmap

  * `[IMPLEMENTED ✅]` Core simulation engine with discrete-time clock
  * `[IMPLEMENTED ✅]` Rider Agent state machine and properties
  * `[IN DEVELOPMENT 🚧]` Driver Agent state machine and bonus evaluation logic
  * `[IN DEVELOPMENT 🚧]` Platform `Test` and `Campaign` framework for incentives
  * `[IN DEVELOPMENT 🚧]` Hexagonal grid and `Matcher` algorithm
  * `[PLANNED 📝]` Advanced driver multi-homing strategies
  * `[PLANNED 📝]` Dynamic surge pricing model
  * `[PLANNED 📝]` WebSocket emitter for live frontend visualization