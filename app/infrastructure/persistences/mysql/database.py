import aiomysql

__all__ = ("Database", )


class Database:

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        dbname: str,
        autocommit: bool = True,
        port: int = 3306,
        pool_min_size: int = 1,
        pool_max_size: int = 10,
        charset: str = 'utf8mb4',
        pool_recycle: int = 60,
        wait_timeout: int = 30
    ):
        self._host = host
        self._user = user
        self._password = password
        self._dbname = dbname
        self._autocommit = autocommit
        self._port = port
        self._charset = charset
        self._pool_min_size = pool_min_size
        self._pool_max_size = pool_max_size
        self._pool_recycle = pool_recycle
        self._wait_timeout = wait_timeout
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            db=self._dbname,
            autocommit=self._autocommit,
            minsize=self._pool_min_size,
            maxsize=self._pool_max_size,
            cursorclass=aiomysql.cursors.DictCursor,
            connect_timeout=1,
            pool_recycle=self._pool_recycle,
            init_command=f"SET wait_timeout={self._wait_timeout}",
        )

    async def check_connection(self):
        async with self.pool.acquire() as conn:
            await conn.ping(reconnect=True)

    async def init_connection(self):
        try:
            await self.connect()
            await self.check_connection()
        except Exception:
            raise

    async def close(self):
        if self.pool:
            self.pool.terminate()
            await self.pool.wait_closed()
            self.pool = None


