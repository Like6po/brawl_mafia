from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import profile_callback


def profile_kb():
    kb_obj = InlineKeyboardMarkup()
    key_shop = InlineKeyboardButton(text='🛒 Магазин бустеров',
                                    callback_data=profile_callback.new(type='boosters'))
    key_buy_money = InlineKeyboardButton(text='💎 Купить гемы',
                                         callback_data=profile_callback.new(type='gems'))
    kb_obj.row(key_shop)
    kb_obj.row(key_buy_money)
    return kb_obj
