import secrets

import uvicorn
from fastapi import Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status
from starlette.responses import HTMLResponse

from configuration.app import App


app = App().app


def get_current_username(credentials: HTTPBasicCredentials = Depends(HTTPBasic())) -> str:
    correct_username = secrets.compare_digest(credentials.username, "Reei")
    correct_password = secrets.compare_digest(credentials.password, "dnepr1")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/api/docs", response_class=HTMLResponse)
async def get_docs(username: str = Depends(get_current_username)) -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")

if __name__ == "__main__":
    uvicorn.run(app, **config.uvicorn.dict())