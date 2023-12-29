package com.company;

import java.util.ArrayList;
import java.util.List;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Transient;

@Entity
public class Node {
    @Id
    private int id;
    private int parent_id;

    @Transient
    Node parent;

    @Transient
    List<Node> child = new ArrayList<>();

    public Node()
    {
        id = 0;
        parent_id = 0;
    }

    public Node( int _id, int _parent )
    {
        id = _id;
        parent_id = _parent;
    }
    public boolean isLeaf()
    {
        return child.size() == 0;
    }

    public boolean isRoot()
    {
        return parent == null;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getParent_id() {
        return parent_id;
    }

    public void setParent_id(int parent_id) {
        this.parent_id = parent_id;
    }

    public Node getParent() {
        return parent;
    }

    public void setParent(Node parent) {
        this.parent = parent;
    }

    @Transient
    public List<Node> getChild() {
        return child;
    }

    public int leafCount()
    {
        if (isLeaf())
            return 1;

        int s = 0;

        for( int i = 0; i < child.size(); i++ )
            s += child.get(i).leafCount();

        return s;
    }
}
