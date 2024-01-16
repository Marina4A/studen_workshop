package ru.marina.db.repositories;

import jakarta.persistence.criteria.*;
import org.hibernate.query.Query;
import org.hibernate.Session;
import org.hibernate.Transaction;
import ru.marina.db.MySessionFactory;
import ru.marina.db.entities.NodeEntity;

import java.util.List;

public class NodeRepository implements NodeRepositoryIf {

    @Override
    public List<NodeEntity> findAll() {
        try (Session session = MySessionFactory.getSessionFactory().openSession()) {
            CriteriaBuilder criteriaBuilder = session.getCriteriaBuilder();
            CriteriaQuery<NodeEntity> criteriaQuery = criteriaBuilder.createQuery(NodeEntity.class);
            Root<NodeEntity> root = criteriaQuery.from(NodeEntity.class);
            criteriaQuery.select(root);

            Query<NodeEntity> query = session.createQuery(criteriaQuery);
            return query.getResultList();
        }
    }

    @Override
    public NodeEntity findById(int id) {
        try (Session session = MySessionFactory.getSessionFactory().openSession()) {
            return session.get(NodeEntity.class, id);
        }
    }

    @Override
    public void insert(NodeEntity n) {
        try (Session session = MySessionFactory.getSessionFactory().openSession()) {
            Transaction transaction = session.beginTransaction();
            session.persist(n);
            transaction.commit();
        }
    }

    @Override
    public void update(NodeEntity n) {
        try (Session session = MySessionFactory.getSessionFactory().openSession()) {
            CriteriaBuilder criteriaBuilder = session.getCriteriaBuilder();
            CriteriaUpdate<NodeEntity> criteriaUpdate = criteriaBuilder.createCriteriaUpdate(NodeEntity.class);
            Root<NodeEntity> root = criteriaUpdate.from(NodeEntity.class);
            criteriaUpdate.set("parentId", n.getParentId());
            criteriaUpdate.where(criteriaBuilder.equal(root.get("id"), n.getId()));

            Transaction transaction = session.beginTransaction();
            session.createMutationQuery(criteriaUpdate).executeUpdate();
            transaction.commit();
        }
    }

    @Override
    public void delete(int id) {
        try (Session session = MySessionFactory.getSessionFactory().openSession()) {
            CriteriaBuilder criteriaBuilder = session.getCriteriaBuilder();

            CriteriaDelete<NodeEntity> criteriaDelete = criteriaBuilder.createCriteriaDelete(NodeEntity.class);
            Root<NodeEntity> root = criteriaDelete.from(NodeEntity.class);
            criteriaDelete.where(criteriaBuilder.equal(root.get("id"), id));
            Transaction transaction = session.beginTransaction();
            session.createMutationQuery(criteriaDelete).executeUpdate();
            transaction.commit();
        }
    }
}
