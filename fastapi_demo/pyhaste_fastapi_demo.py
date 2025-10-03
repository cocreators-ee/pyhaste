#!/usr/bin/env -S uv run
import asyncio
import random
from io import StringIO

import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import PlainTextResponse

import pyhaste.async_analyzer
from pyhaste.async_analyzer import measure, measure_wrap_async, report

app = FastAPI()


@app.get("/")
@measure_wrap_async("root")
async def root(request: Request, name: str = "Anon"):
    await asyncio.sleep(random.uniform(0.05, 0.15))
    with measure("root.make_response"):
        await asyncio.sleep(random.uniform(0.05, 0.15))
        return {"message": f"Welcome to {request.base_url}, {name}!"}


async def measure_middleware(request: Request, call_next):
    """
    Wrap requests to pyhaste
    """
    with measure("middleware"):
        await asyncio.sleep(random.uniform(0.05, 0.15))
        return await call_next(request)


@app.get("/debug", response_class=PlainTextResponse)
async def debug():
    # Print Pyhaste report to console, and return it as a response
    output_buf = StringIO()
    old = pyhaste.async_analyzer.Console.file
    pyhaste.async_analyzer.Console.file = output_buf
    report()
    pyhaste.async_analyzer.Console.file = old
    output = output_buf.getvalue()
    print(output)
    return output


app.middleware("http")(measure_middleware)

if __name__ == "__main__":
    uvicorn.run("pyhaste_fastapi_demo:app", host="0.0.0.0", port=8123, reload=True)
