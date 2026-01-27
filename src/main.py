import argparse
from cache import CacheSimulator


def parse_trace_line(line: str):
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    parts = line.split()
    if len(parts) != 2:
        raise ValueError(f"Bad trace line: {line}")

    op, addr = parts
    if addr.lower().startswith("0x"):
        address = int(addr, 16)
    else:
        address = int(addr)

    return op, address


def main():
    ap = argparse.ArgumentParser(description="Set-associative cache simulator (LRU)")
    ap.add_argument("--cache_kb", type=int, required=True)
    ap.add_argument("--block", type=int, required=True)
    ap.add_argument("--assoc", type=int, required=True)
    ap.add_argument("--trace", type=str, required=True)
    ap.add_argument("--hit_time", type=float, default=1.0, help="Hit time in cycles (default: 1)")
    ap.add_argument("--miss_penalty", type=float, default=50.0, help="Miss penalty in cycles (default: 50)")

    args = ap.parse_args()

    sim = CacheSimulator(args.cache_kb, args.block, args.assoc)

    with open(args.trace, "r") as f:
        for raw in f:
            parsed = parse_trace_line(raw)
            if parsed is None:
                continue
            _, address = parsed
            sim.access(address)

    s = sim.stats()
    amat = args.hit_time + s["miss_rate"] * args.miss_penalty

    print("\n=== Cache Simulator Results ===")
    print(f"Cache Size       : {s['cache_size_kb']} KB")
    print(f"Block Size       : {s['block_size_bytes']} B")
    print(f"Associativity    : {s['associativity']}-way")
    print(f"Number of Sets   : {s['num_sets']}")
    print(f"Accesses         : {s['accesses']}")
    print(f"Hits             : {s['hits']}")
    print(f"Misses           : {s['misses']}")
    print(f"Hit Rate         : {s['hit_rate']*100:.2f}%")
    print(f"Miss Rate        : {s['miss_rate']*100:.2f}%\n")
    print(f"AMAT             : {amat:.2f} cycles (hit_time={args.hit_time}, miss_penalty={args.miss_penalty})\n")
    
if __name__ == "__main__":
    main()
