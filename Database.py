import mysql.connector as mysql
from Block import Block
from User import User
import pickle


def main():
    db = Database()


class Database:
    def __init__(self):
        self.db = mysql.connect(host="localhost",
                                user="root",
                                passwd="root",
                                database="users_db")
        self.cursor = self.db.cursor()

    # If name exists return false else true.
    def verify_new_name(self, name):
        self.cursor.execute("Select * FROM users WHERE name ='" + name + "'")
        users = self.cursor.fetchall()
        if users:
            return False
        return True

    def verify_block(self, name, block):  # Needs to check if there is a user with both name and block, true if exists.
        self.cursor.execute("SELECT * FROM users WHERE name ='" + name + "'")
        user = self.cursor.fetchall()
        for tup in user:
            if pickle.loads(tup[3]).__eq__(block): return True
        return False

    def update_gen_block(self, block, username):
        self.cursor.execute("UPDATE users SET block ='" + block + "' WHERE name = '" + username + "'")

    def create_db(self, name):
        self.cursor.execute("CREATE DATABASE " + name)

    def delete_all_users(self):
        self.cursor.execute("TRUNCATE TABLE users")

    def create_users_table(self):
        self.cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY,"
                            " name VARCHAR(255),"
                            " password VARCHAR(255),"
                            " block MEDIUMBLOB)")

    def insert_user_data(self, username, password, block):
        sql_command = "INSERT INTO users (name, password, block) VALUES (%s, %s, %s)"
        val = (username, password, pickle.dumps(block))
        self.cursor.execute(sql_command, val)
        self.db.commit()  # Required to make the changes.
        print("1 record inserted, ID:", self.cursor.lastrowid)

    def show_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for user in users:
            block = pickle.loads(user.block)
            print("User Block: " + block)
            print("User " + user)

    def show_by_column(self, column):
        self.cursor.execute("SELECT " + column + " From users")
        results = self.cursor.fetchall()
        for result in results:
            if column == "block":
                block = pickle.loads(result)
                print(block)
            else:
                print(result)

    def show_by_value_from_column(self, column, value):
        self.cursor.execute("SELECT * FROM users WHERE " + column + " =" + value)
        results = self.cursor.fetchall()
        for result in results:
            if column == "block":
                block = pickle.loads(result)
                print(block)
            else:
                print(result)


if __name__ == '__main__':
    main()