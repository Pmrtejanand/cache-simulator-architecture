from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CacheLine:
    valid: bool = False
    tag: Optional[int] = None
    last_used: int = 0  # for LRU


@dataclass
class CacheSet:
    ways: int
    lines: List[CacheLine] = field(init=False)

    def __post_init__(self):
        self.lines = [CacheLine() for _ in range(self.ways)]


class CacheSimulator:
    """
    Set-associative cache simulator with LRU replacement.
    """

    def __init__(self, cache_size_kb: int, block_size_bytes: int, associativity: int):
        if cache_size_kb <= 0 or block_size_bytes <= 0:
            raise ValueError("Cache size and block size must be > 0")

        self.cache_size_bytes = cache_size_kb * 1024
        self.block_size = block_size_bytes

        # total lines in cache
        if self.cache_size_bytes % self.block_size != 0:
            raise ValueError("Cache size must be divisible by block size")

        self.num_lines = self.cache_size_bytes // self.block_size

        # allow assoc=0 => fully associative
        if associativity == 0:
            associativity = self.num_lines

        self.assoc = associativity

        if self.num_lines % self.assoc != 0:
            raise ValueError("Associativity must divide total number of lines")

        self.num_sets = self.num_lines // self.assoc

        # Stats
        self.accesses = 0
        self.hits = 0
        self.misses = 0
        self._time = 0

        # Initialize sets
        self.sets = [CacheSet(self.assoc) for _ in range(self.num_sets)]

    def _index_and_tag(self, address: int):
        block_addr = address // self.block_size
        index = block_addr % self.num_sets
        tag = block_addr // self.num_sets
        return index, tag

    def access(self, address: int) -> bool:
        """Return True if hit, False if miss."""
        self.accesses += 1
        self._time += 1

        index, tag = self._index_and_tag(address)
        cset = self.sets[index]

        # Check hit
        for line in cset.lines:
            if line.valid and line.tag == tag:
                self.hits += 1
                line.last_used = self._time
                return True

        # Miss
        self.misses += 1

        # Fill invalid line first
        for line in cset.lines:
            if not line.valid:
                line.valid = True
                line.tag = tag
                line.last_used = self._time
                return False

        # Evict LRU
        lru_line = min(cset.lines, key=lambda l: l.last_used)
        lru_line.tag = tag
        lru_line.last_used = self._time
        lru_line.valid = True
        return False

    def stats(self):
        hit_rate = (self.hits / self.accesses) if self.accesses else 0.0
        miss_rate = (self.misses / self.accesses) if self.accesses else 0.0

        return {
            "cache_size_kb": self.cache_size_bytes // 1024,
            "block_size_bytes": self.block_size,
            "associativity": self.assoc,
            "num_sets": self.num_sets,
            "accesses": self.accesses,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "miss_rate": miss_rate,
        }

