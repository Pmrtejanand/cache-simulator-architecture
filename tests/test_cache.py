
from src.cache import CacheSimulator


def test_basic_hits_and_misses():
    sim = CacheSimulator(cache_size_kb=1, block_size_bytes=16, associativity=1)

    # first access miss, next accesses hit same block
    assert sim.access(0x0000) is False
    assert sim.access(0x0004) is True
    assert sim.access(0x000F) is True

    stats = sim.stats()
    assert stats["accesses"] == 3
    assert stats["misses"] == 1
    assert stats["hits"] == 2


def test_lru_eviction():
    sim = CacheSimulator(cache_size_kb=1, block_size_bytes=16, associativity=2)

    a = 0 * sim.block_size
    b = sim.num_sets * sim.block_size
    c = 2 * sim.num_sets * sim.block_size

    assert sim.access(a) is False
    assert sim.access(b) is False
    assert sim.access(a) is True      # a becomes MRU, b is LRU
    assert sim.access(c) is False     # should evict b

    # After inserting c, a should still be present
    assert sim.access(a) is True

    # b was evicted by c
    assert sim.access(b) is False
