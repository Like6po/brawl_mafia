from aiogram.utils.markdown import hlink

from loader import bot
from utils.misc.mailing_process import roles_dict_brawl


async def mute_chat(chat_obj):
    await bot.set_chat_permissions(chat_obj.id,
                                   permissions={'can_send_messages': False, 'can_send_media_messages': False,
                                                'can_send_polls': False, 'can_send_other_messages': False,
                                                'can_change_info': False, 'can_invite_users': False,
                                                'can_add_web_page_previews': False, 'can_pin_messages': False})


async def unmute_chat(chat_obj):
    await bot.set_chat_permissions(chat_obj.id,
                                   permissions={'can_send_messages': True, 'can_send_media_messages': False,
                                                'can_send_polls': False, 'can_send_other_messages': False,
                                                'can_change_info': False, 'can_invite_users': False,
                                                'can_add_web_page_previews': False, 'can_pin_messages': False})


def msg_day_time_dead_from_mafia(player_dead, is_show_dead_roles):
    if is_show_dead_roles == 1:
        return f'В эту ночь бандой Булла из Бравл Сити был изгнан' \
               f' {roles_dict_brawl[player_dead.role]}' \
               f' {hlink(player_dead.name, f"tg://user?id={player_dead.id}")}.'
    else:
        return f'В эту ночь бандой Булла из Бравл Сити был изгнан' \
               f' {hlink(player_dead.name, f"tg://user?id={player_dead.id}")}.'


def msg_day_time_dead_from_cop(player_dead, is_show_dead_roles):
    if is_show_dead_roles == 1:
        return f'В эту ночь из Бравл Сити Кольтом был изган' \
               f' {roles_dict_brawl[player_dead.role]}' \
               f' {hlink(player_dead.name, f"tg://user?id={player_dead.id}")}.'
    else:
        return f'В эту ночь из Бравл Сити Кольтом был изган' \
               f' {hlink(player_dead.name, f"tg://user?id={player_dead.id}")}.'


def msg_day_time_dead_from_afk(player_dead, is_show_dead_roles):
    if is_show_dead_roles == 1:
        return f'В эту ночь от безысходности Бравл Сити покинул' \
               f' {roles_dict_brawl[player_dead.role]}' \
               f' {hlink(player_dead.name, f"tg://user?id={player_dead.id}")}.'
    else:
        return f'В эту ночь от безысходности Бравл Сити покинул' \
               f' {hlink(player_dead.name, f"tg://user?id={player_dead.id}")}.'


def game_msg_register_is_end_on_time(time_to_sleep):
    seconds = time_to_sleep // 2
    if seconds < 60:
        return f'🕗 До окончания подбора осталось {seconds} cек.'
    else:
        minutes = seconds // 60
        seconds = seconds - minutes * 60
        if seconds > 0:
            return f'🕗 До окончания подбора осталось {minutes} мин. {seconds} cек.'
        else:
            return f'🕗 До окончания подбора осталось {minutes} мин.'


def msg_night_res_show_homeless_results(player_obj, killer_obj):
    return f"Этой ночью у бравлера {hlink(player_obj.name, f'tg://user?id={player_obj.id}')} " \
           f"вы видели {hlink(killer_obj.name, f'tg://user?id={killer_obj.id}')}."

