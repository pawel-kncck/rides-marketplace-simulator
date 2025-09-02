# Gemini Project Context: High-Fidelity Ride-Hailing Simulator

This document provides context for the Gemini AI agent to understand and assist with the development of this project.

## Project Overview

This project is a high-fidelity ride-hailing simulator. It uses an agent-based model (ABM) to simulate the competitive dynamics of a duopoly ride-hailing market. The goal is to create a "digital twin" that allows for testing strategic hypotheses and quantifying the impact of investment decisions in a complex, non-linear environment.

The simulation is built in Python and follows a modular architecture that separates the core engine, the market environment, the agents (riders and drivers), and the ride-hailing platforms.

## Key Files and Directories

*   `main.py`: The main entry point for running a simulation from the command line.
*   `configs/`: Contains `.yaml` files that define the parameters for different simulation scenarios.
*   `simulator/`: The primary source code directory, organized into four key modules:
    *   `core/`: The simulation engine, which manages the discrete-time clock.
    *   `market/`: The environment, containing the agent populations and the spatial grid.
    *   `agents/`: The `RiderAgent` and `DriverAgent` classes and their decision-making logic.
    *   `platform/`: The logic for the ride-hailing platforms, including the matching algorithm and incentive framework.
*   `tests/`: Contains unit and end-to-end tests for the simulator.
*   `docs/`: Contains detailed documentation for users and developers.

## Building and Running

### Prerequisites

*   Python 3.9+
*   `pip` and `venv`

### Setup and Installation

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running Tests

To verify the installation and the integrity of the codebase, run the test suite:

```bash
pytest
```

### Running a Simulation

Simulations are run from the root directory, specifying a configuration file.

```bash
python main.py --config configs/warsaw_base.yaml
```

## Development Conventions

*   **Testing:** All new code must be accompanied by tests.
    *   **Unit Tests:** Isolate and test specific logic functions (e.g., utility calculations, state transitions).
    *   **End-to-End (E2E) Tests:** Create a dedicated config file for major new features to validate the behavior of the system as a whole.
*   **Logging:** The project uses a structured event log for debugging. When adding new features, emit log events at key decision points to allow for reconstructing the "journal" of an agent or order.
*   **Documentation:** The project maintains a multi-document structure in the `/docs` directory to serve different audiences (users vs. developers). All new features should be reflected in the relevant documentation, especially the `feature-parameter-ref.md` living document.
