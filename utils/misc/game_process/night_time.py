import asyncio

from data.game_models import Conv
from utils.misc.game_process.service_defs import mute_chat

from keyboards.inline.game_process import game_go_to_bot_kb
from loader import bot
from utils.misc.mailing_process import mailing_night_messages_to_players


async def night_time(chat_id: int, chat_obj: Conv):
    chat_obj.phase = 'night'
    await mailing_night_messages_to_players(chat_obj, chat_id, bot)
    await mute_chat(chat_obj)

    await bot.send_message(chat_id,
                           '🌑 Наступает ночь. '
                           'Все Шелли, населяющие Бравл Сити засыпают 💤, '
                           'просыпается банда Булла и решает, кого же выгнать из города 🔫👿 этой ночью...',
                           reply_markup=game_go_to_bot_kb())
    await asyncio.sleep(chat_obj.night_time)
    chat_obj.clear_effects()
    # тут день
