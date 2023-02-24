import ipaddress

import uvicorn
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import ORJSONResponse

from src.api.v1 import base, users, files
from src.core.config import app_settings

app = FastAPI(
    title=app_settings.app_title, docs_url='/api/openapi', redoc_url='/api/redoc', openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)

app.include_router(base.router, prefix='/api/v1')
app.include_router(users.router, prefix='/users')
app.include_router(files.router, prefix='/files')


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    for network in app_settings.BLACK_LIST:
        if ipaddress.ip_address(request.client.host) in ipaddress.ip_network(network):
            return Response('Access denied', status_code=status.HTTP_403_FORBIDDEN)
        continue

    response = await call_next(request)
    return response


if __name__ == '__main__':
    uvicorn.run('main:app', host=app_settings.PROJECT_HOST, port=app_settings.PROJECT_PORT)
