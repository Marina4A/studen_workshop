package ru.marina.hw41;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import ru.marina.hw41.tree.Forest;

import java.io.File;

@SpringBootApplication
public class TreeServerApp {
	public static final Forest forest = new Forest();

	public static void main(String[] args) {
		readCsv(new File("input.scv"));
		SpringApplication.run(TreeServerApp.class, args);
	}

	public static void readCsv(File file) {
		try {
			forest.readCsv(file);
			System.out.println(forest);
		} catch (RuntimeException e) {
			System.out.println("Ошибка чтения леса: " + e.getMessage());
		}
//		System.exit(0);
	}

}
