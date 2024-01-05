package ru.marina.hw42.tree;

import java.util.ArrayList;
import java.util.List;

public class Node {
    private long id;

    private Node parent = null;

    private final List<Node> children = new ArrayList<>();

    public Node(long id) {
        this.id = id;
    }

    public boolean isLeaf() {
        return children.isEmpty();
    }

    public boolean isRoot() {
        return parent == null;
    }

    public void add(long child) {
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

    public long getId() {
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
        return Long.toString(id);
    }
}
