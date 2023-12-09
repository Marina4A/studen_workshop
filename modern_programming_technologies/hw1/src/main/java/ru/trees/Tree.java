package ru.trees;

import java.util.ArrayList;
import java.util.List;

class Tree {
    private Node root;

    public Tree(Node root) {
        this.root = root;
    }

    public Node getRoot() {
        return root;
    }

    public List<Node> getAllNodes() {
        List<Node> nodes = new ArrayList<>();
        traverse(root, nodes);
        return nodes;
    }

    private void traverse(Node node, List<Node> nodes) {
        nodes.add(node);
        for (Node child : node.getChildren()) {
            traverse(child, nodes);
        }
    }

    public List<Node> getAllLeaves() {
        List<Node> leaves = new ArrayList<>();
        traverseLeaves(root, leaves);
        return leaves;
    }

    private void traverseLeaves(Node node, List<Node> leaves) {
        if (node.isLeaf()) {
            leaves.add(node);
        } else {
            for (Node child : node.getChildren()) {
                traverseLeaves(child, leaves);
            }
        }
    }
}
