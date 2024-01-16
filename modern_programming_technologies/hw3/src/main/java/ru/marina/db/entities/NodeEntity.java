package ru.marina.db.entities;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import ru.marina.tree.Node;

@Entity
@Table(name = "trees")
public class NodeEntity {
    @Id
    private int id;

    @Column
    private int parentId;

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

    public NodeEntity(int id, int parentId) {
        this.id = id;
        this.parentId = parentId;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getParentId() {
        return parentId;
    }

    public void setParentId(int parentId) {
        this.parentId = parentId;
    }
}
