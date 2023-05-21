"""Напишите Python приложение с графическим интерфейсом (например, с помощью Tkinter или PyQt),
которое будет выполнять CRUD операции (create, read, update, delete) для таблицы в базе данных.
Приложение должно подключаться к серверной базе данных (например, MySQL) и предоставлять пользователю возможность
добавлять, просматривать, изменять и удалять данные в таблице для автосервиса."""

from tkinter import *
import mysql.connector


class RecordManager:
    def __init__(self, host, user, password, database):
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.mydb.cursor()

        # Create GUI elements
        self.root = Tk()
        self.root.title("Auto Service App")

        self.name_entry = Entry(self.root, width=30)
        self.name_entry.grid(row=0, column=1, padx=20)

        self.address_entry = Entry(self.root, width=30)
        self.address_entry.grid(row=1, column=1)

        self.phone_entry = Entry(self.root, width=30)
        self.phone_entry.grid(row=2, column=1)

        self.age_entry = Entry(self.root, width=30)
        self.age_entry.grid(row=3, column=1)

        self.name_label = Label(self.root, text="Name")
        self.name_label.grid(row=0, column=0)

        self.address_label = Label(self.root, text="Address")
        self.address_label.grid(row=1, column=0)

        self.phone_label = Label(self.root, text="Phone Number")
        self.phone_label.grid(row=2, column=0)

        self.age_label = Label(self.root, text="Age")
        self.age_label.grid(row=3, column=0)

        self.add_btn = Button(self.root, text="Add Record", command=self.add_record)
        self.add_btn.grid(row=4, column=0, pady=20)

        self.remove_btn = Button(self.root, text="Remove Record", command=self.remove_record)
        self.remove_btn.grid(row=4, column=1)

        self.update_btn = Button(self.root, text="Update Record", command=self.update_record)
        self.update_btn.grid(row=4, column=2)

        self.view_btn = Button(self.root, text="View Records", command=self.view_records)
        self.view_btn.grid(row=5, column=0, columnspan=3, pady=20)

    def add_record(self):
        sql = "INSERT INTO customers (name, address, phone, age) VALUES (%s, %s, %s, %s)"
        values = (self.name_entry.get(), self.address_entry.get(), self.age_entry.get(), self.phone_entry.get())
        self.cursor.execute(sql, values)
        self.mydb.commit()
        self.clear_fields()

    def remove_record(self):
        sql = "DELETE FROM customers WHERE name = %s"
        value = (self.name_entry.get(),)
        self.cursor.execute(sql, value)
        self.mydb.commit()
        self.clear_fields()

    def update_record(self):
        sql = "UPDATE customers SET address = %s, phone = %s, age = %s WHERE name = %s"
        values = (self.address_entry.get(), self.phone_entry.get(), self.age_entry.get(), self.name_entry.get())
        self.cursor.execute(sql, values)
        self.mydb.commit()
        self.clear_fields()

    def view_records(self):
        self.cursor.execute("SELECT * FROM customers")
        records = self.cursor.fetchall()
        self.display_records(records)

    def display_records(self, records):
        row_counter = 6
        for record in records:
            display = Label(self.root, text=record)
            display.grid(row=row_counter, column=0, padx=10, pady=5, columnspan=3)
            row_counter += 1

    def clear_fields(self):
        self.name_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.age_entry.delete(0, END)


    def start(self):
        self.cursor.execute("DROP DATABASE mydatabase;")

        # Создаем базу данных "mydatabase", если ее нет
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase;")

        # Переключаемся на базу данных "mydatabase"
        self.cursor.execute("USE mydatabase")

        # Здесь создаем таблицу "customers" со столбцами "name", "address", "age", "phone"
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), "
            "address VARCHAR(255), age INT, phone VARCHAR(20));")
        self.mydb.commit()

        self.root.mainloop()


if __name__ == '__main__':
    config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "Andreevna1501",
        "database": None
    }

    manager = RecordManager(**config)
    manager.start()
