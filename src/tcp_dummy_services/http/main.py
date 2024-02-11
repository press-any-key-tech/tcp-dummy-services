from tcp_dummy_services.core import logger
from tcp_dummy_services.core import settings

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

from tcp_dummy_services.domain.entities import Thing
from tcp_dummy_services.api.v1.things.services import ReadService, WriteService
from tcp_dummy_services.domain.exceptions import (
    ThingNotFoundException,
    ThingAlreadyExistsException,
)


app: FastAPI = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


@app.get("/things/{id}", response_model=Thing)
async def read_thing(id: str):

    try:
        return await ReadService().get_by_id(id=id)
    except ThingNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"Thing with id [{id}] not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/things", response_model=Dict[str, Thing])
async def list_things():
    try:
        return await ReadService().get_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/things", response_model=Thing)
async def create_things(test: Thing):

    try:
        return await WriteService().create(entity=test)

    except ThingAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail="Thing already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/things/{id}", response_model=Thing)
async def update_thing(id: str, test: Thing):

    try:
        return await WriteService().update(id=id, entity=test)

    except ThingNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"Thing with id [{id}] not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/things/{id}", response_model=Thing)
async def delete_thing(id: str):

    try:
        return await WriteService().delete_by_id(id=id)
    except ThingNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"Thing with id [{id}] not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
