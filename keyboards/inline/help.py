from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import help_callback



def help_kb():
    kb_obj = InlineKeyboardMarkup()
    key_phases = InlineKeyboardButton(text='🌗 Фазы',
                                      callback_data=help_callback.new(type='phase'))
    key_roles = InlineKeyboardButton(text='🎭 Бравлеры',
                                     callback_data=help_callback.new(type='roles'))
    key_premium = InlineKeyboardButton(text='💰 Premium',
                                       callback_data=help_callback.new(type='premium'))
    key_back = InlineKeyboardButton(text='↩️ Меню',
                                    callback_data=help_callback.new(type='menu'))
    kb_obj.row(key_phases, key_roles)
    kb_obj.row(key_premium)
    kb_obj.row(key_back)
    return kb_obj


def help_back_kb():
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=help_callback.new(type='kb')))
    return kb_obj


def help_roles_kb():
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text="🙎‍♀️ Шелли",
                                    callback_data=help_callback.new('peace')))
    kb_obj.row(InlineKeyboardButton(text="🐃 Булл",
                                    callback_data=help_callback.new('don')))
    kb_obj.row(InlineKeyboardButton(text="🚑👩🏼‍⚕️ Пэм",
                                    callback_data=help_callback.new('doctor')))
    kb_obj.row(InlineKeyboardButton(text="☂️💃 Пайпер",
                                    callback_data=help_callback.new('whore')))
    kb_obj.row(InlineKeyboardButton(text="🔫🕵️ Кольт",
                                    callback_data=help_callback.new('cop')))
    kb_obj.row(InlineKeyboardButton(text="🦅 Ворон",
                                    callback_data=help_callback.new('mafia')))
    kb_obj.row(InlineKeyboardButton(text="🍾 Барли",
                                    callback_data=help_callback.new('homeless')))
    kb_obj.row(InlineKeyboardButton(text="💣 Тик",
                                    callback_data=help_callback.new('suicide')))
    # kb_obj.row(InlineKeyboardButton(text="🐺 Леон Оборотень",
    #                               callback_data=help_callback.new('werewolf')))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=help_callback.new('kb')))
    return kb_obj


def help_roles_back_kb():
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=help_callback.new(type='roles')))

    return kb_obj
