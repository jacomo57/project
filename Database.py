import mysql.connector as mysql


def main():
    db = Database()
    print(db)


class Database:
    def __init__(self):
        self.db = mysql.connect(host="10.51.101.87", user="root", passwd="root")
        self.cursor = self.db.cursor()


if __name__ == '__main__':
    main()
