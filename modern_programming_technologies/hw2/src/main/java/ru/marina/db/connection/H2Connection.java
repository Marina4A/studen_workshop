package ru.marina.db.connection;

import java.sql.DriverManager;
import java.sql.SQLException;


public class H2Connection extends DBConnection {
    private static final String url = "jdbc:h2:~/treeDB";

    public H2Connection() throws SQLException {
        connect();
    }

    @Override
    public void connect() throws SQLException {
        DriverManager.registerDriver(new org.h2.Driver());
        connection = DriverManager.getConnection(url, userName, password);
    }
}

