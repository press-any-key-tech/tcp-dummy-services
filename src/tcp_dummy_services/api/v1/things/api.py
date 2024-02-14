""" Api definition
    All validations and mappings should be in the services
"""

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Header,
    Path,
    status,
    HTTPException,
    Response,
)

from tcp_dummy_services.core import logger
from tcp_dummy_services.core import settings

from typing import Dict, List

from tcp_dummy_services.domain.entities import Thing
from tcp_dummy_services.api.v1.things.services import ReadService, WriteService
from tcp_dummy_services.domain.exceptions import (
    ThingNotFoundException,
    ThingAlreadyExistsException,
)


api_router = APIRouter()


@api_router.get("/things/{id}", response_model=Thing)
async def read_thing(id: str):

    try:
        return await ReadService().get_by_id(id=id)
    except ThingNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"Thing with id [{id}] not found")
    except Exception as e:
        logger.exception("Not controlled error")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/things", response_model=List[Thing])
async def list_things():
    try:
        return await ReadService().get_list()
    except Exception as e:
        logger.exception("Not controlled error")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/things", response_model=Thing)
async def create_things(test: Thing):

    try:
        return await WriteService().create(entity=test)

    except ThingAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail="Thing already exists")
    except Exception as e:
        logger.exception("Not controlled error")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.put("/things/{id}", response_model=Thing)
async def update_thing(id: str, test: Thing):

    try:
        return await WriteService().update(id=id, entity=test)

    except ThingNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"Thing with id [{id}] not found")
    except Exception as e:
        logger.exception("Not controlled error")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.delete("/things/{id}", status_code=204)
async def delete_thing(id: str):

    try:
        await WriteService().delete_by_id(id=id)
    except ThingNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"Thing with id [{id}] not found")
    except Exception as e:
        logger.exception("Not controlled error")
        raise HTTPException(status_code=500, detail=str(e))

    return Response(status_code=204)
