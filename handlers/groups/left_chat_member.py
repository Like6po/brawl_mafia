

from aiogram import types
from aiogram.utils.markdown import hlink

from filters import GroupFilter
from loader import Game, dp
from utils.misc.mailing_process import roles_dict_brawl


@dp.message_handler(GroupFilter(),
                    content_types=[types.ContentType.LEFT_CHAT_MEMBER])
async def left_member(message: types.Message):
    left_id = message.left_chat_member.id
    if left_id == (await dp.bot.get_me()).id:
        if Game.get_chat(message.chat.id):
            Game.remove_chat(message.chat.id)
    else:
        chat_obj = Game.get_chat(message.chat.id)
        if chat_obj:
            player_obj = chat_obj.get_player(message.left_chat_member.id)
            if player_obj:
                chat_obj.kill(player_obj)
                await message.answer(
                    f"☠️ {hlink(player_obj.name, f'tg://user?id={player_obj.id}')} забомбил 🔥 и ливнул!"
                    f" Его персонаж был - {roles_dict_brawl[player_obj.role]}")
