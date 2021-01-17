
from typing import Optional

import aiomysql
from aiomysql import Pool
from pymysql import IntegrityError

from data.db_models import User, Chat
from data import config


class Database:

    def __init__(self) -> None:
        self.pool: Optional[Pool] = None

    async def connect(self) -> None:
        self.pool = await aiomysql.create_pool(host=config.MYSQL_HOST,
                                               port=int(config.MYSQL_PORT),
                                               user=config.MYSQL_USERNAME,
                                               password=config.MYSQL_PASSWORD,
                                               db=config.MYSQL_DB_NAME)

    async def execute(self, sql: str, parameters: tuple = (),
                      fetchone: bool = False, fetchall: bool = False, commit: bool = False) -> Optional[tuple]:
        async with self.pool.acquire() as connector:
            async with connector.cursor() as cur:
                result: Optional[tuple] = None
                print(sql, parameters)
                await cur.execute(sql, parameters)
                if commit:
                    await connector.commit()
                if fetchall:
                    result = await cur.fetchall()
                if fetchone:
                    result = await cur.fetchone()
                print(result)
                return result

    async def get_player(self, user_id) -> Optional[User]:
        sql: str = """
        SELECT * FROM player WHERE user_id=%s
        """
        result = await self.execute(sql, parameters=(user_id), fetchone=True)
        if result:
            return User(result)
        await self.new_player(user_id)
        return await self.get_player(user_id)

    async def get_chat(self, chat_id) -> Optional[Chat]:
        sql: str = """
        SELECT * FROM chat WHERE chat_id=%s
        """
        result = await self.execute(sql, parameters=(chat_id), fetchone=True)
        if result:
            return Chat(result)
        await self.new_chat(chat_id)
        return await self.get_chat(chat_id)

    async def new_player(self, user_id) -> None:
        sql: str = """
        INSERT INTO player (user_id) VALUES (%s)
        """
        await self.execute(sql, parameters=(user_id), commit=True)

    async def new_chat(self, chat_id) -> None:
        sql: str = """
        INSERT INTO chat (chat_id) VALUES (%s)
        """
        await self.execute(sql, parameters=(chat_id), commit=True)

    async def set_player(self, user_id, **kwargs) -> None:
        query: str = f"{', '.join([f'{i}=%s' for i in kwargs])}"
        sql: str = f"""
        UPDATE player SET {query} WHERE user_id={user_id}
        """
        params: tuple = tuple(i for x, i in kwargs.items())
        await self.execute(sql, parameters=params, commit=True)

    async def upd_player(self, user_id, **kwargs) -> None:
        query: str = f"{', '.join([f'{i}={i}+%s' for i in kwargs])}"
        sql: str = f"""
        UPDATE player SET {query} WHERE user_id={user_id}
        """
        params: tuple = tuple(i for x, i in kwargs.items())
        await self.execute(sql, parameters=params, commit=True)

    async def set_chat(self, chat_id, **kwargs) -> None:
        query: str = f"{', '.join([f'{i}=%s' for i in kwargs])}"
        sql: str = f"""
        UPDATE chat SET {query} WHERE chat_id={chat_id}
        """
        params: tuple = tuple(i for x, i in kwargs.items())
        await self.execute(sql, parameters=params, commit=True)

    async def upd_chat(self, chat_id, **kwargs) -> None:
        query: str = f"{', '.join([f'{i}={i}+%s' for i in kwargs])}"
        sql: str = f"""
        UPDATE chat SET {query} WHERE chat_id={chat_id}
        """
        params: tuple = tuple(i for x, i in kwargs.items())
        await self.execute(sql, parameters=params, commit=True)

    async def new_payment(self, payment_id, amount, user_id):
        sql: str = f"""
        INSERT INTO transactions (transaction_id, amount, user_id) VALUES (%s, %s, %s)
        """
        try:
            await self.execute(sql, parameters=(payment_id, amount, user_id), commit=True)
            return True
        except IntegrityError:
            return False
