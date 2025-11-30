import networkx as nx
import time
import random

def find_min_edge_cover_networkx(edges, num_vertices):
    """
    Finds minimum edge cover using NetworkX
    """
    G = nx.Graph()
    G.add_nodes_from(range(num_vertices))
    G.add_edges_from(edges)

    # Check for isolated vertices
    if not nx.is_empty(G) and any(G.degree(v) == 0 for v in G.nodes()):
        print("Error: graph contains isolated vertices!")
        return None

    try:
        start = time.time()
        cover = nx.min_edge_cover(G)
        end = time.time()
        return cover, (end - start) * 1000000  # in microseconds
    except nx.NetworkXException as e:
        print(f"NetworkX error: {e}")
        return None

def verify_edge_cover(edges, num_vertices, cover):
    """
    Verifies if the set 'cover' is a valid edge cover
    """
    covered_vertices = set()
    for u, v in cover:
        covered_vertices.add(u)
        covered_vertices.add(v)

    # Check if all vertices are covered
    all_vertices = set(range(num_vertices))
    if covered_vertices != all_vertices:
        return False, f"Not all vertices covered. Covered: {covered_vertices}, All: {all_vertices}"

    return True, "OK"

# Test 1: Triangle
print("=== Test 1: Triangle ===")
edges1 = [(0, 1), (1, 2), (2, 0)]
result1 = find_min_edge_cover_networkx(edges1, 3)
if result1:
    cover1, time1 = result1
    print(f"NetworkX result: {sorted(cover1)}")
    print(f"Cover size: {len(cover1)}")
    print(f"Execution time: {time1:.2f} μs")
    print(f"Expected: 2 edges (formula: |V| - |max_matching| = 3 - 1 = 2)")
print()

# Test 2: Complete graph K4
print("=== Test 2: Complete graph K4 ===")
edges2 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
result2 = find_min_edge_cover_networkx(edges2, 4)
if result2:
    cover2, time2 = result2
    print(f"NetworkX result: {sorted(cover2)}")
    print(f"Cover size: {len(cover2)}")
    print(f"Execution time: {time2:.2f} μs")
    print(f"Expected: 2 edges (formula: |V| - |max_matching| = 4 - 2 = 2)")
print()

# Test 3: Path with 5 vertices
print("=== Test 3: Path (0-1-2-3-4) ===")
edges3 = [(0, 1), (1, 2), (2, 3), (3, 4)]
result3 = find_min_edge_cover_networkx(edges3, 5)
if result3:
    cover3, time3 = result3
    print(f"NetworkX result: {sorted(cover3)}")
    print(f"Cover size: {len(cover3)}")
    print(f"Execution time: {time3:.2f} μs")
    print(f"Expected: 3 edges (formula: |V| - |max_matching| = 5 - 2 = 3)")
print()

# Test 4: Graph from file
print("=== Test 4: Graph from file ===")
edges4 = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5)]
result4 = find_min_edge_cover_networkx(edges4, 6)
if result4:
    cover4, time4 = result4
    print(f"NetworkX result: {sorted(cover4)}")
    print(f"Cover size: {len(cover4)}")
    print(f"Execution time: {time4:.2f} μs")
print()

# Additional test: large random graph
print("=== Test 5: Large random graph ===")
random.seed(42)
n = 100
edges5 = []
for i in range(n):
    for j in range(i+1, n):
        if random.random() < 0.1:  # 10% chance of an edge
            edges5.append((i, j))

print(f"Vertices: {n}, Edges: {len(edges5)}")
result5 = find_min_edge_cover_networkx(edges5, n)
if result5:
    cover5, time5 = result5
    print(f"Cover size: {len(cover5)}")
    print(f"Execution time: {time5:.2f} μs")
    is_valid, msg = verify_edge_cover(edges5, n, cover5)
    print(f"Validation: {msg}")

# Comparison instructions with C++ implementation
print("\n=== Comparison Instructions ===")
print("1. Run the C++ program and save the results")
print("2. Compare edge cover sizes")
print("3. Compare execution times")
print("4. Verify that both programs give the same size (though edges themselves may differ)")
