import asyncio

from data.game_models import Kill
from loader import Game, bot
from utils.misc.game_process.service_defs import msg_day_time_dead_from_mafia, msg_day_time_dead_from_cop, \
    msg_day_time_dead_from_afk, unmute_chat

from utils.misc.game_process.night_results import night_results

from utils.misc.game_process.check_end_game import check_end_game
from utils.misc.game_process.voting_time import voting_time


async def day_time(chat_id, chat_obj):

    chat_obj.clear_effects()
    chat_obj.day += 1
    chat_obj.phase = 'day'

    await bot.send_message(chat_id,
                           f"Наступает {chat_obj.day} день. "
                           f"Бравл Сити просыпается, а солнце приносит с собой неприятные вести, "
                           f"которые стоит обсудить!")
    await unmute_chat(chat_obj)
    await bot.send_message(chat_id,
                           f"👥 Живые жители: \n\n{chat_obj.get_text_alive_roles()}")
    await asyncio.sleep(chat_obj.day_time)




