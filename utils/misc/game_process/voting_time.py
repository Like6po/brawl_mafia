import asyncio
from loader import bot
from utils.misc.mailing_process import mailing_day_messages_to_players


async def voting_time(chat_id, chat_obj):

    chat_obj.phase = 'voting'
    message_voting = await mailing_day_messages_to_players(chat_id, chat_obj, bot)
    await asyncio.sleep(chat_obj.vote_time)
    await bot.delete_message(chat_id, message_voting.message_id)







