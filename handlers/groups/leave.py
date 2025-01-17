import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink

from filters import GroupFilter
from loader import Game, dp

from utils.misc.mailing_process import roles_dict_brawl


@dp.message_handler(Command('leave'), GroupFilter())
async def leave(message: types.Message):
    chat_obj = Game.get_chat(message.chat.id)
    if not chat_obj:
        await message.delete()
        temp_message = await message.answer(f'⚠️ {message.from_user.get_mention()}, сначала нужно начать новую игру!')
        await asyncio.sleep(3)
        return await temp_message.delete()

    if chat_obj.phase != 'starting':
        player_obj = chat_obj.get_player(message.from_user.id)
        if not player_obj:
            return await message.delete()

        chat_obj.kill(player_obj)
        return await message.reply(f"☠️ {hlink(player_obj.name, f'tg://user?id={player_obj.id}')} забомбил 🔥 и ливнул!"
                                   f" Его персонаж был - {roles_dict_brawl[player_obj.role]}")

    player_obj = chat_obj.get_registered_player(message.from_user.id)
    if not player_obj:
        return await message.reply('⚠️ Вы не участвуете в подборе игроков!')

    chat_obj.registered.remove(player_obj)
    chat_obj.is_new_player_join = True
    await message.reply('⚠️ Вы покинули подбор игроков!')
