package ru.marina.db.entities;

public class NodeEntity {
    private int id;

    private int parentId;

    public NodeEntity(int id, int parentId) {
        this.id = id;
        this.parentId = parentId;
    }

    public int getId() {
        return id;
    }

    public int getParentId() {
        return parentId;
    }

}
