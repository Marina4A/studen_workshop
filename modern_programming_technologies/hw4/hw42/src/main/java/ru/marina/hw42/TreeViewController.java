package ru.marina.hw42;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import ru.marina.hw42.tree.Node;
import ru.marina.hw42.tree.Tree;
import ru.marina.hw42.tree.TreeUtils;

import java.util.List;

public class TreeViewController {
    public TreeView<Node> treeView;

    private final Tree tree = new Tree();
    private final TreeItem<Node> rootTreeItem = new TreeItem<Node>(tree.getRoot());
    public Label messageLine;
    public Button addButton;
    public TextField nodeIdToInsertTextField;
    public Button deleteButton;

    @FXML
    protected void onLoadTreesClick() {
        try {
            TreeUtils.readDB(tree);
        }
        catch (Exception e) {
            Throwable cause = e.getCause();
            String msg = "Ошибка " + e.getMessage();
            if (cause != null) {
                msg = msg + " " + cause.getMessage();
            }
            messageLine.setText(msg);
//System.out.println(msg); //ttodo remove me
        }
        updateView();
    }

    private void updateViewRecursive(TreeItem<Node> parent, List<Node> children) {
        for (Node n : children) {
            TreeItem<Node> ti = new TreeItem<>(n);
            updateViewRecursive(ti, n.getChildren());
            parent.getChildren().add(ti);
        }
    }

    public void updateView() {
        rootTreeItem.getChildren().clear();
        updateViewRecursive(rootTreeItem, tree.getSubTrees());
        treeView.setRoot(rootTreeItem);
    }

    public void onDeleteButtonAction(ActionEvent actionEvent) {
        tree.delete(
                treeView.getSelectionModel().getSelectedItem().getValue());
        updateView();
    }

    public void onAddButtonAction(ActionEvent actionEvent) {
        long id = 0;
        long parent = 0;
        try {
            id = Long.parseLong(nodeIdToInsertTextField.getText());
        }
        catch (NumberFormatException e) {
            messageLine.setText("Invalid value of new node id: " + e.getMessage());
            return;
        }

        try {
            parent = treeView.getSelectionModel().getSelectedItem().getValue().getId();
            TreeUtils.addToDB(id, parent);
            tree.addNode(id, parent);
        }
        catch (Exception e) {
            messageLine.setText("Error adding new node " + id + " to parent " + parent + ": " + e.getMessage());
            return;
        }
        updateView();
    }
}