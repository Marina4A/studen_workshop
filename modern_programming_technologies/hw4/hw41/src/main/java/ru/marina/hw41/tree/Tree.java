package ru.marina.hw41.tree;

import java.util.ArrayList;
import java.util.List;

public class Tree {
    private Node root = null;

    public Tree(int rootId) {
        root = new Node(rootId);
    }

    public Node getRoot() {
        return root;
    }

    private void _getNodes(List<Node> l, Node r) {
        l.add(r);
        for (Node n: r.getChildren()) {
            _getNodes(l, n);
        }
    }

    private void _getLeaves(List<Node> l, Node n) {
        if (n.isLeaf()) {
            l.add(n);
            return;
        }
        for (Node c: n.getChildren()) {
            _getNodes(l, c);
        }
    }

    public List<Node> getNodes() {
        List<Node> l = new ArrayList<>();
        _getNodes(l, root);
        return l;
    }

    public List<Node> getLeaves() {
        List<Node> l = new ArrayList<>();
        _getLeaves(l, root);
        return l;
    }
}
