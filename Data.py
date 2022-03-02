def main():
    dict = {"IP1": 1292}
    data = Data(dict)
    print(data.addresses)


class Data:
    def __init__(self, addresses={}):  # dictionary for addresses ip goes to port
        self.addresses = addresses

    def __str__(self):
        print()


if __name__ == '__main__':
    main()
