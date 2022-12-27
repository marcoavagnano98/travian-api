if __name__ == '__main__':
    from account import Account

    account = Account("https://ts4.x1.europe.travian.com/", {"name": "pippo", "password": "pluto"})
    account_info = account.get_villages_info()


