package ru.marina.hw41.tree;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Forest {
    private List<Tree> forest = new ArrayList<>();

    public List<Tree> getForest() {
        return forest;
    }

    public void readCsv(File file) {
        try (InputStream is = new FileInputStream(file);
             Scanner sc = new Scanner(is)) {
            int line = 1;
            while (sc.hasNextLine()) {
                String s = sc.nextLine();
                String[] pair = s.split(",");
                if (pair.length != 2) {
                    throw new RuntimeException("csv file \"" + file.getName() + "\"" +
                            " line #" + line +
                            ": number of elements equals to " + pair.length + " , but should be 2 (\"" + s + "\")");
                }
                int id = Integer.parseInt(pair[0].trim());
                int parent = Integer.parseInt(pair[1].trim());
                addNode(id, parent);
                line++;
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (NumberFormatException e) {
            throw new RuntimeException("invalid number " + e.getMessage(), e);
        }
    }

    private void addNode(int id, int parent) {
        if (id == parent) { // new Tree
            for (Tree t : forest) {
                if (t.getRoot().getId() == id) { // such a tree already exists
                    return;
                }
            }
            forest.add(new Tree(id));
            return;
        }
        for (Tree t : forest) {
            List<Node> nodes = t.getNodes();
            for (Node n : nodes) {
                if (n.getId() == parent) {
                    n.add(id);
                }
            }
        }
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("forest of ").append(forest.size()).append(" trees:");
        int treeCounter = 0;
        for (Tree t: forest) {
            sb.append("\n  tree #").append(treeCounter++).append(": ");
            int nodeCounter = 0;
            for (Node n : t.getNodes()) {
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
