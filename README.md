# Cache Simulator — Computer Architecture Project

A configurable **set-associative cache simulator** implementing **LRU replacement**, **fully-associative mode**, and **Average Memory Access Time (AMAT)** analysis. Built to model real CPU cache behavior and evaluate memory hierarchy performance.

## Features
- Supports **direct-mapped, N-way set associative, and fully associative** caches  
- Configurable **cache size, block size, and associativity**  
- Implements **LRU (Least Recently Used) replacement policy**  
- Computes **hit rate, miss rate, and AMAT (Average Memory Access Time)**  
- Includes **automated test suite (pytest)** for correctness validation  
- CLI-based simulation using memory trace files  

## Example Usage
```bash
python3 src/main.py --cache_kb 16 --block 64 --assoc 4 --trace traces/sample.txt --hit_time 1 --miss_penalty 50

## Sample Output
Cache Size       : 16 KB
Block Size       : 64 B
Associativity    : 4-way
Number of Sets   : 64
Accesses         : 6
Hits             : 2
Misses           : 4
Hit Rate         : 33.33%
Miss Rate        : 66.67%
AMAT             : 34.33 cycles


## Architecture Overview
- Address mapping into Index + Tag
- Cache sets store valid bit, tag, and LRU timestamp
- Eviction selects Least Recently Used (LRU) cache line
- Performance modeled using AMAT = HitTime + MissRate × MissPenalty

##Running Tests
python3 -m pytest -q


## Why This Project Matters
- Demonstrates computer architecture & memory hierarchy fundamentals
- Implements cache replacement policy (LRU) used in real CPUs
- Evaluates performance using AMAT, mirroring industry practice
- Built with test-driven development for correctness and reliability


##Tech Stack
- Python, Computer Architecture, Memory Systems, Pytest, CLI Tools
