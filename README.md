# OTIMIZATION-ALGORITHM-WITH-PSO-AND-DSA

This repository contains a system for optimizing material simulation parameters using a hybrid approach that combines Particle Swarm Optimization (PSO) and Downhill Simplex Algorithm (DSA). The system integrates parameter optimization with geometry creation, simulation execution, and data analysis, leveraging Abaqus for geometry creation and simulation.

⚠ **Note**: This project is a work in progress and currently contains errors and placeholder scripts. Some parts, such as the simulation execution (`functions.py`), need to be fully implemented.

---

## Overview

The project is designed to optimize simulation parameters to match target forces and temperature values. It automates the following tasks:

1. **Geometry Creation**: Generates input files (`.inp`) for Abaqus simulations using Python scripts.
2. **Optimization**:
   - **PSO**: A global optimization algorithm that finds approximate optimal parameters.
   - **DSA**: A local optimization algorithm that refines the parameters further.
3. **Simulation Execution**: Runs Abaqus simulations with the optimized parameters.
4. **Data Analysis**: Logs and stores simulation results to assess performance and accuracy.

---

## Workflow

### 1. **Geometry Creation**
- Scripts in the `generate-simulation/codes-to-create-geometry` directory automate the creation of Abaqus input files (`.inp`).
- The `simulationManager.py` script orchestrates the geometry creation process using Abaqus CAE.
- This process is triggered by the `main.py` script in the `generate-simulation` directory:
  1. Runs Abaqus in no-GUI mode to generate geometry files.
  2. Deletes temporary files generated during the process.

### 2. **Optimization**
- The `hybrid-algorithm-pso-and-dsa/main.py` script orchestrates the optimization workflow:
  - **PSO Optimization**:
    - The `run_pso` function in `pso.py` optimizes the parameters (`A`, `B`, `C`, `n`, `m`) using the `pyswarm` library.
    - The objective function minimizes the error between simulated and target forces and temperature.
    - Results are saved to an Excel file (`datas.xlsx`) for tracking each iteration.
  - **DSA Refinement (Optional)**:
    - The `run_dsa` function in `dsa.py` refines the parameters found by PSO using the Nelder-Mead method within a localized search space.

### 3. **Simulation Execution**
- The optimized parameters are passed to Abaqus for simulation.
- The Abaqus job is submitted, and simulation results (e.g., forces and temperature) are retrieved.

### 4. **Data Logging and Analysis**
- Each iteration's parameters, target values, simulation results, and errors are logged in an Excel file (`datas.xlsx`).
- This file is updated after every simulation to track progress.
