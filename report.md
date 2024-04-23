# Memory Subsystem Design Report (Krishna Reddy, Savindu Wimalasooriya)

## Design Decisions

### Cache Indexing
- **Index Calculation**: The cache line indexed into is given by the formula: `(mem_address >> 4) % (cache_size / cache_line_size)` as the memory address points to 4 bytes and each cache line contains 6 bytes

### L1 Cache
- **Operational Modes**: The L1 cache supports both instruction fetching and data operations.
- **Write Strategy**: L1 cache implements a direct write-through approach to L2, ensuring data consistency between the L1 and L2 caches without explicit write-backs.
- **Energy Calculation**:
  - Active energy is calculated based on the time the cache is actively being read or written to, using the active power constant.
  - Idle energy consumption is based on the total time minus active time, multiplied by the idle power rate.

### L2 Cache
- **Associativity**: The L2 cache's associativity level is configurable, allowing it to be adjusted based on the input parameter. This affects how memory addresses map to cache sets.
- **Write Strategy**: Any writes write-through to L1 and L2. Upon eviction, and in the case of a dirty bit, this is written to DRAM. This energy cost is factored in with the 645 pJ penalty for L1 and L2 miss, as specified in the Ed Discussion #150: _"copy of data DRAM -> L2 and L2 -> DRAM on misses do not take extra time or extra active energy for the writes - this is included in penalty energy"_
- **Replacement Policy**: Random replacement within the associativity set is used when a cache miss occurs and a new line needs to be loaded.
- **Energy Calculation**:
  - Active energy is calculated based on the time the cache is actively being read or written to, using the active power constant.
  - Idle energy consumption is based on the total time minus active time, multiplied by the idle power rate.

### Main Memory
- **Access Penalties**: Both read and write operations incur a fixed penalty, representing the additional time taken for operations reaching the main memory.
- **Energy Calculation**:
  - Active energy is calculated based on the time the memory is actively being read or written to, using the active power constant.
  - Idle energy consumption is based on the total time minus active time, multiplied by the idle power rate.

### General
- **Energy Penalties**: Additional penalties are added for L2 accesses and main memory operations, reflecting the higher energy cost of using these slower memory forms.

### L2 Associativity Impact
- **L2 Cache Miss Rate**: An increase from associativity 2 to 4 significantly decreases the miss rate. The increase from 4 to 8 did not result in a decrease as large. This is likely because the probability of over 4 collisions is significantly low enough for 8 associativity to not have a huge impact.
- **Energy Consumption**: The decrease in L2 cache misses, slightly decreased the total energy consumption by decreasing the energy used by DRAM
- **Time**: The time was also slightly decreased, by decreasing L2 cache misses
