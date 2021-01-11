from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import start_callback


def start_kb():
    kb_obj = InlineKeyboardMarkup()
    key_add_to_chat = InlineKeyboardButton(text='🤵🏻 Добавить в чат',
                                           url='http://t.me/brawl_mafia_bot?startgroup=True')
    key_news = InlineKeyboardButton(text='📝 Новости бота',
                                    url='http://t.me/brawl_mafia_news')
    key_chat = InlineKeyboardButton(text='👨‍🦰 Чат для игры',
                                    url='http://t.me/brawl_mafia_chat')
    key_help = InlineKeyboardButton(text='💬 Помощь',
                                    callback_data=start_callback.new(type='help'))
    kb_obj.row(key_add_to_chat, key_news)
    kb_obj.row(key_help, key_chat)
    return kb_obj


def start_join_kb(chat_id):
    join_kb = InlineKeyboardMarkup()
    join_kb.add(InlineKeyboardButton(text='👨‍🦰 Присоединиться', url=f't.me/brawl_mafia_bot?start={chat_id}'))
    return join_kb
