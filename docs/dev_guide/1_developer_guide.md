# Developer Guide: System Architecture

## 1\. Introduction

This document provides a technical deep-dive into the architecture and inner workings of the High-Fidelity Ride-Hailing Simulator. It is intended for developers and data scientists who will be maintaining, calibrating, or extending the model.

It assumes the reader is familiar with the project's goals, as outlined in the [README.md](https://www.google.com/search?q=../README.md).

-----

## 2\. Architecture Overview

The simulator follows a modular, agent-based architecture designed for clarity, testability, and extensibility. The core design principle is a strict separation of concerns between the simulation engine, the market environment, the platform's "backend," and the agents' individual "brains".

The project is organized into four main source directories within `simulator/`:

  * **`core`**: Manages the simulation's clock and main execution loop. It is the heartbeat of the system.
  * **`market`**: Represents the environment. It holds all the agents and the spatial grid they inhabit.
  * **`agents`**: Contains the state and properties for the `RiderAgent` and `DriverAgent` classes.
  * **`platform`**: Contains the logic for the ride-hailing platforms, including the matching algorithm.

-----

## 3\. High-Level Simulation Flow

The simulation begins at the `main.py` entry point, which is responsible for parsing command-line arguments, loading the specified `.yaml` configuration file, and initializing the core components in the correct order.

The simulation then proceeds according to a **two-level clock** managed by the `Engine`.

1.  **Major Ticks (Outer Loop):** Represents a large time step (e.g., one hour). Strategic, less frequent decisions are made here.

      * Drivers decide whether to go online for a "shift".
      * A probability check occurs for idle riders to initiate a new ride search.

2.  **Minor Ticks (Inner Loop):** Represents a small, operational time step (e.g., 10 seconds). This is where the real-time marketplace dynamics unfold.

      * Riders send search requests to platforms.
      * Platforms attempt to match riders with available drivers.
      * Drivers accept or reject offers.
      * Agent locations are updated.

This sequence of events, driven by the `Engine`, causes macro-level outcomes like market share and ROI to emerge from the low-level interactions of all the individual agents.

-----

## 4\. Module Deep Dives

For a detailed, step-by-step explanation of how each component works, please refer to the following documents:

  * **[2. Entry Point & Engine](https://www.google.com/search?q=./2_entry_point_and_engine.md):** A detailed look at how the simulation is launched and how the two-level clock orchestrates the sequence of events.
  * **[3. The Market Environment](https://www.google.com/search?q=./3_market_environment.md):** An explanation of how the world is created, including agent population generation and the spatial grid.
  * **[4. Agents Deep Dive](https://www.google.com/search?q=./4_agents_deep_dive.md):** A breakdown of the Rider and Driver agent state machines and their decision-making logic.
  * **[5. Platforms & Matching](https://www.google.com/search?q=./5_platforms_and_matching.md):** A step-by-step guide to the platform's "backend," detailing the `Matcher` and the "Order Try" flow.