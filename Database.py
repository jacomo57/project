import mysql.connector as mysql
from Block import Block
from User import User
import pickle


def main():
    db = Database()
    db.show_all_users()


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
            if pickle.loads(tup[2]).__eq__(block): return True
        return False

    def update_db_gen(self, block, username):
        sql_command = "UPDATE users SET block = %s WHERE name = %s"
        val = (pickle.dumps(block), username)
        self.cursor.execute(sql_command, val)
        self.db.commit()
        print(self.cursor.rowcount, "record(s) affected")

    def create_db(self, name):
        self.cursor.execute("CREATE DATABASE " + name)

    def delete_all_users(self):
        self.cursor.execute("TRUNCATE TABLE users")

    def create_users_table(self):
        self.cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY,"
                            " name VARCHAR(255),"
                            " block MEDIUMBLOB)")

    def insert_user_data(self, username, block):
        sql_command = "INSERT INTO users (name, block) VALUES (%s, %s)"
        val = (username, pickle.dumps(block))
        self.cursor.execute(sql_command, val)
        self.db.commit()  # Required to make the changes.
        print("1 record inserted, ID:", self.cursor.lastrowid)

    def show_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        users_tup = self.cursor.fetchall()
        for user in users_tup:
            block = pickle.loads(user[-1])  # I know block is last
            print("User ", user)
            print("Block ", block)

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
