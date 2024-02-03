from tcp_dummy_services.core import logger
from tcp_dummy_services.core import settings

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

from tcp_dummy_services.domain.entities import Thing

app: FastAPI = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


things: Dict[str, Thing] = {}


@app.get("/things/{id}", response_model=Thing)
async def read_test(id: str):
    if id not in things:
        raise HTTPException(status_code=404, detail="Thing not found")
    return things[id]


@app.get("/things", response_model=Dict[str, Thing])
async def read_things():
    return things


@app.post("/things", response_model=Thing)
async def create_test(test: Thing):
    if test.id in things:
        raise HTTPException(status_code=400, detail="Thing already exists")
    things[test.id] = test
    return test


@app.put("/things/{id}", response_model=Thing)
async def update_test(id: str, test: Thing):
    if id not in things:
        raise HTTPException(status_code=404, detail="Thing not found")
    things[id] = test
    return test


@app.delete("/things/{id}", response_model=Thing)
async def delete_test(id: str):
    if id not in things:
        raise HTTPException(status_code=404, detail="Thing not found")
    return things.pop(id)
