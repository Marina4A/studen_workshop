package ru.marina.hw41.db.entities;

import jakarta.persistence.*;

import lombok.Data;
import ru.marina.hw41.tree.Node;

@Data
@Entity
@Table(name = "trees")
public class NodeEntity {
    @Id
    private long id;

    @Column
    private long parentId;

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
