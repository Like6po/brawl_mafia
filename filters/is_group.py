from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class GroupFilter(BoundFilter):
    async def check(self, message: types.Message):
        return True if message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPERGROUP] else False
