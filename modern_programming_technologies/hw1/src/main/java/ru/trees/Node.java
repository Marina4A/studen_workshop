package ru.trees;

import java.util.ArrayList;
import java.util.List;

public class Node {
    private int id;
    private Node parent;
    private List<Node> children;

    public Node(int id) {
        this.id = id;
        children = new ArrayList<>();
    }

    public int getId() {
        return id;
    }

    public Node getParent() {
        return parent;
    }

    public void setParent(Node parent) {
        this.parent = parent;
    }

    public List<Node> getChildren() {
        return children;
    }

    public boolean isLeaf() {
        return children.isEmpty();
    }

    public boolean isRoot() {
        return parent == null;
    }
}

