EXAMPLE = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


def is_valid_line(s):
    return s is not None and s != ""


def read_points(lines):
    """
    input: lines of 'x,y,z'
    output: list of (x, y, z) as integers
    """
    points = []

    for line in lines:
        if not is_valid_line(line.strip()):
            continue

        parts = line.strip().split(",")
        x = int(parts[0])
        y = int(parts[1])
        z = int(parts[2])

        points.append((x, y, z))

    return points


def squared_distance(a, b):
    """
    a, b are (x, y, z)
    returns squared euclidean distance (integer)
    """
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx**2 + dy**2 + dz**2


def build_all_edges(points):
    """
    returns list of edges: (dist2, i, j) for all i < j
    we sort edges so we can process the closest connections first.
    """
    n = len(points)
    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            d2 = squared_distance(points[i], points[j])
            edges.append((d2, i, j))

    # Sort by dist2, then by i, then by j for deterministic tie-breaking
    edges.sort()
    return edges


class UnionFind:
    """
    Union-Find / Disjoint Set Union (DSU)

    we use it to maintain "circuits" (connected components) efficiently.

    parent[x] = representative parent of x
    size[root] = size of the component for that root

    operations:
    - find(x): get component representative
    - union(a, b): merge components if different
    """

    def __init__(self, n):
        self.parent = []
        self.size = []
        self.components = n

        for i in range(n):
            self.parent.append(i)
            self.size.append(1)

    def find(self, x):
        # iterative path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        """
        merge the components of a and b.

        returns:
            True if a merge happened (they were in different components),
            False if nothing changed (already same component).
        """
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return False

        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

    def component_sizes(self):
        """
        returns list of sizes of all connected components.
        """
        counts = {}

        for i in range(len(self.parent)):
            r = self.find(i)
            if r not in counts:
                counts[r] = 0
            counts[r] += 1

        sizes = []
        for r in counts:
            sizes.append(counts[r])

        return sizes
