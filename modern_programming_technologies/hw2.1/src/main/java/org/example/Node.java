package org.example;

import java.util.HashSet;
import java.util.Set;

public class Node {
    private int id;
    private Set<Node> children;

    public Node(int id) {
        this.id = id;
        this.children = new HashSet<>();
    }

    public int getId() {
        return id;
    }

    public Set<Node> getChildren() {
        return children;
    }

    public void addChild(Node child) {
        children.add(child);
    }
}