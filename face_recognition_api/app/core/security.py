from __future__ import annotations

from robyn_rate_limits import InMemoryStore
from robyn_rate_limits import RateLimiter

limiter = RateLimiter(store=InMemoryStore, calls_limit=3, limit_ttl=100)
