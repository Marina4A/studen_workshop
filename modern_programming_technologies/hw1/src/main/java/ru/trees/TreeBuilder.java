package ru.trees;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TreeBuilder {
    public static List<Tree> buildTrees(List<int[]> data) {
        Map<Integer, Node> nodes = new HashMap<>();
        for (int[] row : data) {
            int id = row[0];
            int parentId = row[1];
            Node node = nodes.get(id);
            if (node == null) {
                node = new Node(id);
                nodes.put(id, node);
            }
            if (parentId != id) {
                Node parent = nodes.get(parentId);
                if (parent == null) {
                    parent = new Node(parentId);
                    nodes.put(parentId, parent);
                }
                node.setParent(parent);
                parent.getChildren().add(node);
            }
        }
        List<Tree> trees = new ArrayList<>();
        for (Node node : nodes.values()) {
            if (node.isRoot()) {
                Tree tree = new Tree();
                tree.setRoot(node);
                trees.add(tree);
            }
        }
        return trees;
    }
}