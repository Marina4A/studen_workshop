package ru.trees;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.sql.*;


public class Main {
    public static void main(String[] args) {

        /* try
        {
            createDb();
        } catch (SQLException e)
        {
            e.printStackTrace();
        } catch (IOException e)
        {
            e.printStackTrace();
        } // */

        List<Tree> trees = readTreesFromDb();
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
        writeResultToFile(maxLeavesTreeId, maxLeaves, multipleMaxLeavesTrees); // */
    }

    static void createDb() throws SQLException, IOException
    {
        String filename = "input.csv";

        Connection conn = DriverManager.getConnection( "jdbc:h2:./tree", "sa", "" );
        Statement q = conn.createStatement();

        q.execute( "create schema if not exists treedb" );

        q.execute("drop table if exists node");
        q.execute("CREATE TABLE node(ID INT, " +
                "parent_id int);");

        conn.commit();

        BufferedReader reader = new BufferedReader(new FileReader(filename));
        Map<Integer, Node> nodes = new HashMap<>();
        String line;
        while ((line = reader.readLine()) != null)
        {
            String[] tokens = line.split(",");
            int nodeId = parseInteger(tokens[0]);
            int parentId = parseInteger(tokens[1]);
            q.execute("insert into node (id, parent_id) values (" +
                    nodeId + ", " + parentId + ");" );
        }
        conn.commit();

        reader.close();
        conn.close();
    }

    static List<Tree> readTreesFromDb()
    {
        List<Tree> trees = new ArrayList<>();
        try
        {
            Connection conn = DriverManager.getConnection( "jdbc:h2:./tree", "sa", "" );
            Statement q = conn.createStatement();

            PreparedStatement stmt = conn.prepareStatement( "select id, parent_id from node;" );
            ResultSet rs = stmt.executeQuery();

            Map<Integer, Node> nodes = new HashMap<>();
            while (rs.next())
            {
                int nodeId = rs.getInt(1);
                int parentId = rs.getInt(2);

                addNode(nodes, nodeId, parentId);
            }

            for (Node node : nodes.values()) {
                if (node.isRoot()) {
                    trees.add(new Tree(node));
                }
            }
        } catch (SQLException e)
        {
            e.printStackTrace();
        }
        return trees;
    }

    /* private static List<Tree> readTreesFromFile(String filename) {
        List<Tree> trees = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            Map<Integer, Node> nodes = new HashMap<>();
            String line;
            while ((line = reader.readLine()) != null) {
                String[] tokens = line.split(",");
                int nodeId = parseInteger(tokens[0]);
                int parentId = parseInteger(tokens[1]);
                addNode(nodes, nodeId, parentId);
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
    } // */

    private static void addNode(Map<Integer, Node> nodes, int nodeId, int parentId)
    {
        Node node = nodes.getOrDefault(nodeId, new Node(nodeId));
        Node parent = nodes.getOrDefault(parentId, new Node(parentId));
        node.setParent(parent);
        parent.getChildren().add(node);
        nodes.put(nodeId, node);
        nodes.put(parentId, parent);
    }

    private static int parseInteger(String value) {
        try {
            return Integer.parseInt(value);
        } catch (NumberFormatException e) {
            return 0; // Возвращаем 0, если не удалось преобразовать в число
        }
    }

    private static void writeResultToFile(int treeId, int numLeaves, boolean multipleTrees) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("output.csv"))) {
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