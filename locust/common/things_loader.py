from typing import Dict, List
from locust.clients import HttpSession
from ksuid import Ksuid


def create_thing(session: HttpSession) -> Dict:

    thing_id: str = str(Ksuid())
    thing: dict = {"id": thing_id, "name": f"thing {thing_id}"}
    response = session.post("/things", json=thing)

    return response.json()


def delete_thing(session: HttpSession, id: str):
    response = session.delete(f"/things/{id}")
