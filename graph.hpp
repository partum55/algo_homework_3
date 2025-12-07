#ifndef MIN_EDGE_COVER_HPP
#define MIN_EDGE_COVER_HPP

#include <vector>
#include <algorithm>
#include <stdexcept>
#include <queue>

struct Edge {
    int u, v;
    Edge(int u = 0, int v = 0) : u(u), v(v) {}

    bool operator==(const Edge& other) const {
        return (u == other.u && v == other.v) || (u == other.v && v == other.u);
    }
};

class MinEdgeCover {
private:
    int n;
    std::vector<Edge> edges;
    std::vector<std::vector<int>> adj;

    // find maximum matching
    std::vector<Edge> findMaxMatching() {
        std::vector<int> match(n, -1);
        std::vector<Edge> matching;

        // greedy algorithm for initial matching
        std::vector<bool> used(n, false);
        for (const auto& e : edges) {
            if (!used[e.u] && !used[e.v]) {
                match[e.u] = e.v;
                match[e.v] = e.u;
                used[e.u] = used[e.v] = true;
                matching.push_back(e);
            }
        }

        // improvement using augmenting paths
        bool improved = true;
        while (improved) {
            improved = false;
            std::vector<int> parent(n, -1);
            std::vector<bool> visited(n, false);
            std::queue<int> q;

            // find unmatched vertices
            for (int i = 0; i < n; i++) {
                if (match[i] == -1) {
                    q.push(i);
                    visited[i] = true;
                }
            }

            int pathEnd = -1;
            while (!q.empty() && pathEnd == -1) {
                int u = q.front();
                q.pop();

                for (int v : adj[u]) {
                    if (!visited[v]) {
                        visited[v] = true;
                        parent[v] = u;

                        if (match[v] == -1) {
                            pathEnd = v;
                            break;
                        } else {
                            q.push(match[v]);
                            visited[match[v]] = true;
                            parent[match[v]] = v;
                        }
                    }
                }
            }

            if (pathEnd != -1) {
                // augmenting path found
                improved = true;
                int v = pathEnd;
                while (parent[v] != -1) {
                    int u = parent[v];
                    int prev = parent[u];
                    match[v] = u;
                    match[u] = v;
                    v = prev;
                }

                // rebuild matching
                matching.clear();
                for (int i = 0; i < n; i++) {
                    if (match[i] != -1 && i < match[i]) {
                        matching.push_back(Edge(i, match[i]));
                    }
                }
            }
        }

        return matching;
    }

public:
    MinEdgeCover(int vertices, const std::vector<Edge>& edgeList)
        : n(vertices), edges(edgeList), adj(vertices) {

        if (vertices <= 0) {
            throw std::invalid_argument("Number of vertices must be positive");
        }

        // build adjacency list
        for (const auto& e : edges) {
            if (e.u < 0 || e.u >= n || e.v < 0 || e.v >= n) {
                throw std::invalid_argument("Invalid vertex index");
            }
            adj[e.u].push_back(e.v);
            adj[e.v].push_back(e.u);
        }

        // check for isolated vertices
        for (int i = 0; i < n; i++) {
            if (adj[i].empty()) {
                throw std::invalid_argument("Graph contains isolated vertices - edge cover impossible");
            }
        }
    }

    std::vector<Edge> solve() {
        std::vector<Edge> matching = findMaxMatching();
        std::vector<bool> covered(n, false);
        std::vector<Edge> result = matching;

        // mark covered vertices
        for (const auto& e : matching) {
            covered[e.u] = true;
            covered[e.v] = true;
        }

        // for each uncovered vertex, add any incident edge
        for (int i = 0; i < n; i++) {
            if (!covered[i]) {
                for (const auto& e : edges) {
                    if (e.u == i || e.v == i) {
                        result.push_back(e);
                        covered[i] = true;
                        covered[e.u] = true;
                        covered[e.v] = true;
                        break;
                    }
                }
            }
        }

        return result;
    }

    // check if the given set is an edge cover
    static bool isEdgeCover(int n, const std::vector<Edge>& cover) {
        std::vector<bool> covered(n, false);
        for (const auto& e : cover) {
            covered[e.u] = true;
            covered[e.v] = true;
        }
        for (int i = 0; i < n; i++) {
            if (!covered[i]) return false;
        }
        return true;
    }
};

#endif // MIN_EDGE_COVER_HPP