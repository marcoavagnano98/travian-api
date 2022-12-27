import requests
import json
from custom_session import CustomSession as Cs


class Login:
    def __init__(self, url, credentials, session):
        self.session = session
        self.base_url = url
        self.header = {"Content-Type": "application/json", "Content-Length": ""}
        self.body = {**credentials, "w": "1536:864",
                     "mobileOptimizations": False}
        self.header["Content-Length"] = str(len(str(self.body).replace(" ", "")))
        self.logged_in = False


    def login(self):
        token_response = self.session.json_post_request(url=self.base_url + f'api/v1/auth/{self.get_nonce()}', headers=self.header)
        if token_response.status_code != 200:
            raise requests.exceptions.RequestException
        self.logged_in = True
        token = json.loads(token_response.text)['token']
        self.session.set_auth_bearer(token)


    def get_nonce(self):
        nonce_response = self.session.json_post_request(url=self.base_url + "api/v1/auth/login", headers=self.header,
                                                        body=self.body)
        if nonce_response.status_code != 200:
            raise requests.exceptions.RequestException
        return json.loads(nonce_response.text)['nonce']
