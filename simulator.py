import sys
import random
# all units in picojoules and nanoseconds
L1_IDLE_POW = 500
L1_ACTIVE_POW = 1000
L1_RW_TIME = 0.5
L2_IDLE_POW = 800
L2_ACTIVE_POW = 2000
L2_RW_TIME = 5
L2_PENALTY = 640
MEM_IDLE_POW = 800
MEM_ACTIVE_POW = 4000
MEM_RW_TIME = 50

# opcodes
READ = 0
WRITE = 1
INS_FETCH = 2

total_time = 0



class Memory:
    def __init__(self):
        self.energy_penalty = 0
        self.active_ns = 0
    def attempt_read(self):
        global total_time
        self.energy_penalty += 640
        self.active_ns += MEM_RW_TIME
        total_time += MEM_RW_TIME
    def attempt_write(self):
        global total_time
        self.active_ns += MEM_RW_TIME
        total_time += MEM_RW_TIME

class L2:
    def __init__(self, associativity): 
        self.energy_penalty = 0
        self.active_ns = 0
        #num cache lines
        self.memory_size = 4096
        #cache lines stored
        self.memory = [-1 for _ in range(self.memory_size)]
        self.bits = [-1 for _ in range(self.memory_size)]
        self.associativity = associativity

        self.hits = 0
        self.misses = 0

    def attempt_read(self, opcode, address, l1, mem_module):
        global total_time
        self.active_ns += L2_RW_TIME
        self.energy_penalty += 5
        set_index = int((address >> 4) % ((self.memory_size) / self.associativity))
        found_index = -1
        for i in range(self.associativity):
            if self.memory[set_index * self.associativity + i] == (address >> 4):
                found_index = set_index * self.associativity + i
        if found_index == -1: # miss
            rand_ind = random.randint(0, self.associativity - 1)
            self.memory[set_index * self.associativity + rand_ind] = (address >> 4)
            mem_module.attempt_read()
            self.misses += 1
        else:
            self.hits += 1
            total_time += L2_RW_TIME
        return

    def attempt_write(self, opcode, address, l1, mem_module):
        global total_time
        self.active_ns += L2_RW_TIME
        set_index = int((address >> 4) % ((self.memory_size) / self.associativity))
        found_index = -1
        for i in range(self.associativity):
            if self.memory[set_index * self.associativity + i] == (address >> 4) or self.memory[set_index * self.associativity + i] == -1:
                found_index = set_index * self.associativity + i
        if found_index == -1: # miss
            rand_ind = random.randint(0, self.associativity - 1)
            # write back here
            mem_module.attempt_write()
            self.memory[set_index * self.associativity + rand_ind] = (address >> 4)
            self.misses += 1
        else:
            self.hits += 1
            total_time += 5
        return
    

class L1:
    def __init__(self):
        self.active_ns_instr = 0
        self.active_ns_mem = 0
        self.hits_instr = 0
        self.hits_mem = 0
        self.misses_instr = 0
        self.misses_mem = 0
        self.instructions_size = 512
        self.memory_size = 512
        #cache lines stored
        self.instructions = [-1 for _ in range(self.instructions_size)]
        self.memory = [-1 for _ in range(self.memory_size)]

    def attempt_read(self, opcode, address, l2, mem_module):
        global total_time
        line_addr = (address >> 4) % 512 
        if opcode == INS_FETCH:
            self.active_ns_instr += L1_RW_TIME
            if self.instructions[line_addr] == (address >> 4): # hit
                total_time += .5
                self.hits_instr += 1
            else: # miss
                self.instructions[line_addr] = (address >> 4)
                l2.attempt_read(opcode, address, self, mem_module)
                self.misses_instr += 1 
        elif opcode == READ:
            self.active_ns_mem += L1_RW_TIME
            if self.memory[line_addr] == (address >> 4):
                total_time += .5
                self.hits_mem += 1
            else: # miss
                self.memory[line_addr] = (address >> 4)
                l2.attempt_read(opcode, address, self, mem_module)
                self.misses_mem += 1
        return
    def attempt_write(self, opcode, address, l2, mem_module):
        line_addr = (address >> 4) % 512
        if(self.memory[line_addr] == (address >> 4) or self.memory[line_addr] == -1):
            self.hits_mem += 1
        else:
            self.misses_mem += 1
        self.memory[line_addr] = (address >> 4)
        l2.attempt_write(opcode, address, self, mem_module)
        self.active_ns_mem += L1_RW_TIME
        return

def simulate_line(l1, l2, mem, opcode, address):
    if(opcode == INS_FETCH or opcode == READ):
        l1.attempt_read(opcode, address, l2, mem)
    else:
        l1.attempt_write(opcode, address, l2, mem)
    return

def main(input, associativity):
    global total_time
    file = open(input, 'r')
    l1_cache = L1()
    l2_cache = L2(int(associativity))
    mem = Memory()
    count = 0
    while True:
        curr_line = file.readline()
        if not curr_line:
            break
        count += 1
        mem_args = curr_line.split(' ')
        simulate_line(l1_cache, l2_cache, mem, int(mem_args[0]), int(mem_args[1], 16))
    l1_energy = (l1_cache.active_ns_instr * L1_ACTIVE_POW) + (l1_cache.active_ns_mem * L1_ACTIVE_POW)  + (total_time - l1_cache.active_ns_instr - l1_cache.active_ns_mem) * L1_IDLE_POW
    l1_energy_instr = (l1_cache.active_ns_instr * L1_ACTIVE_POW)
    l1_energy_mem = (l1_cache.active_ns_mem * L1_ACTIVE_POW)
    l2_energy = (l2_cache.active_ns * L2_ACTIVE_POW) + (total_time - l2_cache.active_ns) * L2_IDLE_POW + l2_cache.energy_penalty
    mem_energy = (mem.active_ns * MEM_ACTIVE_POW) + (total_time - mem.active_ns) * MEM_IDLE_POW + mem.energy_penalty
    print("Test case: ", input)
    print("Associativity: ", int(associativity))
    print("Total time (ns): ", total_time)
    print("Total Energy (pJ): ", l1_energy + l2_energy + mem_energy)
    print("Avg Time per Mem Operation (ns): ", (total_time / count))
    print("L1 Total Energy (pJ): ", l1_energy)
    print("L1i Dynamic Energy (pJ): ", l1_energy_instr)
    print("L1i Hits / Misses: ", l1_cache.hits_instr, " / ", l1_cache.misses_instr)
    print("L1d Dynamic Energy (pJ): ", l1_energy_mem)
    print("L1d Hits / Misses: ", l1_cache.hits_mem, " / ", l1_cache.misses_mem)
    print("L2 Energy (pJ): ", l2_energy)
    print("L2 Hits / Misses: ", l2_cache.hits, " / ", l2_cache.misses)
    print("DRAM Energy (pJ): ", mem_energy)
    return
    

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])