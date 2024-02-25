from typing import Dict
from locust import HttpUser, task
from common import create_thing, delete_thing
import random


class ThingUser(HttpUser):

    base_path: str = "/things"
    things: Dict = {}
    things_keys: list = []

    def on_start(self):
        """Initialize the user session with several well known Things to test" """
        thing: Dict = create_thing(self.client)
        self.things[thing["id"]] = thing
        self.things_keys = list(self.things.keys())

    def on_stop(self):
        """Delete all the things created during the test"""
        for key, value in self.things.items():
            delete_thing(self.client, id=key)

        self.things = {}
        self.things_keys = []

    @task
    def get_things(self):
        """Get a whole list of things from the service"""
        self.client.get("/things")

    @task
    def get_thing(self):
        """Get just one thing from the service"""
        random_key = random.choice(self.things_keys)
        self.client.get(f"/things/{random_key}")
