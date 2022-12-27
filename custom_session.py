import requests


class CustomSession:
    def __init__(self):
        self.session = requests.Session()

    def close_session(self):
        if self.session:
            self.session.close()

    def get_request(self, url, headers=None):
        return self.session.get(url=url, headers=headers)

    def json_post_request(self, url, headers, body=None):
        if body is None:
            body = {}
        if type(body) != dict:
            raise TypeError
        return self.session.post(url=url, headers=headers,
                                 json=body)

    def set_auth_bearer(self, token):
        self.session.auth = ("Authorization", f'Bearer {token}')
