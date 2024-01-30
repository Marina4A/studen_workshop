package ru.marina;

import ru.marina.tree.Tree;
import ru.marina.tree.TreeDbHelper;

import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;


public class Main {
    private static final String scvFileName = "output.csv";

    public static void main(String[] args) {
        // закоментировать, иначе БД будет удалена, воссоздана, и наполнена тестовыми данными
        TreeDbHelper.recreateDB();

        Tree tree = TreeDbHelper.readDB();
        try (FileWriter fw = new FileWriter(scvFileName)) {
            int leavesCounter = tree.getAllLeaves().size();
            fw.write(Integer.toString(leavesCounter));
//            System.out.println("Всего листьев = " + leavesCounter);
            fw.flush();
        } catch (FileNotFoundException e) {
            System.out.println("Ошибка создания файла \"" + scvFileName + "\": " + e.getMessage());
        } catch (IOException e) {
            System.out.println("Ошибка записи в файл \"" + scvFileName + "\": " + e.getMessage());
        }
    }
}