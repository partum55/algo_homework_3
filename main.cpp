#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <fstream>
#include <chrono>

using namespace std;

struct Edge {
    int u, v;
    Edge(int u, int v) : u(u), v(v) {}
    bool operator<(const Edge& other) const {
        if (u != other.u) return u < other.u;
        return v < other.v;
    }
};

class Graph {
private:
    int V; // number of vertices
    vector<vector<int>> adj; // adjacency list
    vector<Edge> edges; // list of edges

public:
    Graph(int V) : V(V) {
        adj.resize(V);
    }

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
        edges.push_back(Edge(min(u, v), max(u, v)));
    }

    // Check if there are isolated vertices
    bool hasIsolatedVertices() {
        for (int i = 0; i < V; i++) {
            if (adj[i].empty()) {
                return true;
            }
        }
        return false;
    }

    // DFS to find augmenting path in matching
    bool dfs(int v, vector<int>& match, vector<bool>& used) {
        for (int to : adj[v]) {
            if (used[to]) continue;
            used[to] = true;

            if (match[to] == -1 || dfs(match[to], match, used)) {
                match[to] = v;
                match[v] = to;
                return true;
            }
        }
        return false;
    }

    // Find maximum matching (Kuhn's algorithm)
    vector<int> findMaxMatching() {
        vector<int> match(V, -1);

        for (int v = 0; v < V; v++) {
            if (match[v] == -1) {
                vector<bool> used(V, false);
                dfs(v, match, used);
            }
        }

        return match;
    }

    // Find minimum edge cover
    set<Edge> findMinEdgeCover() {
        // Check for isolated vertices
        if (hasIsolatedVertices()) {
            cerr << "Error: graph contains isolated vertices. Edge cover does not exist!" << endl;
            return set<Edge>();
        }

        set<Edge> edgeCover;

        // Step 1: Find maximum matching
        vector<int> match = findMaxMatching();

        // Step 2: Add all edges from matching
        vector<bool> covered(V, false);
        for (int v = 0; v < V; v++) {
            if (match[v] != -1 && v < match[v]) {
                edgeCover.insert(Edge(v, match[v]));
                covered[v] = true;
                covered[match[v]] = true;
            }
        }

        // Step 3: For each uncovered vertex, add any incident edge
        for (int v = 0; v < V; v++) {
            if (!covered[v] && !adj[v].empty()) {
                int u = adj[v][0];
                edgeCover.insert(Edge(min(v, u), max(v, u)));
                covered[v] = true;
                covered[u] = true;
            }
        }

        return edgeCover;
    }

    void printGraph() {
        cout << "Graph has " << V << " vertices and " << edges.size() << " edges:" << endl;
        for (const auto& e : edges) {
            cout << "(" << e.u << ", " << e.v << ")" << endl;
        }
    }

    int getVertexCount() const { return V; }
    int getEdgeCount() const { return edges.size(); }
};

// Function to read graph from file
Graph readGraphFromFile(const string& filename) {
    ifstream fin(filename);
    int V, E;
    fin >> V >> E;

    Graph g(V);
    for (int i = 0; i < E; i++) {
        int u, v;
        fin >> u >> v;
        g.addEdge(u, v);
    }

    fin.close();
    return g;
}

// Function to create test graph
Graph createTestGraph1() {
    // Simple graph: triangle
    Graph g(3);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 0);
    return g;
}

Graph createTestGraph2() {
    // Complete graph K4
    Graph g(4);
    g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(0, 3);
    g.addEdge(1, 2);
    g.addEdge(1, 3);
    g.addEdge(2, 3);
    return g;
}

Graph createTestGraph3() {
    // Path with 5 vertices
    Graph g(5);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 3);
    g.addEdge(3, 4);
    return g;
}

int main() {
    cout << "=== Minimum Edge Cover ===" << endl << endl;

    // Test 1: Triangle
    cout << "--- Test 1: Triangle ---" << endl;
    Graph g1 = createTestGraph1();
    g1.printGraph();

    auto start = chrono::high_resolution_clock::now();
    set<Edge> cover1 = g1.findMinEdgeCover();
    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(end - start);

    cout << "\nMinimum edge cover (" << cover1.size() << " edges):" << endl;
    for (const auto& e : cover1) {
        cout << "(" << e.u << ", " << e.v << ")" << endl;
    }
    cout << "Execution time: " << duration.count() << " μs" << endl;
    cout << endl;

    // Test 2: Complete graph K4
    cout << "--- Test 2: Complete graph K4 ---" << endl;
    Graph g2 = createTestGraph2();
    g2.printGraph();

    start = chrono::high_resolution_clock::now();
    set<Edge> cover2 = g2.findMinEdgeCover();
    end = chrono::high_resolution_clock::now();
    duration = chrono::duration_cast<chrono::microseconds>(end - start);

    cout << "\nMinimum edge cover (" << cover2.size() << " edges):" << endl;
    for (const auto& e : cover2) {
        cout << "(" << e.u << ", " << e.v << ")" << endl;
    }
    cout << "Execution time: " << duration.count() << " μs" << endl;
    cout << endl;

    // Test 3: Path with 5 vertices
    cout << "--- Test 3: Path (0-1-2-3-4) ---" << endl;
    Graph g3 = createTestGraph3();
    g3.printGraph();

    start = chrono::high_resolution_clock::now();
    set<Edge> cover3 = g3.findMinEdgeCover();
    end = chrono::high_resolution_clock::now();
    duration = chrono::duration_cast<chrono::microseconds>(end - start);

    cout << "\nMinimum edge cover (" << cover3.size() << " edges):" << endl;
    for (const auto& e : cover3) {
        cout << "(" << e.u << ", " << e.v << ")" << endl;
    }
    cout << "Execution time: " << duration.count() << " μs" << endl;
    cout << endl;

    // Example of reading from file
    cout << "--- Reading graph from file ---" << endl;
    cout << "File format input.txt:" << endl;
    cout << "First line: V E (number of vertices and edges)" << endl;
    cout << "Next E lines: u v (edges)" << endl;

    // Create example file
    ofstream fout("input.txt");
    fout << "6 7" << endl;
    fout << "0 1" << endl;
    fout << "0 2" << endl;
    fout << "1 3" << endl;
    fout << "2 3" << endl;
    fout << "2 4" << endl;
    fout << "3 5" << endl;
    fout << "4 5" << endl;
    fout.close();

    Graph g4 = readGraphFromFile("input.txt");
    g4.printGraph();

    start = chrono::high_resolution_clock::now();
    set<Edge> cover4 = g4.findMinEdgeCover();
    end = chrono::high_resolution_clock::now();
    duration = chrono::duration_cast<chrono::microseconds>(end - start);

    cout << "\nMinimum edge cover (" << cover4.size() << " edges):" << endl;
    for (const auto& e : cover4) {
        cout << "(" << e.u << ", " << e.v << ")" << endl;
    }
    cout << "Execution time: " << duration.count() << " μs" << endl;

    return 0;
}
