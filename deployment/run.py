import uvicorn

from settings import settings


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.server_host,
        port=settings.server_port,
        log_level=settings.log_level,
        reload=True
    )
