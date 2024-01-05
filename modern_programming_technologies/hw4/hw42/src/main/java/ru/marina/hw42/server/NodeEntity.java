package ru.marina.hw42.server;

import ru.marina.hw42.tree.Node;

public class NodeEntity {
    public long id;
    public long parentId;

    public NodeEntity() {}

    public NodeEntity(Node n) {
        id = n.getId();
        Node parent = n.getParent();
        if (parent == null) {
            parentId = id;
        }
        else {
            parentId = parent.getId();
        }
    }

    public NodeEntity(long id, long parentId) {
        this.id = id;
        this.parentId = parentId;
    }

}
