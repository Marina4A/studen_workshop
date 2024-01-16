package ru.marina.tree;

import ru.marina.db.connection.DBConnection;
import ru.marina.db.connection.H2Connection;
import ru.marina.db.entities.NodeEntity;

import java.sql.SQLException;
import java.util.List;

public class TreeDbHelper {

    public static Tree readDB() {
        Tree tree = new Tree();
        try (DBConnection connection = new H2Connection()) {
            List<NodeEntity> nodesList = connection.readTree();
            for (NodeEntity n : nodesList) {
                tree.addNode(n.getId(), n.getParentId());
            }
        } catch (SQLException e) {
            System.out.println("Ошибка чтения таблицы: " + e.getMessage());
        }
        return tree;
    }

    public static void deleteFromDB(int id) {
        try (DBConnection connection = new H2Connection()) {
            connection.deleteNode(id);
        } catch (SQLException e) {
            System.out.println("Ошибка удаления узла " + id + " из таблицы: " + e.getMessage());
        }
    }

    public static void addToDB(Node n) {
        int id = n.getId();
        int parent;

        if (n.isRoot()) {
            parent = id;
        } else {
            parent = n.getParent().getId();
        }
        try (DBConnection connection = new H2Connection()) {
            connection.insertNode(id, parent);
        } catch (SQLException e) {
            System.out.println("Ошибка добавления узла " + id + " в таблицу: " + e.getMessage());
        }
    }

    public static void recreateDB() {
        try (DBConnection connection = new H2Connection()) {
            connection.dropSchema();
            connection.createSchema();
            connection.populateSchema();
        } catch (SQLException e) {
            System.out.println("Ошибка создания или наполнения БД: " + e.getMessage());
        }
    }

}
