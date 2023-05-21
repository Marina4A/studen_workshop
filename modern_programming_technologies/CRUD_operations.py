"""Напишите Python приложение с графическим интерфейсом (например, с помощью Tkinter или PyQt),
которое будет выполнять CRUD операции (create, read, update, delete) для таблицы в базе данных.
Приложение должно подключаться к серверной базе данных (например, MySQL) и предоставлять пользователю возможность
добавлять, просматривать, изменять и удалять данные в таблице для автосервиса."""

from tkinter import *
import mysql.connector

# root = Tk()
# root.mainloop()
#
#
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="username",
#   password="password",
#   database="database_name"
# )
#
# mycursor = mydb.cursor()
#
# mycursor.execute("SELECT * FROM table_name")
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#   print(x)
#
#
# sql = "INSERT INTO table_name (column1, column2, column3) VALUES (%s, %s, %s)"
# val = ("value1", "value2", "value3")
# mycursor.execute(sql, val)
#
# mydb.commit()
#
# print(mycursor.rowcount, "record inserted.")
#
# mycursor.execute("UPDATE table_name SET column1 = 'new_value' WHERE id = '1'")
#
# mydb.commit()
#
# print(mycursor.rowcount, "record(s) affected")
#
# mycursor.execute("DELETE FROM table_name WHERE id = '1'")
#
# mydb.commit()
#
# print(mycursor.rowcount, "record(s) deleted")
#
#
# def add_record():
#   sql = "INSERT INTO table_name (column1, column2, column3) VALUES (%s, %s, %s)"
#   val = (entry1.get(), entry2.get(), entry3.get())
#   mycursor.execute(sql, val)
#   mydb.commit()
#   print(mycursor.rowcount, "record inserted.")
#
#
# Button(root, text="Add Record", command=add_record).pack()
#
# entry1 = Entry(root)
# entry1.pack()
#
# entry2 = Entry(root)
# entry2.pack()
#
# entry3 = Entry(root)
# entry3.pack()

def add_record():
  sql = "INSERT INTO customers (name, address, phone) VALUES (%s, %s, %s)"
  values = (name_entry.get(), address_entry.get(), phone_entry.get())
  mycursor.execute(sql, values)
  mydb.commit()
  clear_fields()


def remove_record():
  sql = "DELETE FROM customers WHERE name = %s"
  value = (name_entry.get(),)
  mycursor.execute(sql, value)
  mydb.commit()
  clear_fields()


def update_record():
  sql = "UPDATE customers SET address = %s, phone = %s WHERE name = %s"
  values = (address_entry.get(), phone_entry.get(), name_entry.get())
  mycursor.execute(sql, values)
  mydb.commit()
  clear_fields()


def view_records():
  mycursor.execute("SELECT * FROM customers")
  records = mycursor.fetchall()
  display_records(records)


def display_records(records):
  for index, record in enumerate(records):
    display = Label(root, text=record)
    display.grid(row=index + 5, column=0, padx=10, pady=5, columnspan=3)


def clear_fields():
  name_entry.delete(0, END)
  address_entry.delete(0, END)
  phone_entry.delete(0, END)



mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="database_name"
)

mycursor = mydb.cursor()


root = Tk()
root.title("Auto Service App") # Заголовок окна

# Добавление элементов интерфейса
root.mainloop()


# Создание полей ввода
name_entry = Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=20)

address_entry = Entry(root, width=30)
address_entry.grid(row=1, column=1)

phone_entry = Entry(root, width=30)
phone_entry.grid(row=2, column=1)

# Создание меток
name_label = Label(root, text="Name")
name_label.grid(row=0, column=0)

address_label = Label(root, text="Address")
address_label.grid(row=1, column=0)

phone_label = Label(root, text="Phone Number")
phone_label.grid(row=2, column=0)

# Создание кнопок
add_btn = Button(root, text="Add Record", command=add_record)
add_btn.grid(row=3, column=0, pady=20)

remove_btn = Button(root, text="Remove Record", command=remove_record)
remove_btn.grid(row=3, column=1)

update_btn = Button(root, text="Update Record", command=update_record)
update_btn.grid(row=3, column=2)

view_btn = Button(root, text="View Records", command=view_records)
view_btn.grid(row=4, column=0, columnspan=3, pady=20)
