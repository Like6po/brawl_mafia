from aiogram import types
from aiogram.dispatcher.filters import Command, ChatTypeFilter
from aiogram.utils.markdown import hcode, hbold

from data.db_models import User
from keyboards.inline.callback_datas import profile_callback
from keyboards.inline.profile import profile_kb
from keyboards.inline.shop import shop_kb, gems_kb
from loader import dp, db


@dp.message_handler(Command('profile'), ChatTypeFilter(types.ChatType.PRIVATE))
async def profile(message: types.Message):
    user_data: User = await db.get_player(message.from_user.id)
    await message.answer(f"{hcode(message.from_user.full_name)}\n\n"
                         f"{hbold('🏆 Побед')}: {user_data.wins}\n"
                         f"{hbold('🗡 Поражений')}: {user_data.loses}\n"
                         f"{hbold('💎 Гемы')}: {user_data.money}\n\n"
                         f"{hbold('📂 Документы')}: {user_data.documents}\n"
                         f"{hbold('🕵️‍♂️ Активная роль')}: {user_data.active_roles}",
                         reply_markup=profile_kb())


@dp.callback_query_handler(profile_callback.filter(type='boosters'))
async def profile_boosters(cbq: types.CallbackQuery):
    await cbq.message.edit_text(f"{hbold('📂 Документы (💎 30)')} - если в чате активированы бустеры,"
                                f"и вы являетесь Вороном или Буллом, то при проверке Кольт получит сообщение, "
                                f"что вы - Шелли. Документы используются без ограничений на количество использований "
                                f"за игру.\n\n"
                                f"{hbold('🕵️‍♂️ Активная роль(💎 60)')} - если в чате активированы бустеры, "
                                f" то вы почти гарантированно получите случайную активную роль (не Шелли).",
                                reply_markup=shop_kb())


@dp.callback_query_handler(profile_callback.filter(type='gems'))
async def profile_boosters(cbq: types.CallbackQuery):
    await cbq.message.edit_text(f"{hbold('💎 Гемы')} - валюта, за которую можно приобрести бустеры. "
                                f"За каждую победу вы получаете немного гемов. Также их можно купить за деньги здесь.\n"
                                f"Оплачиваем нужную сумму и жмём кнопку '✅ОПЛАТИЛ!!!✅', чтобы я проверил платеж!",
                                reply_markup=gems_kb(cbq.from_user.id))


