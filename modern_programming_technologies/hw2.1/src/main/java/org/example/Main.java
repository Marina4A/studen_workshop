package org.example;


import org.example.connection.DBConnection;
import org.example.connection.H2Connection;

import java.io.FileWriter;
import java.io.IOException;
import java.sql.SQLException;
import java.util.List;
public class Main {
    public static void main(String[] args) {
        try (DBConnection connection = new H2Connection()) {
            // Создание, заполнение и чтение базы данных
            connection.dropSchema();
            connection.createSchema();
            connection.populateSchema();

            // Построение графа на основе данных из базы данных
            Graph graph = buildGraph(connection.readTree());

            // Проверка на возможность пройти по всем узлам
            boolean canTraverse = graph.canTraverse();

            // Запись результата в файл output.csv
            writeOutput(canTraverse);

        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    private static Graph buildGraph(List<int[]> nodes) {
        Graph graph = new Graph();
        for (int[] node : nodes) {
            graph.addEdge(node[1], node[0]);
        }
        return graph;
    }

    private static void writeOutput(boolean canTraverse) {
        try (FileWriter writer = new FileWriter("output.csv")) {
            writer.write(String.valueOf(canTraverse));
        } catch (IOException e) {
            System.out.println("Ошибка при записи в файл output.csv: " + e.getMessage());
        }
    }
}