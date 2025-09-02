Of course. Here is the `User Guide & Scenario Cookbook` for the High-Fidelity Ride-Hailing Simulator.

-----

# User Guide & Scenario Cookbook

Welcome to the High-Fidelity Ride-Hailing Simulator\! This guide is for strategists, analysts, and business managers who want to use the simulator to test scenarios, forecast outcomes, and inform investment decisions.

This document will walk you through how to configure, run, and interpret simulations. No programming knowledge is required.

-----

## 1\. The Configuration File (`config.yaml`)

Every simulation run is controlled by a single `.yaml` configuration file. This file is where you define the market conditions and the strategic actions for each platform.

### **Simulation Settings**

This block controls the overall simulation environment.

```yaml
simulation:
  # The total duration of the simulation.
  duration_days: 90
  # A unique seed for the random number generator to ensure the run is reproducible.
  random_seed: 42
```

### **Market Settings**

This block defines the market's static properties and the initial state of the agent population.

```yaml
market:
  # The local currency for all financial calculations.
  local_currency: "PLN"
  # The fixed exchange rate for converting the local currency to EUR for reporting.
  eur_fx_rate: 4.2483
  # Total number of agents to create at the start of the simulation.
  initial_riders: 10000
  initial_drivers: 1000
  # Defines the initial distribution of riders' app ownership.
  rider_population:
    pct_with_app_a_only: 0.20
    pct_with_app_b_only: 0.20
    pct_with_both_apps: 0.60
```

### **Platform Settings**

This is where you set the core strategic levers for each platform.

```yaml
platforms:
  A:
    price_per_km: 2.10
    commission_rate: 0.25
  B:
    price_per_km: 2.15
    commission_rate: 0.24
```

-----

## 2\. Running a Simulation

Running a simulation is done from the command line.

1.  **Open your terminal** and navigate to the project's root directory (`ride_hailing_simulator/`).
2.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```
3.  **Run the simulation script**, pointing it to your desired configuration file:
    ```bash
    python main.py --config configs/your_scenario_config.yaml
    ```

The simulator will print progress updates to the console and save the output files once complete.

-----

## 3\. Interpreting the Outputs

The simulation generates several output files in a timestamped folder inside the `/results` directory. The two most important are:

  * **`summary.csv`:** This file gives you the high-level, aggregate results at the end of the simulation period. It includes key metrics like Final Market Share, Total GMV (EUR), Total Spend (EUR), and the **uplift-to-cost ratio** for any A/B tests you ran.
  * **`timeseries.csv`:** This file provides a tick-by-tick breakdown of key metrics (Market Share, Active Drivers, Average ETA, etc.) for each platform. It's perfect for plotting graphs to see how the market evolved over time.

-----

## 4\. Scenario Cookbook 🍳

This section provides step-by-step recipes for answering common strategic questions.

### **Scenario 1: A Sustained Price Reduction**

**Goal:** To measure the market share impact and cost of a 5% price reduction over 90 days, assuming our competitor does not react.

1.  **Create the Baseline:** First, copy `configs/warsaw_base.yaml` to `configs/scenario_1_baseline.yaml`. Run this simulation to get your benchmark results.
2.  **Create the Test Scenario:** Copy the baseline file to `configs/scenario_1_price_cut.yaml`.
3.  **Modify the Config:** In the new file, find the `platforms` block and reduce the `price_per_km` for your platform (e.g., Platform A) by 5%.
    ```yaml
    platforms:
      A:
        price_per_km: 1.99 # Was 2.10
      B:
        price_per_km: 2.15
    ```
4.  **Run & Compare:** Run the new simulation. Compare the `summary.csv` files from the baseline and the test run. You can now quantify the change in market share, GMV, and profitability resulting from the price cut. Observe the `timeseries.csv` to see how long it takes for the market share to shift, demonstrating the **market inertia** effect.

### **Scenario 2: ROI of a Driver "Welcome Back" Bonus**

**Goal:** To A/B test a "complete 50 rides in a month, get 200 PLN" bonus for inactive drivers and measure its ROI.

1.  **Start with a Baseline Config:** Copy your base config to `configs/scenario_2_driver_bonus.yaml`.
2.  **Define the Test:** In the config file, add an `incentives` block (if it doesn't exist). Inside, define a new `Test`.
    ```yaml
    incentives:
      - test: # Use a descriptive name for the test ID
          id: welcome_back_bonus_q3_2025
          # Target only drivers.
          user_type: driver
          # Use a rule to select inactive drivers (logic defined in the code).
          targeting_criteria: "rides_in_last_30_days == 0"
          # Define the A/B test split.
          variants:
            - variant: control
              split_pct: 0.1 # 10% control group
            - variant: treatment_200_pln
              split_pct: 0.9 # 90% treatment group
    ```
3.  **Define the Bonus:** Now, define the `BonusQuest` campaign for the treatment variant.
    ```yaml
          # This campaign is linked to the test variant above.
          campaign:
            variant_id: treatment_200_pln
            # Define the bonus quest details.
            type: BonusQuest
            duration_days: 30
            requirement:
              type: completed_rides
              value: 50
            reward:
              type: fixed_amount
              value: 200
    ```
4.  **Run & Analyze:** Run the simulation. When it's finished, open the `summary.csv` file. Find the row corresponding to your test ID (`welcome_back_bonus_q3_2025`) and look at the `uplift_to_cost_ratio` column. This number is the direct ROI of your campaign, which you can use to make data-driven investment decisions.