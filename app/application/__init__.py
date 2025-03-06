from app.application.dic import DIC
from app.application.post_service import PostService
from app.infrastructure.persistences.mysql.database import Database
from app.infrastructure.persistences.memory_db.database import database
from app.infrastructure.repositories import MemoryUserRepository, MemoryPostRepository, MySQLPostRepository
from app.config.config import config


async def application_startup():
    mysql_conf = config["databases"]["mysql"]
    mysql_database = Database(
        host=mysql_conf["host"],
        port=mysql_conf["port"],
        user=mysql_conf["user"],
        password=mysql_conf["password"],
        dbname=mysql_conf["dbname"],
    )

    await mysql_database.init_connection()

    user_repository = MemoryUserRepository(database=database)
    # post_repository = MemoryPostRepository(database=database)
    post_repository = MySQLPostRepository(database=mysql_database)

    DIC.post_service = PostService(
        user_repository=user_repository,
        post_repository=post_repository
    )

    DIC.mysql_database = mysql_database


async def application_shutdown():
    if DIC.mysql_database:
        await DIC.mysql_database.close()


async def application_health_check():
    await DIC.mysql_database.check_connection()
