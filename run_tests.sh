#!/bin/bash

# Define the output file
output_file="simulation_results.csv"

# Header for the CSV file
echo "Test Case,Associativity,Total Time (ns),Total Energy (pJ),Avg Time per Mem Operation (ns),L1 Total Energy (pJ),L1i Dynamic Energy (pJ),L1i Hits,L1i Misses,L1d Dynamic Energy (pJ),L1d Hits,L1d Misses,L2 Energy (pJ),L2 Hits,L2 Misses,DRAM Energy (pJ)" > "$output_file"

# Directory containing the test cases
test_dir="Spec_Benchmark"

# Array of associativity values
declare -a assoc_values=(2 4 8)

# Iterate over each test file in the directory
for test_file in "$test_dir"/*.din; do
    # For each associativity value
    for assoc in "${assoc_values[@]}"; do
        # Run the simulator and capture the output
        output=$(python3 simulator.py "$test_file" $assoc)

        # Extract data from the output using grep and awk
        total_time=$(echo "$output" | grep 'Total time (ns):' | awk '{print $4}')
        total_energy=$(echo "$output" | grep 'Total Energy (pJ):' | awk '{print $5}' | tr -d '\n')
        avg_time=$(echo "$output" | grep 'Avg Time per Mem Operation (ns):' | awk '{print $7}')
        l1_total_energy=$(echo "$output" | grep 'L1 Total Energy (pJ):' | awk '{print $5}')
        l1i_dynamic_energy=$(echo "$output" | grep 'L1i Dynamic Energy (pJ):' | awk '{print $5}')
        l1i_hits=$(echo "$output" | grep 'L1i Hits / Misses:' | awk '{print $5}')
        l1i_misses=$(echo "$output" | grep 'L1i Hits / Misses:' | awk '{print $7}')
        l1d_dynamic_energy=$(echo "$output" | grep 'L1d Dynamic Energy (pJ):' | awk '{print $5}')
        l1d_hits=$(echo "$output" | grep 'L1d Hits / Misses:' | awk '{print $5}')
        l1d_misses=$(echo "$output" | grep 'L1d Hits / Misses:' | awk '{print $7}')
        l2_energy=$(echo "$output" | grep 'L2 Energy (pJ):' | awk '{print $4}')
        l2_hits=$(echo "$output" | grep 'L2 Hits / Misses:' | awk '{print $5}')
        l2_misses=$(echo "$output" | grep 'L2 Hits / Misses:' | awk '{print $7}')
        dram_energy=$(echo "$output" | grep 'DRAM Energy (pJ):' | awk '{print $4}')

        # Append to the CSV
        echo "$test_file,$assoc,$total_time,$total_energy,$avg_time,$l1_total_energy,$l1i_dynamic_energy,$l1i_hits,$l1i_misses,$l1d_dynamic_energy,$l1d_hits,$l1d_misses,$l2_energy,$l2_hits,$l2_misses,$dram_energy" >> "$output_file"
    done
done
