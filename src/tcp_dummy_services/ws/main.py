
from tcp_dummy_services.core import logger
from tcp_dummy_services.core import settings

from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
from typing import Dict
import json

from tcp_dummy_services.domain.entities import Thing, Response


app: FastAPI = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


things: Dict[str, Thing] = {}


# TODO: Refactor to reduce congnitive complexity
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        try:
            command = json.loads(data)
        except json.JSONDecodeError:
            response = Response(status=400, message="Invalid JSON")
            await websocket.send_text(response.model_dump_json())
            continue
        except Exception as e:
            response = Response(status=500, message="Internal server error")
            await websocket.send_text(response.model_dump_json())
            logger.error(f"Internal server error: {e}")
            continue

        if command["action"] == "create":
            thing = Thing(**command["data"])
            if thing.id in things:
                response = Response(status=400, message="Thing already exists")
            else:
                things[thing.id] = thing
                logger.info(f"Thing created: {thing.model_dump_json()}")
                response = Response(status=201, message="Thing created")

        elif command["action"] == "read":
            if command["id"] in things:
                logger.info(f"Thing read: {things[command["id"]].model_dump_json()}")
                
                response = Response(status=200, message=things[command["id"]].model_dump_json())                
            else:
                response = Response(status=404, message="Thing not found")

        elif command["action"] == "update":
            thing = Thing(**command["data"])
            if thing.id in things:
                things[thing.id] = thing
                logger.info(f"Thing updated: {thing.model_dump_json()}")                
                response = Response(status=200, message="Thing updated")
            else:
                response = Response(status=404, message="Thing not found")

        elif command["action"] == "delete":
            if command["id"] in things:
                del things[command["id"]]
                logger.info(f"Thing deleted: {command["id"]}")
                response = Response(status=200, message="Thing deleted")
            else:
                response = Response(status=404, message="Thing not found")
        else:
            response = Response(status=400, message="Invalid action")
        
        await websocket.send_text(response.model_dump_json())
