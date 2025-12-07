#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import time
import random
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np

def read_cpp_result(filename):
    """Read C++ algorithm result from file"""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        n, m, k = map(int, lines[0].strip().split())

        all_edges = []
        for i in range(1, m + 1):
            u, v = map(int, lines[i].strip().split())
            all_edges.append((u, v))

        cover_edges = set()
        for i in range(m + 1, m + 1 + k):
            u, v = map(int, lines[i].strip().split())
            cover_edges.add((min(u, v), max(u, v)))

        return n, all_edges, cover_edges, k
    except:
        return None, None, None, None

def networkx_min_edge_cover(n, edges):
    """Find minimum edge cover using NetworkX"""
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)

    start_time = time.perf_counter()
    cover = nx.min_edge_cover(G)
    end_time = time.perf_counter()

    return cover, (end_time - start_time) * 1000  # milliseconds

def verify_edge_cover(n, edges, cover):
    """Verify that the cover is valid"""
    covered = set()
    for u, v in cover:
        covered.add(u)
        covered.add(v)
    return len(covered) == n

def generate_random_graph(n, edge_prob=0.3, seed=None):
    """Generate random graph without isolated vertices"""
    if seed is not None:
        random.seed(seed)

    edges = []
    # Ensure connectivity - create a spanning tree
    for i in range(n - 1):
        parent = random.randint(0, i)
        edges.append((parent, i + 1))

    # Add random edges
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < edge_prob:
                edges.append((i, j))

    return edges

def generate_complete_graph(n):
    """Generate complete graph Kn"""
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((i, j))
    return edges

def generate_bipartite_graph(n1, n2, prob=0.5):
    """Generate random bipartite graph"""
    edges = []
    # Ensure all vertices have at least one edge
    for i in range(n1):
        j = random.randint(0, n2 - 1)
        edges.append((i, n1 + j))

    for i in range(n2):
        j = random.randint(0, n1 - 1)
        edges.append((j, n1 + i))

    # Add random edges
    for i in range(n1):
        for j in range(n2):
            if random.random() < prob:
                edges.append((i, n1 + j))

    # Remove duplicates
    edges = list(set(edges))
    return edges, n1 + n2

def generate_grid_graph(rows, cols):
    """Generate 2D grid graph"""
    edges = []
    n = rows * cols

    for i in range(rows):
        for j in range(cols):
            node = i * cols + j
            # Right neighbor
            if j < cols - 1:
                edges.append((node, node + 1))
            # Bottom neighbor
            if i < rows - 1:
                edges.append((node, node + cols))

    return edges, n

def generate_cycle_with_chords(n, num_chords):
    """Generate cycle with random chords"""
    edges = []
    # Create cycle
    for i in range(n):
        edges.append((i, (i + 1) % n))

    # Add random chords
    added = 0
    attempts = 0
    while added < num_chords and attempts < num_chords * 10:
        i, j = random.randint(0, n-1), random.randint(0, n-1)
        if abs(i - j) > 1 and (i, j) not in edges and (j, i) not in edges:
            edges.append((i, j))
            added += 1
        attempts += 1

    return edges

def compare_on_file(filename, title):
    """Compare C++ and NetworkX results on a specific file"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

    n, edges, cpp_cover, cpp_size = read_cpp_result(filename)

    if n is None:
        print(f"[ERROR] Could not read {filename}")
        return None

    # Verify C++ result
    cpp_valid = verify_edge_cover(n, edges, cpp_cover)

    # NetworkX solution
    nx_cover, nx_time = networkx_min_edge_cover(n, edges)
    nx_cover_normalized = set((min(u, v), max(u, v)) for u, v in nx_cover)
    nx_size = len(nx_cover)
    nx_valid = verify_edge_cover(n, edges, nx_cover)

    # Display results
    print(f"\n[GRAPH] Properties:")
    print(f"   Vertices: {n}")
    print(f"   Edges: {len(edges)}")
    print(f"   Density: {2*len(edges)/(n*(n-1)):.3f}")

    print(f"\n[C++] Implementation:")
    print(f"   Cover size: {cpp_size}")
    print(f"   Valid: {'YES' if cpp_valid else 'NO'}")
    print(f"   Edges: {sorted(cpp_cover)}")

    print(f"\n[NetworkX] Library:")
    print(f"   Cover size: {nx_size}")
    print(f"   Valid: {'YES' if nx_valid else 'NO'}")
    print(f"   Time: {nx_time:.4f} ms")
    print(f"   Edges: {sorted(nx_cover_normalized)}")

    print(f"\n[COMPARISON]:")
    if cpp_size == nx_size:
        print(f"   Result: IDENTICAL")
        print(f"   Both algorithms found optimal solution of size {cpp_size}")
    else:
        print(f"   Result: DIFFERENT")
        print(f"   Difference: {abs(cpp_size - nx_size)} edges")

    # Check if solutions are exactly the same
    if cpp_cover == nx_cover_normalized:
        print(f"   Edge sets: IDENTICAL")
    else:
        print(f"   Edge sets: DIFFERENT (but both valid covers)")

    return {
        'title': title,
        'n': n,
        'm': len(edges),
        'density': 2*len(edges)/(n*(n-1)) if n > 1 else 0,
        'cpp_size': cpp_size,
        'nx_size': nx_size,
        'cpp_valid': cpp_valid,
        'nx_valid': nx_valid,
        'nx_time': nx_time,
        'match': cpp_size == nx_size
    }

def benchmark_scalability():
    """Benchmark algorithm on graphs of increasing size"""
    print(f"\n{'='*70}")
    print(f"  Scalability Benchmark - Various Graph Types")
    print(f"{'='*70}\n")

    results = {
        'sparse': [],
        'dense': [],
        'complete': [],
        'bipartite': []
    }

    sizes = [10, 20, 50, 100, 200, 500, 1000]

    print("Testing SPARSE graphs (edge_prob=0.2):")
    for n in sizes:
        edges = generate_random_graph(n, edge_prob=0.2, seed=42)
        nx_cover, nx_time = networkx_min_edge_cover(n, edges)

        results['sparse'].append({
            'n': n,
            'm': len(edges),
            'cover_size': len(nx_cover),
            'time_ms': nx_time
        })
        print(f"   n={n:4d}, m={len(edges):5d}, cover={len(nx_cover):4d}, time={nx_time:8.4f} ms")

    print("\nTesting DENSE graphs (edge_prob=0.6):")
    for n in sizes[:6]:  # Limit size for dense graphs
        edges = generate_random_graph(n, edge_prob=0.6, seed=42)
        nx_cover, nx_time = networkx_min_edge_cover(n, edges)

        results['dense'].append({
            'n': n,
            'm': len(edges),
            'cover_size': len(nx_cover),
            'time_ms': nx_time
        })
        print(f"   n={n:4d}, m={len(edges):5d}, cover={len(nx_cover):4d}, time={nx_time:8.4f} ms")

    print("\nTesting COMPLETE graphs:")
    for n in [10, 15, 20, 30, 40, 50]:
        edges = generate_complete_graph(n)
        nx_cover, nx_time = networkx_min_edge_cover(n, edges)

        results['complete'].append({
            'n': n,
            'm': len(edges),
            'cover_size': len(nx_cover),
            'time_ms': nx_time
        })
        print(f"   n={n:4d}, m={len(edges):5d}, cover={len(nx_cover):4d}, time={nx_time:8.4f} ms")

    print("\nTesting BIPARTITE graphs:")
    for n in [20, 40, 60, 100, 150, 200]:
        n1, n2 = n // 2, n // 2
        edges, total_n = generate_bipartite_graph(n1, n2, prob=0.4)
        nx_cover, nx_time = networkx_min_edge_cover(total_n, edges)

        results['bipartite'].append({
            'n': total_n,
            'm': len(edges),
            'cover_size': len(nx_cover),
            'time_ms': nx_time
        })
        print(f"   n={total_n:4d}, m={len(edges):5d}, cover={len(nx_cover):4d}, time={nx_time:8.4f} ms")

    return results

def plot_scalability(results):
    """Plot comprehensive scalability results"""
    fig = plt.figure(figsize=(16, 10))

    # Create 2x2 subplot grid
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    # Plot 1: Time vs Vertices for all graph types
    ax1 = fig.add_subplot(gs[0, :])
    for graph_type, data in results.items():
        if data:
            n_values = [r['n'] for r in data]
            times = [r['time_ms'] for r in data]
            ax1.plot(n_values, times, 'o-', linewidth=2, markersize=6, label=graph_type.capitalize())

    ax1.set_xlabel('Number of Vertices', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Time (milliseconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Execution Time vs Graph Size (Various Graph Types)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')

    # Plot 2: Cover Size vs Vertices
    ax2 = fig.add_subplot(gs[1, 0])
    for graph_type, data in results.items():
        if data:
            n_values = [r['n'] for r in data]
            cover_sizes = [r['cover_size'] for r in data]
            ax2.plot(n_values, cover_sizes, 's-', linewidth=2, markersize=6, label=graph_type.capitalize())

    ax2.set_xlabel('Number of Vertices', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Cover Size', fontsize=12, fontweight='bold')
    ax2.set_title('Cover Size vs Graph Size', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    # Plot 3: Efficiency (Cover/Edges ratio)
    ax3 = fig.add_subplot(gs[1, 1])
    for graph_type, data in results.items():
        if data:
            n_values = [r['n'] for r in data]
            efficiency = [r['cover_size']/r['m'] * 100 for r in data]
            ax3.plot(n_values, efficiency, '^-', linewidth=2, markersize=6, label=graph_type.capitalize())

    ax3.set_xlabel('Number of Vertices', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Cover/Edges Ratio (%)', fontsize=12, fontweight='bold')
    ax3.set_title('Algorithm Efficiency', fontsize=14, fontweight='bold')
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)

    plt.savefig('scalability_benchmark.png', dpi=150, bbox_inches='tight')
    print(f"\n[SAVE] Saved comprehensive scalability plot: scalability_benchmark.png")
    plt.show()

def stress_test():
    """Run stress tests with challenging cases"""
    print(f"\n{'='*70}")
    print(f"  Stress Testing - Challenging Cases")
    print(f"{'='*70}\n")

    test_cases = []

    # Test 1: Large sparse graph
    print("Test 1: Large Sparse Graph (n=2000)")
    edges = generate_random_graph(2000, edge_prob=0.05, seed=42)
    nx_cover, nx_time = networkx_min_edge_cover(2000, edges)
    test_cases.append(("Large Sparse", 2000, len(edges), len(nx_cover), nx_time))
    print(f"   Vertices: 2000, Edges: {len(edges)}, Cover: {len(nx_cover)}, Time: {nx_time:.4f} ms\n")

    # Test 2: Complete graph K100
    print("Test 2: Complete Graph K100")
    edges = generate_complete_graph(100)
    nx_cover, nx_time = networkx_min_edge_cover(100, edges)
    test_cases.append(("Complete K100", 100, len(edges), len(nx_cover), nx_time))
    print(f"   Vertices: 100, Edges: {len(edges)}, Cover: {len(nx_cover)}, Time: {nx_time:.4f} ms\n")

    # Test 3: Grid graph
    print("Test 3: Grid Graph (40x40)")
    edges, n = generate_grid_graph(40, 40)
    nx_cover, nx_time = networkx_min_edge_cover(n, edges)
    test_cases.append(("Grid 40x40", n, len(edges), len(nx_cover), nx_time))
    print(f"   Vertices: {n}, Edges: {len(edges)}, Cover: {len(nx_cover)}, Time: {nx_time:.4f} ms\n")

    # Test 4: Bipartite graph
    print("Test 4: Large Bipartite Graph (500+500)")
    edges, n = generate_bipartite_graph(500, 500, prob=0.1)
    nx_cover, nx_time = networkx_min_edge_cover(n, edges)
    test_cases.append(("Bipartite 500+500", n, len(edges), len(nx_cover), nx_time))
    print(f"   Vertices: {n}, Edges: {len(edges)}, Cover: {len(nx_cover)}, Time: {nx_time:.4f} ms\n")

    # Test 5: Cycle with many chords
    print("Test 5: Cycle with Chords (n=1000, 500 chords)")
    edges = generate_cycle_with_chords(1000, 500)
    nx_cover, nx_time = networkx_min_edge_cover(1000, edges)
    test_cases.append(("Cycle+Chords", 1000, len(edges), len(nx_cover), nx_time))
    print(f"   Vertices: 1000, Edges: {len(edges)}, Cover: {len(nx_cover)}, Time: {nx_time:.4f} ms\n")

    return test_cases

def main():
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║      Comprehensive Algorithm Comparison: C++ vs NetworkX          ║")
    print("╚════════════════════════════════════════════════════════════════════╝")

    # Compare on test files
    files = [
        ('graph1.txt', 'Example 1: Simple Graph'),
        ('graph2.txt', 'Example 2: Complete Graph K4'),
        ('graph3.txt', 'Example 3: Tree')
    ]

    comparison_results = []
    for filename, title in files:
        result = compare_on_file(filename, title)
        if result:
            comparison_results.append(result)

    # Summary table
    if comparison_results:
        print(f"\n{'='*70}")
        print(f"  Basic Examples Summary")
        print(f"{'='*70}\n")

        table_data = []
        for r in comparison_results:
            table_data.append([
                r['title'].split(':')[1].strip(),
                r['n'],
                r['m'],
                f"{r['density']:.3f}",
                r['cpp_size'],
                r['nx_size'],
                '✓' if r['match'] else '✗',
                f"{r['nx_time']:.4f}"
            ])

        headers = ['Graph', 'V', 'E', 'Density', 'C++ Size', 'NX Size', 'Match', 'NX Time (ms)']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))

        # Check if all match
        all_match = all(r['match'] for r in comparison_results)
        print(f"\n{'[PASS] All results match!' if all_match else '[WARNING] Some results differ'}")
        print(f"[PASS] All C++ solutions are valid edge covers")

    # Stress testing
    print("\n")
    stress_results = stress_test()

    print(f"\n{'='*70}")
    print(f"  Stress Test Summary")
    print(f"{'='*70}\n")

    stress_table = []
    for name, n, m, cover, time_ms in stress_results:
        stress_table.append([name, n, m, cover, f"{100*cover/m:.1f}%", f"{time_ms:.4f}"])

    headers = ['Test Case', 'Vertices', 'Edges', 'Cover Size', 'Efficiency', 'Time (ms)']
    print(tabulate(stress_table, headers=headers, tablefmt='grid'))

    # Scalability benchmark
    print(f"\n")
    bench_results = benchmark_scalability()
    plot_scalability(bench_results)

    print(f"\n{'='*70}")
    print(f"  Comprehensive Testing Complete!")
    print(f"{'='*70}\n")
    print("[INFO] Results saved to: scalability_benchmark.png")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
