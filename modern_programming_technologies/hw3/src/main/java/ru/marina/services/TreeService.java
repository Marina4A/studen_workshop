package ru.marina.services;

import ru.marina.db.entities.NodeEntity;
import ru.marina.db.repositories.NodeRepository;
import ru.marina.tree.Node;
import ru.marina.tree.Tree;

import java.util.List;

public class TreeService {

    public static Tree readFromDB() {
        Tree tree = new Tree();
        try {
            NodeRepository nodeRepository = new NodeRepository();
            List<NodeEntity> nodesList = nodeRepository.findAll();
            for (NodeEntity n : nodesList) {
                tree.addNode(n.getId(), n.getParentId());
            }
        } catch (Exception e) {
            String errMsg = String.format("Ошибка чтения таблицы: " + e.getMessage());
            throw new RuntimeException(errMsg);
        }
        return tree;
    }

    public static void deleteFromDBRecursive(NodeRepository nodeRepository, Node node) {
        for (Node n: node.getChildren()) {
            deleteFromDBRecursive(nodeRepository, n);
        }
        nodeRepository.delete(node.getId());
    }

    public static void deleteFromDB(Node n) {
        if (n == null) {
            return;
        }
        try {
            NodeRepository nodeRepository = new NodeRepository();
            deleteFromDBRecursive(nodeRepository, n);
        } catch (Exception e) {
            String errMsg = String.format("Ошибка удаления узла " + n.getId() + " из таблицы: " + e.getMessage());
            throw new RuntimeException(errMsg);
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
        try {
            NodeRepository nodeRepository = new NodeRepository();

            nodeRepository.insert(new NodeEntity(id, parent));
        } catch (Exception e) {
            String errMsg = String.format("Ошибка добавления узла " + id + " в таблицу: " + e.getMessage());
            throw new RuntimeException(errMsg);
        }
    }

    public static void addToDB(int id, int parentId) {
        try {
            new NodeRepository().insert(new NodeEntity(id, parentId));
        } catch (Exception e) {
            String errMsg = String.format("Ошибка добавления узла " + id + " в таблицу: " + e.getMessage());
            throw new RuntimeException(errMsg);
        }
    }

    public static final NodeEntity[] initialNodes = {
            new NodeEntity(1, 1),
            new NodeEntity(3, 1),
            new NodeEntity(2, 1),
            new NodeEntity(4, 2),
            new NodeEntity(6, 3),
            new NodeEntity(5, 2),
            new NodeEntity(7, 3),
            new NodeEntity(9, 3),
            new NodeEntity(8, 3),
            new NodeEntity(10, 10),
            new NodeEntity(12, 10),
            new NodeEntity(11, 10),
            new NodeEntity(13, 10),
            new NodeEntity(15, 11),
            new NodeEntity(14, 11),
            new NodeEntity(16, 12),
            new NodeEntity(18, 12),
            new NodeEntity(17, 12),
            new NodeEntity(19, 12),
            new NodeEntity(21, 13),
            new NodeEntity(20, 13),
            new NodeEntity(22, 13),
            new NodeEntity(30, 30),
            new NodeEntity(23, 13),
            new NodeEntity(31, 30),
            new NodeEntity(33, 32),
            new NodeEntity(32, 31),
            new NodeEntity(34, 33),
            new NodeEntity(36, 35),
            new NodeEntity(35, 34),
            new NodeEntity(37, 36),
            new NodeEntity(38, 37),
            new NodeEntity(39, 38),
    };

    public static void recreateDB() {
        try {
            NodeRepository nodeRepository = new NodeRepository();
            for (NodeEntity n : initialNodes) {
                nodeRepository.insert(n);
            }
        } catch (Exception e) {
            System.out.println("Ошибка создания или наполнения БД: " + e.getMessage());
        }
    }

}
