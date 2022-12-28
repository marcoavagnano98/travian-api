if __name__ == '__main__':
    from account import Account

    #account = Account("https://ts3.x1.america.travian.com/", {"name": "pomiy11146", "password": "americanpie"})

    account = Account("https://ts4.x1.europe.travian.com/", {"name": "mark98", "password": "tirana"})
    account_info = account.get_all_buildings()
    a = 0


