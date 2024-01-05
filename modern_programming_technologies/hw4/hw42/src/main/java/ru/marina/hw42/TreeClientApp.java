package ru.marina.hw42;

import javafx.application.Application;
import javafx.beans.binding.Bindings;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

public class TreeClientApp extends Application {
    private TreeViewController tvController;

    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(TreeClientApp.class.getResource("main-view.fxml"));
        Scene scene = new Scene(fxmlLoader.load(), 320, 640);
        tvController = fxmlLoader.getController();
        tvController.updateView();

        tvController.deleteButton.disableProperty().
                bind(Bindings.isEmpty(tvController.treeView.getSelectionModel().getSelectedIndices()));

        tvController.addButton.disableProperty().
                bind(Bindings.or(
                        Bindings.isEmpty(tvController.treeView.getSelectionModel().getSelectedIndices()),
                        tvController.nodeIdToInsertTextField.textProperty().isEmpty()
                        ));

        stage.setTitle("Tree view");
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}