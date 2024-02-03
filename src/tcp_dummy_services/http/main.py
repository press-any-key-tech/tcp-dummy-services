import asyncio
import argparse

from tcp_dummy_services.core import logger
from tcp_dummy_services.core import settings

import sys


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app: FastAPI = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


class MyTest(BaseModel):
    id: str
    name: str


tests: Dict[str, MyTest] = {}


@app.get("/tests/{mytest_id}", response_model=MyTest)
async def read_test(mytest_id: str):
    if mytest_id not in tests:
        raise HTTPException(status_code=404, detail="MyTest not found")
    return tests[mytest_id]


@app.get("/tests", response_model=Dict[str, MyTest])
async def read_tests():
    return tests


@app.post("/tests", response_model=MyTest)
async def create_test(test: MyTest):
    if test.id in tests:
        raise HTTPException(status_code=400, detail="MyTest already exists")
    tests[test.id] = test
    return test


@app.put("/tests/{mytest_id}", response_model=MyTest)
async def update_test(mytest_id: str, test: MyTest):
    if mytest_id not in tests:
        raise HTTPException(status_code=404, detail="MyTest not found")
    tests[mytest_id] = test
    return test


@app.delete("/tests/{mytest_id}", response_model=MyTest)
async def delete_test(mytest_id: str):
    if mytest_id not in tests:
        raise HTTPException(status_code=404, detail="MyTest not found")
    return tests.pop(mytest_id)
