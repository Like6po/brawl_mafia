from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import settings_callback, settings_mute_dead_callback, \
    settings_mute_no_players_callback, settings_reg_time_callback, \
    settings_night_time_callback, settings_day_time_callback, settings_voting_time_callback, \
    settings_accept_time_callback, settings_pin_callback, settings_boosts_callback, settings_show_roles_callback, \
    settings_show_votes_callback, settings_show_hello_msg_callback


def settings_kb_show_to_admin(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='🕗 Тайминги',
                                    callback_data=settings_callback.new(action='timings',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🤬 Молчанка',
                                    callback_data=settings_callback.new(action='mute',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='💬 Остальное',
                                    callback_data=settings_callback.new(action='some',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🔚 Выход',
                                    callback_data=settings_callback.new(action='exit',
                                                                        chat_id=chat_id)))
    return kb_obj


########################


def settings_kb_mute(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='🔫 Изгнанные (Мертвые)',
                                    callback_data=settings_callback.new(action='mute_dead',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🚷 Не играющие',
                                    callback_data=settings_callback.new(action='mute_not_players',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='menu',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_mute_dead(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='✅ Удалять',
                                    callback_data=settings_mute_dead_callback.new(action='yes',
                                                                                  chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='❌ Оставлять',
                                    callback_data=settings_mute_dead_callback.new(action='no',
                                                                                  chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='mute',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_mute_no_players(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='✅ Удалять',
                                    callback_data=settings_mute_no_players_callback.new(action='yes',
                                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='❌ Оставлять',
                                    callback_data=settings_mute_no_players_callback.new(action='no',
                                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='mute',
                                                                        chat_id=chat_id)))
    return kb_obj


#########################


def settings_kb_timings(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='🕐 Регистрация',
                                    callback_data=settings_callback.new(action='reg_time',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 Ночь',
                                    callback_data=settings_callback.new(action='night_time',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 День',
                                    callback_data=settings_callback.new(action='day_time',
                                                                        chat_id=chat_id)))
    kb_obj.row(
        InlineKeyboardButton(text='🕐 Голосование',
                             callback_data=settings_callback.new(action='voting_time',
                                                                 chat_id=chat_id)))
    kb_obj.row(
        InlineKeyboardButton(text='🕐 Подтверждение',
                             callback_data=settings_callback.new(action='accept_time',
                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='menu',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_reg_time(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='🕐 30',
                                    callback_data=settings_reg_time_callback.new(action=30,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 45',
                                    callback_data=settings_reg_time_callback.new(action=45,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 60',
                                    callback_data=settings_reg_time_callback.new(action=60,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 80',
                                    callback_data=settings_reg_time_callback.new(action=80,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 120',
                                    callback_data=settings_reg_time_callback.new(action=120,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 240',
                                    callback_data=settings_reg_time_callback.new(action=240,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='timings',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_nighttime(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='🕐 30',
                                    callback_data=settings_night_time_callback.new(action=30,
                                                                                   chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 45',
                                    callback_data=settings_night_time_callback.new(action=45,
                                                                                   chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 60',
                                    callback_data=settings_night_time_callback.new(action=60,
                                                                                   chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 80',
                                    callback_data=settings_night_time_callback.new(action=80,
                                                                                   chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 120',
                                    callback_data=settings_night_time_callback.new(action=120,
                                                                                   chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 240',
                                    callback_data=settings_night_time_callback.new(action=240,
                                                                                   chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='timings',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_daytime(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='🕐 30',
                                    callback_data=settings_day_time_callback.new(action=30,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 45',
                                    callback_data=settings_day_time_callback.new(action=45,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 60',
                                    callback_data=settings_day_time_callback.new(action=60,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 80',
                                    callback_data=settings_day_time_callback.new(action=80,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 120',
                                    callback_data=settings_day_time_callback.new(action=120,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 240',
                                    callback_data=settings_day_time_callback.new(action=240,
                                                                                 chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='timings',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_voting_time(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='🕐 30',
                                    callback_data=settings_voting_time_callback.new(action=30,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 45',
                                    callback_data=settings_voting_time_callback.new(action=45,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 60',
                                    callback_data=settings_voting_time_callback.new(action=60,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 80',
                                    callback_data=settings_voting_time_callback.new(action=80,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 120',
                                    callback_data=settings_voting_time_callback.new(action=120,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 240',
                                    callback_data=settings_voting_time_callback.new(action=240,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='timings',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_accept_time(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='🕐 30',
                                    callback_data=settings_accept_time_callback.new(action=30,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 45',
                                    callback_data=settings_accept_time_callback.new(action=45,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 60',
                                    callback_data=settings_accept_time_callback.new(action=60,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 80',
                                    callback_data=settings_accept_time_callback.new(action=80,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 120',
                                    callback_data=settings_accept_time_callback.new(action=120,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🕐 240',
                                    callback_data=settings_accept_time_callback.new(action=240,
                                                                                    chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='timings',
                                                                        chat_id=chat_id)))
    return kb_obj


#########################


def settings_kb_some(chat_id):
    kb_obj = InlineKeyboardMarkup()

    kb_obj.row(InlineKeyboardButton(text='📍 Пин регистрации',
                                    callback_data=settings_callback.new(action='pin',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='🧨 Включение Бустов',
                                    callback_data=settings_callback.new(action='boosts',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='👤 Показ ролей',
                                    callback_data=settings_callback.new(action='show_roles',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='✋ Тайное голосование',
                                    callback_data=settings_callback.new(action='show_votes',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='👋 Приветственное сообщение',
                                    callback_data=settings_callback.new(action='show_hello_msg',
                                                                        chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='menu',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_pin(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='✅ Да',
                                    callback_data=settings_pin_callback.new(action='yes',
                                                                            chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='❌ Нет',
                                    callback_data=settings_pin_callback.new(action='no',
                                                                            chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='some',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_boosts(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='✅ Да',
                                    callback_data=settings_boosts_callback.new(action='yes',
                                                                               chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='❌ Нет',
                                    callback_data=settings_boosts_callback.new(action='no',
                                                                               chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='some',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_show_roles(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='✅ Да',
                                    callback_data=settings_show_roles_callback.new(action='yes',
                                                                                   chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='❌ Нет',
                                    callback_data=settings_show_roles_callback.new(action='no',
                                                                                   chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='some',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_show_votes(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='✅ Да',
                                    callback_data=settings_show_votes_callback.new(action='yes',
                                                                                   chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='❌ Нет',
                                    callback_data=settings_show_votes_callback.new(action='no',
                                                                                   chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='some',
                                                                        chat_id=chat_id)))
    return kb_obj


def settings_kb_show_hello_msg(chat_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text='✅ Да',
                                    callback_data=settings_show_hello_msg_callback.new(action='yes',
                                                                                       chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='❌ Нет',
                                    callback_data=settings_show_hello_msg_callback.new(action='no',
                                                                                       chat_id=chat_id)))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=settings_callback.new(action='some',
                                                                        chat_id=chat_id)))
    return kb_obj
