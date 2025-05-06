import secrets
from kafka.producer import create_topics
import uvicorn
from fastapi import Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status
from starlette.responses import HTMLResponse
import config
from configuration.app import App

app = App().app


@app.get("/api/docs", response_class=HTMLResponse)
async def get_docs() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")


@app.on_event("startup")
async def startup_event():
    await create_topics()


if __name__ == "__main__":
    uvicorn.run(app, **config.uvicorn.dict())
