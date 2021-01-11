import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import ChatNotFound
from aiogram.utils.markdown import hcode, hbold

from data.db_models import User
from filters import GroupFilter
from keyboards.inline.profile import profile_kb

from loader import dp, db


@dp.message_handler(GroupFilter(), Command('profile'))
async def profile_conv(message: types.Message):
    user_data: User = await db.get_player(message.from_user.id)
    try:
        await dp.bot.send_message(message.from_user.id,
                                  f"{hcode(message.from_user.full_name)}\n\n"
                                  f"{hbold('🏆 Побед')}: {user_data.wins}\n"
                                  f"{hbold('🗡 Поражений')}: {user_data.loses}\n"
                                  f"{hbold('💎 Гемы')}: {user_data.money}\n\n"
                                  f"{hbold('📂 Документы')}: {user_data.documents}\n"
                                  f"{hbold('🕵️‍♂️ Активная роль')}: {user_data.active_roles}",
                                  reply_markup=profile_kb())
    except ChatNotFound:
        temp_message = await message.reply(
            'Чтобы я отправил вам ответ на команду, перейдите в переписку со мной и нажмите кнопку '
            '"СТАРТ", затем пропишите команду снова.')
        await asyncio.sleep(5)
        await temp_message.delete()
    await message.delete()
