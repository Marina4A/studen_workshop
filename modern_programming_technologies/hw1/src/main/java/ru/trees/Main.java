package ru.trees;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.List;

public class Main {
    public static void main(String[] args) throws Exception {
        try {
            List<int[]> data = readInput("input.csv");
            List<Tree> trees = TreeBuilder.buildTrees(data);
            int treeId = TreeFinder.findTreeWithMaxLeaves(trees);
            int leaves = trees.stream()
                    .filter(tree -> tree.getRoot().getId() == treeId)
                    .findFirst()
                    .orElseThrow()
                    .countLeaves();
            writeOutput("output.csv", treeId, leaves);
        } catch (Exception e) {
//            e.printStackTrace();
            writeOutput("output.csv", 0, 0);
        }
    }

    private static List<int[]> readInput(String filename) throws Exception {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            return reader.lines()
                    .map(line -> line.split(","))
                    .map(parts -> new int[]{Integer.parseInt(parts[0].replace("\"", "")), Integer.parseInt(parts[1].replace("\"", ""))})
                    .toList();
        }
    }

    private static void writeOutput(String filename, int treeId, int leaves) throws Exception {
        try (FileWriter writer = new FileWriter(filename)) {
            if (treeId == 0) {
                writer.write("0,0\n");
            } else {
                writer.write(treeId + "," + leaves + "\n");
            }
        }
    }
}