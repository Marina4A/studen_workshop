package ru.marina.hw42.tree;

import java.util.ArrayList;
import java.util.List;

public class Tree {
    private final Node root = new Node(-1);

    public Node getRoot() {
        return root;
    }

    public List<Node> getSubTrees() {
        return root.getChildren();
    }

    private void getNodesRecursive(List<Node> l, Node r) {
        l.add(r);
        for (Node n : r.getChildren()) {
            getNodesRecursive(l, n);
        }
    }

    private void getLeavesRecursive(List<Node> l, Node n) {
        if (n.isLeaf()) {
            l.add(n);
            return;
        }
        for (Node c : n.getChildren()) {
            getNodesRecursive(l, c);
        }
    }

    public List<Node> getAllNodes(Node subtree) {
        List<Node> l = new ArrayList<>();
        getNodesRecursive(l, subtree);
        return l;
    }

    public List<Node> getAllNodes() {
        List<Node> l = new ArrayList<>();
        for (Node n : root.getChildren()) {
            getNodesRecursive(l, n);
        }
        return l;
    }

    public List<Node> getAllLeaves(Node subtree) {
        List<Node> l = new ArrayList<>();
        getLeavesRecursive(l, subtree);
        return l;
    }

    public List<Node> getAllLeaves() {
        List<Node> l = new ArrayList<>();
        for (Node n : root.getChildren()) {
            getLeavesRecursive(l, n);
        }
        return l;
    }

    /**
     * @param node   current node to check for being parent
     * @param id     of node to insert
     * @param parent id of parent
     * @return true if new node was inserted or was already presented in tree,
     * otherwise parent is not found in the tree
     */
    private boolean addNodeRecursive(Node node, long id, long parent) {
        if (node.getId() == parent) {
            for (Node n : node.getChildren()) {
                if (n.getId() == id) { // already presented in children
                    throw new RuntimeException("Node with id " + id + " already exists");
                }
            }
            node.add(id);
            return true;
        }
        for (Node n : node.getChildren()) {
            if (addNodeRecursive(n, id, parent)) {
                return true;
            }
        }
        return false;
    }

    public void addNode(long id, long parent) {
        if (id == parent) { // new subTree
            for (Node n : root.getChildren()) {
                if (n.getId() == id) { // such subtree already exists
                    throw new RuntimeException("inserting node with id " + id + " already exists");
                }
            }
            root.add(id);
            return;
        }
        for (Node t : root.getChildren()) {
            if (addNodeRecursive(t, id, parent)) {
                return;
            }
        }
        throw new RuntimeException("inserting node with id " + id + " no parent node with id " + parent);
    }

    private void deleteNodeRecursive(Node node) {
        for (Node n : node.getChildren()) {
            deleteNodeRecursive(n);
        }
        TreeUtils.deletFromDB(node.getId());
    }

    public void delete(Node node) {
        deleteNodeRecursive(node);
        node.getParent().getChildren().remove(node);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("forest of ").append(root.getChildren().size()).append(" trees:");
        int treeCounter = 0;
        for (Node t : root.getChildren()) {
            sb.append("\n  tree #").append(treeCounter++).append(": ");
            int nodeCounter = 0;
            for (Node n : t.getChildren()) {
                if (nodeCounter++ != 0) {
                    sb.append(' ');
                }
                Node p = n.getParent();
                sb.append('(').append(n.getId());
                if (p != null) {
                    sb.append(", ").append(p.getId());
                }
                sb.append(')');
            }
            sb.append('\n');
        }
        return sb.toString();
    }
}
