from collections import defaultdict


class LineageGraph:
    def __init__(self):
        self.edges: dict[str, set[str]] = defaultdict(set)

    def link(self, upstream: str, downstream: str) -> None:
        self.edges[upstream].add(downstream)

    def blast_radius(self, root: str) -> set[str]:
        seen, queue = set(), [root]
        while queue:
            node = queue.pop(0)
            for child in self.edges.get(node, set()):
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
        return seen
