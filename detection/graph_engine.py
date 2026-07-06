"""graph_engine.py."""
"""Trade graph and SCC wash-ring detection."""
import logging
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger("arguschain.detection.graph_engine")

@dataclass
class WashRing:
    accounts: list[str]
    total_volume: float
    cycle_volume: float
    detected_at: datetime
    trade_count: int = 0
    truncated: bool = False

class TradeGraph:
    def __init__(self, max_ring_size: int = 100):
        self.max_ring_size = max_ring_size
        self.edges = defaultdict(list)
        self.edge_data = {}
        self.rings = []

    def add_trade(self, seller: str, buyer: str, amount: float, timestamp: datetime):
        self.edges[seller].append((buyer, amount))
        edge_key = (seller, buyer)
        if edge_key not in self.edge_data:
            self.edge_data[edge_key] = {"total_volume": 0, "trades": []}
        self.edge_data[edge_key]["total_volume"] += amount
        self.edge_data[edge_key]["trades"].append({"timestamp": timestamp, "amount": amount})

    def find_wash_rings(self) -> list[WashRing]:
        if not self.edges:
            return []
        rings = []
        for scc in self._find_sccs():
            if len(scc) >= 3:
                total_volume = sum(self.edge_data.get((s, t), {}).get("total_volume", 0) 
                                  for s in scc for t, _ in self.edges.get(s, []) if t in scc)
                ring = WashRing(
                    accounts=scc, total_volume=total_volume,
                    cycle_volume=total_volume * 0.5, detected_at=datetime.utcnow(),
                    truncated=len(scc) > self.max_ring_size
                )
                rings.append(ring)
        self.rings = rings
        return rings

    def _find_sccs(self):
        # Simplified iterative Tarjan's algorithm
        visited, recstack, parent = set(), set(), {}
        def dfs(v, stack):
            visited.add(v)
            recstack.add(v)
            for u, _ in self.edges.get(v, []):
                if u not in visited:
                    stack.append(u)
                elif u in recstack:
                    parent[u] = v
        result = []
        for v in self.edges:
            if v not in visited:
                stack = [v]
                while stack:
                    node = stack.pop()
                    if node not in visited:
                        dfs(node, stack)
        return []  # Placeholder
