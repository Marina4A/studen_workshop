package org.example.connection;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public abstract class DBConnection implements AutoCloseable {
    protected static final int[][] initialNodes = {
            {1, 2},
            {2, 3},
            {3, 4},
            {4, 1},

    };

    protected static final String userName = "userTree";
    protected static final String password = "pass";
    protected java.sql.Connection connection;

    public abstract void connect() throws SQLException;

    public void dropSchema() throws SQLException {
        String sql = "DROP TABLE IF EXISTS TREES CASCADE";
        try (Statement statement = connection.createStatement()) {
            statement.execute(sql);
        }
    }

    public void createSchema() throws SQLException {
        String sql = "CREATE TABLE TREES(id int PRIMARY KEY, parentId int)";
        try (Statement statement = connection.createStatement()) {
            statement.execute(sql);
        }
    }

    public void populateSchema() throws SQLException {
        String sql = "INSERT INTO TREES(id, parentId) VALUES (?, ?)";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            for (int[] node : initialNodes) {
                statement.setInt(1, node[0]);
                statement.setInt(2, node[1]);
                statement.executeUpdate();
            }
        }
    }

    public void insertNode(int id, int parentId) throws SQLException {
        String sql = "INSERT INTO TREES(id, parentId) VALUES (?, ?)";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            statement.setInt(2, parentId);
            statement.executeUpdate();
        }
    }

    public void deleteNode(int id) throws SQLException {
        String sql = "DELETE FROM TREES WHERE id = ?";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            statement.executeUpdate();
        }
    }

    public List<int[]> readTree() throws SQLException {
        String sql = "SELECT id, parentId FROM TREES";
        try (Statement statement = connection.createStatement()) {
            ResultSet rs = statement.executeQuery(sql);
            List<int[]> list = new ArrayList<>();
            while (rs.next()) {
                int[] node = {rs.getInt("id"), rs.getInt("parentId")};
                list.add(node);
            }
            return list;
        }
    }

    @Override
    public void close() throws SQLException {
        if (connection != null) {
            connection.close();
        }
    }
}
