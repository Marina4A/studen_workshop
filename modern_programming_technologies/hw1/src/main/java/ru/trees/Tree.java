package ru.trees;

import java.util.ArrayList;
import java.util.List;

public class Tree {
    private Node root;

    public Node getRoot() {
        return root;
    }

    public void setRoot(Node root) {
        this.root = root;
    }

    public List<Node> getAllNodes() {
        List<Node> result = new ArrayList<>();
        traverse(root, result);
        return result;
    }

    public List<Node> getLeaves() {
        List<Node> result = new ArrayList<>();
        traverseLeaves(root, result);
        return result;
    }

    public int countLeaves() {
        return getLeaves().size();
    }

    private void traverse(Node node, List<Node> result) {
        result.add(node);
        for (Node child : node.getChildren()) {
            traverse(child, result);
        }
    }

    private void traverseLeaves(Node node, List<Node> result) {
        if (node.isLeaf()) {
            result.add(node);
        } else {
            for (Node child : node.getChildren()) {
                traverseLeaves(child, result);
            }
        }
    }
}