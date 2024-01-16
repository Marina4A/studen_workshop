package ru.marina.db.connection;

import ru.marina.db.entities.NodeEntity;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public abstract class DBConnection implements AutoCloseable {
    protected static final NodeEntity[] initialNodes = {
            new NodeEntity(1, 1),
            new NodeEntity(2, 2),
            new NodeEntity(3, 3),
            new NodeEntity(4, 1),
            new NodeEntity(5, 1),
            new NodeEntity(6, 1),
            new NodeEntity(7, 5),
            new NodeEntity(8, 5),
            new NodeEntity(9, 5),
            new NodeEntity(10, 2),
            new NodeEntity(11, 2),
            new NodeEntity(12, 2),
            new NodeEntity(13, 10),
            new NodeEntity(14, 10),
            new NodeEntity(15, 11),
            new NodeEntity(16, 11),
            new NodeEntity(17, 12),
            new NodeEntity(18, 12),
            new NodeEntity(19, 3),
            new NodeEntity(20, 19),
            new NodeEntity(21, 20),
            new NodeEntity(22, 21),
            new NodeEntity(23, 22),
            new NodeEntity(24, 23),
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
        String sql =
                "INSERT INTO TREES(id, parentId) " +
                "VALUES " +
                "   (?, ?)";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            for (NodeEntity n : initialNodes) {
                statement.setInt(1, n.getId());
                statement.setInt(2, n.getParentId());
                statement.executeUpdate();
            }
        }
    }

    public void insertNode(int id, int parentId) throws SQLException {
        String sql =
                "INSERT INTO TREES(id, parentId) " +
                "VALUES " +
                 "   (?, ?)";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            statement.setInt(2, parentId);
            statement.executeUpdate();
        }
    }

    public void deleteNode(int id) throws SQLException {
        String sql =
                "DELETE FROM TREES " +
                "WHERE id = ? ";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            statement.executeUpdate();

        }
    }

    public List<NodeEntity> readTree() throws SQLException {
        String sql =
                "SELECT id, parentId " +
                "FROM TREES";
        try (Statement statement = connection.createStatement()) {
            ResultSet rs = statement.executeQuery(sql);
            List<NodeEntity> list = new ArrayList<>();
            while (rs.next()) {
                NodeEntity n = new NodeEntity(rs.getInt("id"), rs.getInt("parentId"));
                list.add(n);
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
