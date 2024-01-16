package ru.marina.tree;

import java.util.ArrayList;
import java.util.List;

public class Node {
    private final int id;

    private Node parent = null;

    private final List<Node> children = new ArrayList<>();

    public Node(int id) {
        this.id = id;
    }

    public boolean isLeaf() {
        return children.isEmpty();
    }

    public void add(int child) {
        for (Node n : children) {
            if (n.id == child) {
                return;
            }
        }
        Node newNode = new Node(child);
        newNode.parent = this;
        children.add(newNode);
    }

    public List<Node> getChildren() {
        return children;
    }

    public int getId() {
        return id;
    }

    public Node getParent() {
        return parent;
    }

    @Override
    public String toString() {
        if (parent == null) {
            return "Trees";
        }
        return Integer.toString(id);
    }
}
