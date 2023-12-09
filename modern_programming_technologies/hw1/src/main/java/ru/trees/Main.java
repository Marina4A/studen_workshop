package ru.trees;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        List<Tree> trees = readTreesFromFile("HW1/input.csv");
        int maxLeaves = 0;
        int maxLeavesTreeId = 0;
        boolean multipleMaxLeavesTrees = false;
        for (Tree tree : trees) {
            List<Node> leaves = tree.getAllLeaves();
            int numLeaves = leaves.size();
            if (numLeaves > maxLeaves) {
                maxLeaves = numLeaves;
                maxLeavesTreeId = tree.getRoot().getId();
                multipleMaxLeavesTrees = false;
            } else if (numLeaves == maxLeaves) {
                multipleMaxLeavesTrees = true;
            }
        }
        writeResultToFile(maxLeavesTreeId, maxLeaves, multipleMaxLeavesTrees);
    }

    private static List<Tree> readTreesFromFile(String filename) {
        List<Tree> trees = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            Map<Integer, Node> nodes = new HashMap<>();
            String line;
            while ((line = reader.readLine()) != null) {
                String[] tokens = line.split(",");
                int nodeId = parseInteger(tokens[0]);
                int parentId = parseInteger(tokens[1]);
                Node node = nodes.getOrDefault(nodeId, new Node(nodeId));
                Node parent = nodes.getOrDefault(parentId, new Node(parentId));
                node.setParent(parent);
                parent.getChildren().add(node);
                nodes.put(nodeId, node);
                nodes.put(parentId, parent);
            }
            for (Node node : nodes.values()) {
                if (node.isRoot()) {
                    trees.add(new Tree(node));
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return trees;
    }

    private static int parseInteger(String value) {
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException e) {
            return 0; // Возвращаем 0, если не удалось преобразовать в число
        }
    }

    private static void writeResultToFile(int treeId, int numLeaves, boolean multipleTrees) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("HW1/output.csv"))) {
            if (multipleTrees) {
                writer.write("0,0");
            } else {
                writer.write(treeId + "," + numLeaves);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}