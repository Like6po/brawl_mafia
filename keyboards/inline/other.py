from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def only_in_conv():
    kb_obj = InlineKeyboardMarkup()
    key_add_to_chat = InlineKeyboardButton(text='🤵🏻 Добавить в чат',
                                           url='http://t.me/brawl_mafia_bot?startgroup=True')
    kb_obj.row(key_add_to_chat)
    return kb_obj
