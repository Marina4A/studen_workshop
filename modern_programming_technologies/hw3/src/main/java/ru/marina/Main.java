package ru.marina;

import ru.marina.db.entities.NodeEntity;
import ru.marina.db.repositories.NodeRepository;
import ru.marina.services.TreeService;
import ru.marina.tree.Tree;
import ru.marina.ui.Ui;

import java.util.List;

public class Main {
    private static final Tree tree = new Tree();

    public static void main(String[] args) {
        // comment line "<property name="hibernate.hbm2ddl.auto">create</property>" in hibernate.cfg.xml
        // and next line if you do not want database to be recreated and repopulated
        TreeService.recreateDB();

        Ui ui = new Ui(tree);
        ui.launch();
    }

    public static void test() {
        TreeService.recreateDB();
        NodeRepository nodeRepository = new NodeRepository();
        List<NodeEntity> ln = nodeRepository.findAll();
        for (NodeEntity n : ln) {
            System.out.printf("%d, %d\n", n.getId(), n.getParentId());
        }
        System.out.println("=========================");

        nodeRepository.delete(ln.get(ln.size() - 1).getId());
//        nodeRepository.insert(new NodeEntity(21,20));
        ln = nodeRepository.findAll();
        for (NodeEntity n : ln) {
            System.out.printf("%d, %d\n", n.getId(), n.getParentId());
        }
    }
}