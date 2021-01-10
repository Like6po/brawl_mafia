from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import db


async def get_data_private(user_id: int):
    user_data = await db.get_player(user_id)
    if user_data is None:
        await db.new_player(user_id)
        user_data = await db.get_player(user_id)
    chat_data = None
    return user_data, chat_data


async def get_data_group(user_id: int, chat_id: int):
    user_data = await db.get_player(user_id)
    if user_data is None:
        await db.new_player(user_id)
        user_data = await db.get_player(user_id)
    chat_data = await db.get_chat(chat_id)
    if chat_data is None:
        await db.new_chat(chat_id)
        chat_data = await db.get_chat(chat_id)
    return user_data, chat_data


class DataMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):

        if message.chat.type == types.ChatType.PRIVATE:
            data['user'], data['chat'] = await get_data_private(message.from_user.id)
        elif message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]:
            data['user'], data['chat'] = await get_data_group(message.from_user.id, message.chat.id)
        print(data)

    # async def on_process_callback_query(self, cbq: types.CallbackQuery, data: dict):
    #     if cbq.message.chat.type == types.ChatType.PRIVATE:
    #         data['user'], data['chat'] = await get_data_private(cbq.from_user.id)
    #     elif cbq.message.chat.type in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]:
    #         data['user'], data['chat'] = await get_data_group(cbq.from_user.id, cbq.message.chat.id)