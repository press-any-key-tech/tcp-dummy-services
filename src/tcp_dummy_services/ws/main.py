import asyncio
import argparse

from tcp_dummy_services.core import logger
from tcp_dummy_services.core import settings

import sys


from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from typing import Dict
import json

app: FastAPI = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


class MyTest(BaseModel):
    id: str
    name: str


tests: Dict[str, MyTest] = {}


# TODO: reduce congnitive complexity
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        command = json.loads(data)

        if command["action"] == "create":
            test = MyTest(**command["data"])
            if test.id in tests:
                await websocket.send_text("MyTest already exists")
            else:
                tests[test.id] = test
                logger.info(f"MyTest created: {test.model_dump_json()}")
                await websocket.send_text("MyTest created")

        elif command["action"] == "read":
            if command["id"] in tests:
                logger.info(f"MyTest read: {tests[command["id"]].model_dump_json()}")
                await websocket.send_text(tests[command["id"]].model_dump_json())
            else:
                await websocket.send_text("MyTest not found")

        elif command["action"] == "update":
            test = MyTest(**command["data"])
            if test.id in tests:
                tests[test.id] = test
                logger.info(f"MyTest updated: {test.model_dump_json()}")                
                await websocket.send_text("MyTest updated")
            else:
                await websocket.send_text("MyTest not found")

        elif command["action"] == "delete":
            if command["id"] in tests:
                del tests[command["id"]]
                logger.info(f"MyTest deleted: {command["id"]}")
                await websocket.send_text("MyTest deleted")
            else:
                await websocket.send_text("MyTest not found")
