package ru.marina.db.connection;

import java.sql.DriverManager;
import java.sql.SQLException;

public class PostgresConnection extends DBConnection {
    private static final String url = "jdbc:postgresql://localhost/treeDB";

    public PostgresConnection() throws SQLException {
        connect();
    }

    @Override
    public void connect() throws SQLException {
        connection = DriverManager.getConnection(url, userName, password);
    }
}
