from tcp_dummy_services.core import logger
from tcp_dummy_services.core import settings

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, List
import json

from tcp_dummy_services.domain.entities import Thing, Response
from tcp_dummy_services.core.ws import manager
from tcp_dummy_services.api.v1.things.services import ReadService, WriteService
from tcp_dummy_services.domain.exceptions import (
    ThingNotFoundException,
    ThingAlreadyExistsException,
)


async def ws_create(entity: Thing) -> Thing:
    """
    Create a new thing

    Args:
        entity (Thing): Thing object

    Returns:
        Thing: Thing object
    """

    try:
        body: Thing = await WriteService().create(entity=entity)
        return Response(status=201, message="Thing created", body=body)
    except ThingAlreadyExistsException as e:
        return Response(status=400, message="Thing already exists")
    except Exception as e:
        logger.exception("Not controlled error")
        return Response(status_code=500, detail=str(e))


async def ws_read(id: str) -> Thing:
    """
    Read a thing by id

    Args:
        id (str): Thing id

    Returns:
        Thing: Thing object
    """

    try:
        body: Thing = await ReadService().get_by_id(id=id)
        return Response(status=200, message="Thing created", body=body)

    except ThingNotFoundException as e:
        return Response(status=404, message=f"Thing with id [{id}] not found")
    except Exception as e:
        logger.exception("Not controlled error")
        return Response(status=500, message=str(e))


async def ws_update(id: str, entity: Thing) -> Thing:
    """
    Update a thing by id

    Args:
        id (str): Thing id
        entity (Thing): Thing object

    Returns:
        Thing: Thing object
    """

    try:
        body: Thing = await WriteService().update(id=id, entity=entity)
        return Response(status=200, message="Thing updated", body=body)
    except ThingNotFoundException as e:
        return Response(status=404, message=f"Thing with id [{id}] not found")
    except Exception as e:
        logger.exception("Not controlled error")
        return Response(status=500, message=str(e))


async def ws_delete(id: str):
    """
    Delete a thing by id

    Args:
        id (str): Thing id
    """

    try:
        await WriteService().delete_by_id(id=id)
        return Response(status=204, message="Thing deleted")
    except ThingNotFoundException as e:
        return Response(status=404, message=f"Thing with id [{id}] not found")
    except Exception as e:
        logger.exception("Not controlled error")
        return Response(status=500, message=str(e))


async def ws_list():
    """
    List all things

    Returns:
        List[Thing]: List of things
    """

    try:
        body: List[Thing] = await ReadService().get_list()
        return Response(status=200, message="Things listed", body=body)
    except Exception as e:
        logger.exception("Not controlled error")
        return Response(status=500, message=str(e))
