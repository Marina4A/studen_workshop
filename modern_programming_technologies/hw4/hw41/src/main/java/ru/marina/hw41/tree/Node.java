package ru.marina.hw41.tree;

import lombok.Getter;
import java.util.ArrayList;
import java.util.List;

public class Node {
    @Getter
    private long id;

    @Getter
    private Node parent = null;

    @Getter
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
}
