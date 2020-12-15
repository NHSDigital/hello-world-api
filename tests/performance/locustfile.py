import os
from common.auth import Auth
from locust import HttpUser, task, between
from uuid import uuid4


class HelloWorldsUser(HttpUser):
    wait_time = between(5, 9)

    def auth(self):
        return Auth(
            os.environ["LOCUST_HOST"],
            os.environ["CALLBACK_URL"],
            os.environ["CLIENT_ID"],
            os.environ["CLIENT_SECRET"]
        )

    def on_start(self):
        self.base_path = os.environ["BASE_PATH"]
        self.endpoint = os.environ["ENDPOINT"]
        authenticator = self.auth()
        self.credentials = authenticator.login()
        self.headers = {
            "Authorization": self.credentials["token_type"] + " " + self.credentials["access_token"],
            "apikey": os.environ["CLIENT_ID"],
        }

    @task(1)
    def helloWorld_api(self):
        self.client.get(f"{self.base_path}/{self.endpoint}", headers=self.headers)

        
