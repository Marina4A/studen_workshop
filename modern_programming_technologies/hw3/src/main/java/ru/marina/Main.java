package ru.marina;

import ru.marina.services.TreeService;
import ru.marina.tree.Tree;
import ru.marina.ui.Ui;

public class Main {
    private static final Tree tree = new Tree();

    public static void main(String[] args) {
        TreeService.recreateDB();

        Ui ui = new Ui(tree);
        ui.launch();
    }
}