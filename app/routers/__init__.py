from .heartbeat import router as heartbeat_router
from .posts import router as posts_router

__all__ = ("routers", )

routers = (heartbeat_router, posts_router)
