package org.example;

import java.util.*;
public class Graph {
    private Map<Integer, Node> nodes;

    public Graph() {
        this.nodes = new HashMap<>();
    }

    public void addEdge(int source, int target) {
        Node sourceNode = getNode(source);
        Node targetNode = getNode(target);
        sourceNode.addChild(targetNode);
    }

    private Node getNode(int id) {
        return nodes.computeIfAbsent(id, Node::new);
    }

    public boolean canTraverse() {
        Set<Node> visitedNodes = new HashSet<>();
        Set<Node> visitedGraphs = new HashSet<>();
        Set<Node> currentPath = new HashSet<>();

        for (Node node : nodes.values()) {
            if (!visitedNodes.contains(node) && !visitedGraphs.contains(node)) {
                if (hasCycle(node, visitedNodes, visitedGraphs, currentPath)) {
                    return true;
                }
            }
        }

        return true;
    }

    private boolean hasCycle(Node node, Set<Node> visitedNodes, Set<Node> visitedGraphs, Set<Node> currentPath) {
        visitedNodes.add(node);
        currentPath.add(node);

        Set<Node> children = node.getChildren();
        for (Node child : children) {
            if (currentPath.contains(child) || (!visitedNodes.contains(child) && !visitedGraphs.contains(child) && hasCycle(child, visitedNodes, visitedGraphs, currentPath))) {
                return true; // Обнаружен цикл
            }
        }

        currentPath.remove(node);
        visitedGraphs.add(node); // Пометить текущий узел как посещенный в текущем графе
        visitedNodes.remove(node); // Убрать узел из множества посещенных узлов

        return false;
    }
}