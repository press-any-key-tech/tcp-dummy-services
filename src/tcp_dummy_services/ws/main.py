from tcp_dummy_services.core import logger
from tcp_dummy_services.core import settings

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Tuple
import json

from tcp_dummy_services.domain.entities import Thing, Response
from tcp_dummy_services.core.ws import manager
from tcp_dummy_services.domain.exceptions import DataDecodingException
from tcp_dummy_services.ws.ws_api import (
    ws_create,
    ws_read,
    ws_update,
    ws_delete,
    ws_list,
)

app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    root_path=settings.ROOT_PATH,
)


things: Dict[str, Thing] = {}


def load_data(data: str) -> Dict:
    """Loads data from str string

    Args:
        data (str): _description_

    Returns:
        Dict: _description_
    """

    try:
        payload = json.loads(data)
        return payload
    except json.JSONDecodeError:
        raise DataDecodingException(
            response=Response(status=400, message="Invalid JSON")
        )
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        raise DataDecodingException(
            response=Response(status=500, message="Internal server error")
        )


def decode_parameters(payload: Dict) -> Tuple[str, str]:
    """Loads data from str string

    Args:
        data (str): _description_

    Returns:
        Dict: _description_
    """

    # Switch command action
    return (
        Thing(**payload["data"]) if "data" in payload else None,
        payload["id"] if "id" in payload else None,
    )


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:

        while True:
            data = await websocket.receive_text()
            try:
                payload = load_data(data)

                logger.debug(f"Received data: {payload}")
                entity, entity_id = decode_parameters(payload)

                if payload["action"] == "create":
                    response = await ws_create(entity=entity)
                elif payload["action"] == "read":
                    response = await ws_read(id=entity_id)
                elif payload["action"] == "update":
                    response = await ws_update(id=entity_id, entity=entity)
                elif payload["action"] == "delete":
                    response = await ws_delete(id=entity_id)
                else:
                    response = Response(status=400, message="Invalid action")

            except DataDecodingException as e:
                response = e.response
            except Exception as ex:
                response = Response(status=500, message=f"Server error: {str(ex)}")

            await websocket.send_text(response.model_dump_json())

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.debug("Client disconnected")
