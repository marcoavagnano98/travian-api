if __name__ == '__main__':
    from account import Account
    server_url = "https://ts3.x1.america.travian.com/"
    account = Account(server_url, {"name": "your_username", "password": "your_password"})
    account_info = account.get_all_buildings()
