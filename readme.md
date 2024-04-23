# Simulation Toolchain README


## 1. Simulator (`simulator.py`)

### Overview

`simulator.py` is a Python script that simulates the cache energy and time

### How to Run

The simulator takes two arguments:
- **Test Case File**: The path to the test case file.
- **Associativity**: An integer value (e.g., 2, 4, or 8) that specifies the cache associativity setting.

#### Example Command
    python3 simulator.py Spec_Benchmark/013.spice2g6.din 4

## 2. Bash Script for Automating Simulations (`run_tests.sh`)

### Overview
The provided bash script automates the process of running `simulator.py`, running it on each of the 15 tests with associativities 2,4, and 8 and recording the outputs into a csv file titled `simulation_results.csv`, where each row represents a run.

### How to Run
Ensure that the script is executable and located in the same directory as `simulator.py` and the `Spec_Benchmark` folder, and has execution permissions. Then type the command:

    ./run_tests.sh


