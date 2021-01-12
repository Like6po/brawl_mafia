import asyncio
import math
import random
import time
from typing import Optional

from aiogram import types
from aiogram.utils.exceptions import MessageToReplyNotFound, MessageToDeleteNotFound

from data.game_models import Conv
from keyboards.inline.game_process import game_go_to_bot_kb
from keyboards.inline.start import start_join_kb
from loader import bot, Game, db
from utils.misc.game_process.check_end_game import check_end_game
from utils.misc.game_process.day_time import day_time
from utils.misc.game_process.night_results import night_results
from utils.misc.game_process.service_defs import mute_chat, unmute_chat, game_msg_register_is_end_on_time

from utils.misc.game_process.night_time import night_time
from utils.misc.game_process.voting_time import voting_time
from utils.misc.game_process.votings_results import voting_results
from utils.misc.mailing_process import mailing_roles_to_players


async def register_sleeper(time_to_sleep: int, chat_obj: Conv):
    time_start_sleep: int = int(time.time())
    while not chat_obj.extend_time_register and (
            int(time.time()) - time_start_sleep) < time_to_sleep and not chat_obj.register_is_end_ahead_of_time:
        if chat_obj.is_new_player_join and chat_obj.phase == 'starting':
            await bot.edit_message_text(chat_id=chat_obj.id, message_id=chat_obj.register_message_id,
                                        text=f"📢 Подбор открыт!\n\n"
                                             f"👥 Присоединившиеся бравлеры:\n{chat_obj.get_text_registered_players()}",
                                        reply_markup=start_join_kb(chat_obj.id))
            chat_obj.is_new_player_join = False
        await asyncio.sleep(0.7)

    if chat_obj.register_is_end_ahead_of_time:
        return 1

    if chat_obj.extend_time_register:
        chat_obj.extend_time_register = False
        await register_sleeper(int(time_to_sleep + math.fabs((int(time.time()) - time_start_sleep) - time_to_sleep)),
                               chat_obj)


async def timer_to_start_game(message: types.Message, time_to_sleep: int, chat_id: int):
    chat_obj: Conv = Game.get_chat(chat_id)
    if not chat_obj:
        return await message.answer('❌ Произошла ошибка! Игра не создана!')

    await register_sleeper(time_to_sleep // 2, chat_obj)

    if Game.get_chat(chat_id):
        message1: Optional[types.Message] = None
        if not chat_obj.register_is_end_ahead_of_time:
            try:
                message1 = await bot.send_message(chat_id, game_msg_register_is_end_on_time(time_to_sleep),
                                                  reply_to_message_id=message.message_id)
            except MessageToReplyNotFound:
                message1 = await message.answer(game_msg_register_is_end_on_time(time_to_sleep))
        await register_sleeper(time_to_sleep // 2, chat_obj)

        try:
            await message.delete()
        except MessageToDeleteNotFound:
            pass
        try:
            await message1.delete()
        except MessageToDeleteNotFound:
            pass
        except AttributeError:
            pass

    if Game.get_chat(chat_id):
        if len(chat_obj.registered) < 4:
            Game.remove_chat(chat_obj)
            return await message.answer("🙅‍♂️ Подбор закрыт!\nНедостаточно ❌ бравлеров для начала игры!")

        chat_obj.phase = 'night'

    if Game.get_chat(chat_id):
        random.shuffle(chat_obj.registered)
        # регистрируем всех игроков, распределяя роли. все из registered переходят в players
        players_who_need_back_active_role_to_database = chat_obj.register_players()
        for player_id in players_who_need_back_active_role_to_database:
            await db.upd_player(player_id, active_role=1)
        random.shuffle(chat_obj.players)

        print(chat_obj)
        await bot.send_message(chat_id,
                               f"🙅‍♂️ Подбор закончен!\n\n👥 Бравлеры:\n{chat_obj.get_text_alive_players()}\n\n"
                               f"{chat_obj.get_text_alive_roles()}")
        await mute_chat(chat_obj)
        print(f'[{chat_obj.id}] Рассылаю сообщения с ролями!')
        await mailing_roles_to_players(chat_obj, bot)
        await bot.send_message(chat_id, '🌑 Первая ночь в Бравл Сити!\nВы можете узнать, какой вы 👥 Бравлер!',
                               reply_markup=game_go_to_bot_kb())
        await asyncio.sleep(chat_obj.night_time // 3)

    if Game.get_chat(chat_id):
        await bot.send_message(chat_id, '☀️ Первый день в Бравл Сити!\n'
                                        'Вместе с выходом солнца бравлеры узнают, '
                                        'что в городе завелась банда Булла 🐃. '
                                        'Нужно срочно обсудить план действий 🧐!')
        await unmute_chat(chat_obj)
        chat_obj.phase = 'day'
        chat_obj.day += 1
        await asyncio.sleep(chat_obj.day_time)

    while Game.get_chat(chat_id):
        await night_time(chat_id, chat_obj)
        if Game.get_chat(chat_id):
            await night_results(chat_obj)
        if Game.get_chat(chat_id):
            if await check_end_game(chat_id, chat_obj):
                return await unmute_chat(chat_obj)
        if Game.get_chat(chat_id):
            await day_time(chat_id, chat_obj)
        if Game.get_chat(chat_id):
            await voting_time(chat_id, chat_obj)
        if Game.get_chat(chat_id):
            await voting_results(chat_id, chat_obj)
        chat_obj.clear_day_votes()
        chat_obj.move_dead_to_dead()
        if Game.get_chat(chat_id):
            if await check_end_game(chat_id, chat_obj):
                return 1

        print(chat_obj)
