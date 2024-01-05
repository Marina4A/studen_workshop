package ru.marina.hw42.tree;

import ru.marina.hw42.server.BackendRequest;
import ru.marina.hw42.server.NodeEntity;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.Scanner;

public class TreeUtils {
    public static void readCsv(Tree destination, File file) {
        try (InputStream is = new FileInputStream(file);
             Scanner sc = new Scanner(is)) {
            int line = 1;
            while (sc.hasNextLine()) {
                String s = sc.nextLine();
                String[] pair = s.split(",");
                if (pair.length != 2) {
                    throw new RuntimeException("csv file \"" + file.getName() + "\"" +
                            " line #" + line +
                            ": number of elements equals to " + pair.length + " , but should be 2 (\"" + s + "\")");
                }
                int id = Integer.parseInt(pair[0].trim());
                int parent = Integer.parseInt(pair[1].trim());
                destination.addNode(id, parent);
                line++;
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (NumberFormatException e) {
            throw new RuntimeException("invalid number " + e.getMessage(), e);
        }
    }

    public static void readDB(Tree destination) {
        BackendRequest rn = new BackendRequest();
        List<NodeEntity> nl = rn.getNodes();
        for (NodeEntity n : nl) {
            destination.addNode(n.id, n.parentId);
        }
    }

    public static void deletFromDB(long id) {
        BackendRequest rn = new BackendRequest();
        rn.deleteNode(id);
    }

    public static void addToDB(long id, long parent) {
        BackendRequest rn = new BackendRequest();
        rn.addNode(new NodeEntity(id, parent));
    }

}
