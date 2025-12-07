#include <iostream>
#include <fstream>
#include <iomanip>
#include "graph.hpp"

void printEdges(const std::vector<Edge>& edges) {
    std::cout << "Edges: ";
    for (size_t i = 0; i < edges.size(); i++) {
        std::cout << "(" << edges[i].u << ", " << edges[i].v << ")";
        if (i < edges.size() - 1) std::cout << ", ";
    }
    std::cout << std::endl;
}

void saveToFile(const std::string& filename, int n, const std::vector<Edge>& allEdges,
                const std::vector<Edge>& cover) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Failed to open file for writing: " << filename << std::endl;
        return;
    }

    file << n << " " << allEdges.size() << " " << cover.size() << std::endl;

    // All graph edges
    for (const auto& e : allEdges) {
        file << e.u << " " << e.v << std::endl;
    }

    // Cover edges (for highlighting)
    for (const auto& e : cover) {
        file << e.u << " " << e.v << std::endl;
    }

    file.close();
    std::cout << "Data saved to file: " << filename << std::endl;
}

void example1() {
    std::cout << "\n=== Example 1: Simple Graph ===" << std::endl;

    int n = 5;
    std::vector<Edge> edges = {
        {0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 0}, {1, 3}
    };

    std::cout << "Number of vertices: " << n << std::endl;
    std::cout << "Number of edges: " << edges.size() << std::endl;
    printEdges(edges);

    MinEdgeCover mec(n, edges);
    std::vector<Edge> cover = mec.solve();

    std::cout << "\nMinimum Edge Cover:" << std::endl;
    std::cout << "Number of edges in cover: " << cover.size() << std::endl;
    printEdges(cover);

    std::cout << "Verification: " << (MinEdgeCover::isEdgeCover(n, cover) ? "CORRECT" : "ERROR") << std::endl;

    saveToFile("graph1.txt", n, edges, cover);
}

void example2() {
    std::cout << "\n=== Example 2: Complete Graph K4 ===" << std::endl;

    int n = 4;
    std::vector<Edge> edges = {
        {0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}
    };

    std::cout << "Number of vertices: " << n << std::endl;
    std::cout << "Number of edges: " << edges.size() << std::endl;
    printEdges(edges);

    MinEdgeCover mec(n, edges);
    std::vector<Edge> cover = mec.solve();

    std::cout << "\nMinimum Edge Cover:" << std::endl;
    std::cout << "Number of edges in cover: " << cover.size() << std::endl;
    printEdges(cover);

    std::cout << "Verification: " << (MinEdgeCover::isEdgeCover(n, cover) ? "CORRECT" : "ERROR") << std::endl;

    saveToFile("graph2.txt", n, edges, cover);
}

void example3() {
    std::cout << "\n=== Example 3: Tree ===" << std::endl;

    int n = 7;
    std::vector<Edge> edges = {
        {0, 1}, {0, 2}, {1, 3}, {1, 4}, {2, 5}, {2, 6}
    };

    std::cout << "Number of vertices: " << n << std::endl;
    std::cout << "Number of edges: " << edges.size() << std::endl;
    printEdges(edges);

    MinEdgeCover mec(n, edges);
    std::vector<Edge> cover = mec.solve();

    std::cout << "\nMinimum Edge Cover:" << std::endl;
    std::cout << "Number of edges in cover: " << cover.size() << std::endl;
    printEdges(cover);

    std::cout << "Verification: " << (MinEdgeCover::isEdgeCover(n, cover) ? "CORRECT" : "ERROR") << std::endl;

    saveToFile("graph3.txt", n, edges, cover);
}

void customInput() {
    std::cout << "\n=== Custom Input ===" << std::endl;

    int n, m;
    std::cout << "Enter number of vertices: ";
    std::cin >> n;
    std::cout << "Enter number of edges: ";
    std::cin >> m;

    std::vector<Edge> edges;
    std::cout << "Enter edges (u v):" << std::endl;
    for (int i = 0; i < m; i++) {
        int u, v;
        std::cin >> u >> v;
        edges.push_back({u, v});
    }

    try {
        MinEdgeCover mec(n, edges);
        std::vector<Edge> cover = mec.solve();

        std::cout << "\nMinimum Edge Cover:" << std::endl;
        std::cout << "Number of edges in cover: " << cover.size() << std::endl;
        printEdges(cover);

        std::cout << "Verification: " << (MinEdgeCover::isEdgeCover(n, cover) ? "CORRECT" : "ERROR") << std::endl;

        saveToFile("graph_custom.txt", n, edges, cover);
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
}

int main() {
    std::cout << "╔════════════════════════════════════════════════════╗" << std::endl;
    std::cout << "║      Minimum Edge Cover in General Graph          ║" << std::endl;
    std::cout << "╚════════════════════════════════════════════════════╝" << std::endl;

    example1();
    example2();
    example3();

    std::cout << "\n" << std::string(54, '=') << std::endl;
    std::cout << "Would you like to enter your own graph? (y/n): ";
    char choice;
    std::cin >> choice;

    if (choice == 'y' || choice == 'Y') {
        customInput();
    }

    std::cout << "\nDone! Files graph1.txt, graph2.txt, graph3.txt created." << std::endl;
    std::cout << "Run visualize.py for visualization." << std::endl;

    return 0;
}