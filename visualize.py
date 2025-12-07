#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import sys

def read_graph_data(filename):
    """Read graph data from file"""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        # First line: n m k (vertices, all edges, cover edges)
        n, m, k = map(int, lines[0].strip().split())

        # Next m lines - all edges
        all_edges = []
        for i in range(1, m + 1):
            u, v = map(int, lines[i].strip().split())
            all_edges.append((u, v))

        # Next k lines - cover edges
        cover_edges = []
        for i in range(m + 1, m + 1 + k):
            u, v = map(int, lines[i].strip().split())
            cover_edges.append((u, v))

        return n, all_edges, cover_edges
    except FileNotFoundError:
        print(f"Error: file {filename} not found")
        return None, None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None, None

def visualize_graph(n, all_edges, cover_edges, title="Graph"):
    """Visualize graph with edge cover highlighting"""

    # Create graph
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(all_edges)

    # Setup figure
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))

    # Vertex positions (use spring layout for better display)
    if n <= 8:
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    else:
        pos = nx.kamada_kawai_layout(G)

    # Draw all edges with thin gray lines
    nx.draw_networkx_edges(G, pos, edgelist=all_edges,
                           width=1.5, alpha=0.3, edge_color='gray',
                           style='dashed', ax=ax)

    # Draw cover edges with thick red lines
    nx.draw_networkx_edges(G, pos, edgelist=cover_edges,
                           width=4, alpha=0.8, edge_color='#e74c3c',
                           ax=ax)

    # Draw vertices
    nx.draw_networkx_nodes(G, pos, node_color='#3498db',
                           node_size=700, alpha=0.9, ax=ax)

    # Draw vertex labels
    nx.draw_networkx_labels(G, pos, font_size=14,
                            font_color='white', font_weight='bold',
                            ax=ax)

    # Title and information
    info_text = f"Vertices: {n} | Total edges: {len(all_edges)} | Edges in cover: {len(cover_edges)}"
    ax.set_title(f"{title}\n{info_text}", fontsize=16, fontweight='bold', pad=20)

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='gray', linestyle='--', linewidth=2,
               label='Other edges', alpha=0.5),
        Line2D([0], [0], color='#e74c3c', linewidth=4,
               label='Minimum cover', alpha=0.8)
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11)

    # Add information box
    textstr = f'Cover size: {len(cover_edges)}\n'
    textstr += f'Efficiency: {len(cover_edges)}/{len(all_edges)} '
    textstr += f'({100*len(cover_edges)/len(all_edges):.1f}%)'

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)

    ax.axis('off')
    plt.tight_layout()

    return fig

def main():
    """Main function"""

    # List of files for visualization
    files = ['graph1.txt', 'graph2.txt', 'graph3.txt']
    titles = ['Example 1: Simple Graph',
              'Example 2: Complete Graph K4',
              'Example 3: Tree']

    # Check for command line argument
    if len(sys.argv) > 1:
        files = [sys.argv[1]]
        titles = ['Custom Graph']

    for filename, title in zip(files, titles):
        print(f"\nVisualizing: {filename}")
        n, all_edges, cover_edges = read_graph_data(filename)

        if n is not None:
            fig = visualize_graph(n, all_edges, cover_edges, title)

            # Save to file
            output_name = filename.replace('.txt', '.png')
            plt.savefig(output_name, dpi=150, bbox_inches='tight')
            print(f"Saved: {output_name}")

            plt.show()
        else:
            print(f"Skipping {filename}")

    print("\n✓ Visualization complete!")

if __name__ == "__main__":
    print("═" * 60)
    print("  Minimum Edge Cover Visualization")
    print("═" * 60)

    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()