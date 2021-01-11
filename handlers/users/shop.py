from typing import List

import aiohttp
from aiogram import types
from aiogram.utils.markdown import hbold, hcode
from aiohttp import ContentTypeError

from data.config import qiwi_token, qiwi_number, admins
from data.db_models import User
from data.payment_models import Payment
from keyboards.inline.callback_datas import shop_callback
from keyboards.inline.profile import profile_kb
from loader import dp, db


@dp.callback_query_handler(shop_callback.filter(type='back'))
async def back_to_profile(cbq: types.CallbackQuery):
    user_data: User = await db.get_player(cbq.from_user.id)
    await cbq.message.edit_text(f"{hcode(cbq.from_user.full_name)}\n\n"
                                f"{hbold('🏆 Побед')}: {user_data.wins}\n"
                                f"{hbold('🗡 Поражений')}: {user_data.loses}\n"
                                f"{hbold('💎 Гемы')}: {user_data.money}\n\n"
                                f"{hbold('📂 Документы')}: {user_data.documents}\n"
                                f"{hbold('🕵️‍♂️ Активная роль')}: {user_data.active_roles}",
                                reply_markup=profile_kb())


@dp.callback_query_handler(shop_callback.filter(type='document'))
async def back_to_profile(cbq: types.CallbackQuery):
    user_data: User = await db.get_player(cbq.from_user.id)
    if not user_data.money >= 30:
        return await cbq.answer('Недостаточно гемов!')
    await db.upd_player(cbq.from_user.id, money=-30, documents=1)
    return await cbq.answer(f'Успешно приобретено!\n'
                            f'Теперь у вас:\n'
                            f'📂 {user_data.documents + 1}\n'
                            f'💎 {user_data.money - 30}',
                            show_alert=True)


@dp.callback_query_handler(shop_callback.filter(type='active_role'))
async def back_to_profile(cbq: types.CallbackQuery):
    user_data: User = await db.get_player(cbq.from_user.id)
    if not user_data.money >= 60:
        return await cbq.answer('Недостаточно гемов!')
    await db.upd_player(cbq.from_user.id, money=-60, active_role=1)
    return await cbq.answer(f'Успешно приобретено!\n'
                            f'Теперь у вас:\n'
                            f'🕵️‍♂️ {user_data.active_roles + 1}\n'
                            f'💎 {user_data.money - 60}',
                            show_alert=True)


async def info(number, token) -> List[Payment]:
    headers = {"authorization": f"Bearer {token}"}
    url = "https://edge.qiwi.com/payment-history/v2/persons/" + number + "/payments?rows=10&operation=IN"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            try:
                result = (await resp.json())['data']
            except ContentTypeError:
                for admin in admins:
                    await dp.bot.send_message(chat_id=admin, text='QIWI TOKEN ERROR!!!')
                return [Payment(1, 0, None)]
    data: list = []
    for transaction in result:
        if transaction["status"] == "SUCCESS":
            data.append(Payment(transaction["txnId"], transaction["total"]["amount"], transaction["comment"]))
    return data


@dp.callback_query_handler(shop_callback.filter(type='pay'))
async def back_to_profile(cbq: types.CallbackQuery):
    transactions: List[Payment] = await info(qiwi_number, qiwi_token)

    for transaction in transactions:
        if not transaction.comment:
            continue
        comment = transaction.comment.split(':')
        if len(comment) != 3:
            continue
        if comment[0] != 'brawl_mafia':
            continue
        amount = int(comment[1])
        user_id = int(comment[2])
        if user_id != cbq.from_user.id:
            continue
        if not await db.new_payment(transaction.id, transaction.amount, user_id):
            continue

        amount_money_dict = {30: 100,
                             80: 300,
                             120: 500,
                             250: 100,
                             600: 2500,
                             1000: 5000}

        await db.upd_player(user_id, money=amount_money_dict[amount])

        await cbq.message.edit_text(f'Успешно совершена оплата на 💎 {amount_money_dict[amount]}! Валюта зачислена!')
        break
    else:
        await cbq.answer('Оплаты не найдено!\nПопробуйте через 10 секунд!', show_alert=True)
        user_data: User = await db.get_player(cbq.from_user.id)
        await cbq.message.edit_text(f"{hcode(cbq.from_user.full_name)}\n\n"
                                    f"{hbold('🏆 Побед')}: {user_data.wins}\n"
                                    f"{hbold('🗡 Поражений')}: {user_data.loses}\n"
                                    f"{hbold('💎 Гемы')}: {user_data.money}\n\n"
                                    f"{hbold('📂 Документы')}: {user_data.documents}\n"
                                    f"{hbold('🕵️‍♂️ Активная роль')}: {user_data.active_roles}",
                                    reply_markup=profile_kb())
