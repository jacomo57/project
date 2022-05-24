import mysql.connector as mysql
from Block import Block
from User import User
import pickle


def main():
    db = Database()
    user = User("Jacomo", "root")
    db.insert_users_data(user)
    db.show_by_column("block")


class Database:
    def __init__(self):
        self.db = mysql.connect(host="localhost",
                                user="root",
                                passwd="root",
                                database="users_db")
        self.cursor = self.db.cursor()

    # If name exists return false else true.
    def verify_new_name(self, name, password):
        return True #Just for testing until I do with db
        self.cursor.execute("Select * FROM users WHERE name =" + name)
        names = self.cursor.fetchall()
        if names:
            return False
        return True

    def create_db(self, name):
        self.cursor.execute("CREATE DATABASE " + name)

    def create_users_table(self):
        self.cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY,"
                            " name VARCHAR(255),"
                            " password VARCHAR(255),"
                            " block MEDIUMBLOB)")

    def insert_users_data(self, username, password, block):
        pass
        sql_command = "INSERT INTO users (name, password, block) VALUES (%s, %s, %s)"
        val = (username, password, pickle.dumps(block))
        self.cursor.execute(sql_command, val)
        self.db.commit()  # Required to make the changes.
        print("1 record inserted, ID:", self.cursor.lastrowid)

    def show_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for user in users:
            for thing in user.block:
                pickle.loads(thing)
                print(thing)
            print(user)

    def show_by_column(self, column):
        self.cursor.execute("SELECT " + column + " From users")
        results = self.cursor.fetchall()
        for result in results:
            if column == "block":
                for thing in result:
                    pickle.loads(thing)
                    print(result)
            else:
                print(result)

    def show_by_value_from_column(self, column, value):
        self.cursor.execute("SELECT * FROM users WHERE " + column + " =" + value)
        results = self.cursor.fetchall()
        for result in results:
            if column == "block":
                pickle.loads(result)
                print(result)
            else:
                print(result)

    def change_user_data(self, column, old, new, id):
        self.cursor.execute("SELECT * FROM users WHERE id =" + str(id))
        user = self.cursor.fetchall()
        # NEED TO DO CHECK THAT OLD FITS THE ONE FROM DB AND IF SO CHANGES IT.

    def create_db(self, name):
        self.cursor.execute("CREATE DATABASE " + name)

    def create_users_table(self, name):
        self.cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY,"
                            " name VARCHAR(255),"
                            " password VARCHAR(255),"
                            " block VARCHAR(255))")

    # If name exists return false else true.
    def verify_new_name(self, name, password): #DB
        self.cursor.execute("Select * FROM users WHERE name =" + name)
        names = self.cursor.fetchall()
        if names:
            return False
        return True

    def insert_user_data(self, user):
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