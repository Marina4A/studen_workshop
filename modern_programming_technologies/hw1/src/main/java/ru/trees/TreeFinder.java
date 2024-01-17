package ru.trees;

import java.util.List;

public class TreeFinder {
    public static int findTreeWithMaxLeaves(List<Tree> trees) throws Exception {
        int maxLeaves = 0;
        int treeId = 0;
        boolean foundMoreThanOne = false;
        for (Tree tree : trees) {
            int leaves = tree.countLeaves();
            if (leaves > maxLeaves) {
                maxLeaves = leaves;
                treeId = tree.getRoot().getId();
                foundMoreThanOne = false;
            } else if (leaves == maxLeaves) {
                foundMoreThanOne = true;
            }
        }
        if (foundMoreThanOne) {
            throw new Exception("Multiple trees with max leaves");
        }
        return treeId;
    }
}