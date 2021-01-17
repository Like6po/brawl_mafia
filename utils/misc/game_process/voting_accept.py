import asyncio
import time

from aiogram.utils.exceptions import RetryAfter
from aiogram.utils.markdown import hlink

from data.game_models import Dead_day
from keyboards.inline.game_process import kb_voting_time_accept
from loader import Game, bot
from utils.misc.mailing_process import roles_dict_brawl


async def voting_accept_timer(chat_obj, time_to_sleep, vote_to_player, message_accept):
    time_start_sleep = int(time.time())
    d_likes = 0
    d_dislikes = 0
    while (int(time.time()) - time_start_sleep) < time_to_sleep and not chat_obj.is_accept_end:
        if chat_obj.is_new_vote:
            try:
                new_d_likes = len(set(chat_obj.accept_votes_like))
                new_d_dislikes = len(set(chat_obj.accept_votes_dislike))
                if new_d_likes != d_likes or new_d_dislikes != d_dislikes:
                    await bot.edit_message_text(chat_id=chat_obj.id, message_id=message_accept.message_id,
                                                text=f"Больше всего голосов набрал Бравлер "
                                                     f"{hlink(vote_to_player.name, f'tg://user?id={vote_to_player.id}')},"
                                                     f" изгоняем его?",
                                                reply_markup=kb_voting_time_accept(chat_obj.id, vote_to_player,
                                                                                   likes=new_d_likes,
                                                                                   dislikes=new_d_dislikes))
                    d_likes = new_d_likes
                    d_dislikes = new_d_dislikes

            except Exception as e:
                print('ошибка voting timer ', e)

            chat_obj.is_new_vote = False
        await asyncio.sleep(1)


async def voting_accept(chat_id, chat_obj, player_obj):
    if Game.get_chat(chat_id):
        chat_obj.phase = 'voting1'
        message_accept = await bot.send_message(chat_id,
                                                f"Больше всего голосов набрал Бравлер "
                                                f"{hlink(player_obj.name, f'tg://user?id={player_obj.id}')},"
                                                f" изгоняем его?",
                                                reply_markup=kb_voting_time_accept(chat_id, player_obj))
        await voting_accept_timer(chat_obj, chat_obj.accept_time, player_obj, message_accept)
        await bot.delete_message(chat_id, message_accept.message_id)
        if Game.get_chat(chat_id):
            likes = len(set(chat_obj.accept_votes_like))
            dislikes = len(set(chat_obj.accept_votes_dislike))
            if likes > dislikes:

                chat_obj.kill(player_obj, reason=Dead_day())

                if chat_obj.is_show_dead_roles:
                    await bot.send_message(chat_id,
                                           f"Бравлеры изгнали {hlink(player_obj.name, f'tg://user?id={player_obj.id}')}"
                                           f" и он оказался {roles_dict_brawl[player_obj.role]}!")
                else:
                    await bot.send_message(chat_id,
                                           f"Бравлеры изгнали {hlink(player_obj.name, f'tg://user?id={player_obj.id}')}")


                try:
                    return await bot.send_message(player_obj.id, 'Тебя изгнали из Бравл Сити на дневном собрании!')
                except RetryAfter as e:
                    await asyncio.sleep(e.timeout)
                await asyncio.sleep(0.1)
            else:

                return await bot.send_message(chat_id, 'Бравлеры не пришли к общему решению и никого не изгнали.')
