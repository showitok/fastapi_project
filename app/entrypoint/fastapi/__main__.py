import uvicorn

from app.config.config import config

if __name__ == "__main__":
    uvicorn.run(
        "app.entrypoint.fastapi.factory:create_app",
        host="0.0.0.0",
        port=8080,
        access_log=False,
        reload=config.app.debug,
        reload_dirs=["app"],
        factory=True
    )
