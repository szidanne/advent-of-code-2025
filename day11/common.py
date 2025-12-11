EXAMPLE = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""


def build_graph(data):
    graph = {}
    for line in data:
        line = line.strip()
        if not line:
            continue
        key, vals = line.split(":")
        graph[key.strip()] = vals.strip().split()
    return graph


def dfs_all(graph, node, end, memo):
    """count all paths from node to end (no constraints)"""
    if node == end:
        return 1

    if node in memo:
        return memo[node]

    total = 0
    for nxt in graph.get(node, []):
        total += dfs_all(graph, nxt, end, memo)

    memo[node] = total
    return total


def dfs_required(graph, node, end, required_nodes, seen_required, memo):
    """
    count paths from node to end that visit all nodes in required_nodes at least once.
    state = (node, seen_required) where seen_required is a tuple of visited required nodes.
    """
    key = (node, seen_required)
    if key in memo:
        return memo[key]

    # update requirement state
    if node in required_nodes:
        seen_required = tuple(sorted(set(seen_required) | {node}))

    if node == end:
        memo[key] = 1 if set(seen_required) == required_nodes else 0
        return memo[key]

    total = 0
    for nxt in graph.get(node, []):
        total += dfs_required(graph, nxt, end, required_nodes, seen_required, memo)

    memo[key] = total
    return total
