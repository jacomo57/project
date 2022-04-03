import mysql.connector as mysql
from Block import Block
from User import User


def main():
    db = Database()
    db.show_all_users()
    print()
    db.show_by_column("name")
    print()
    db.show_by_value_from_column("name", "'name1'")


class Database:
    def __init__(self):
        self.db = mysql.connect(host="localhost",
                                user="root",
                                passwd="root",
                                database="users_db")
        self.cursor = self.db.cursor()

    def create_db(self, name):
        self.cursor.execute("CREATE DATABASE " + name)

    def create_users_table(self, name):
        self.cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY,"
                            " name VARCHAR(255),"
                            " password VARCHAR(255),"
                            " block VARCHAR(255))")

    def insert_users_data(self, user):
        sql_command = "INSERT INTO users (name, password, block_id) VALUES (%s, %s, %s)"
        val = (user.user_name, user.password, user.block.hash)
        self.cursor.execute(sql_command, val)
        self.db.commit()  # Required to make the changes.
        print("1 record inserted, ID:", self.cursor.lastrowid)

    def show_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for user in users:
            print(user)

    def show_by_column(self, column_name):
        self.cursor.execute("SELECT " + column_name + " From users")
        results = self.cursor.fetchall()
        for result in results:
            print(result)

    def show_by_value_from_column(self, column, value):
        self.cursor.execute("SELECT * FROM users WHERE " + column + " =" + value)
        results = self.cursor.fetchall()
        for result in results:
            print(result)


if __name__ == '__main__':
    main()
