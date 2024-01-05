module ru.marina.hw42 {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;
    requires com.dlsc.formsfx;
    requires net.synedra.validatorfx;
    requires org.kordamp.ikonli.javafx;
    requires com.google.gson;

    opens ru.marina.hw42 to javafx.fxml;
    exports ru.marina.hw42;
    exports ru.marina.hw42.tree;
    exports ru.marina.hw42.server;
}