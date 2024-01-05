package ru.marina.hw41.db.repositories;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import ru.marina.hw41.db.entities.NodeEntity;

@Repository
public interface NodeRepository extends CrudRepository<NodeEntity, Long> {
}
