package ru.marina.db.repositories;

import ru.marina.db.entities.NodeEntity;

import java.util.List;

public interface NodeRepositoryIf {
    List<NodeEntity> findAll();
    NodeEntity findById(int id);
    void insert(NodeEntity n);
    void update(NodeEntity n);
    void delete(int id);
}
