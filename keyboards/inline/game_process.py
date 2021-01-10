from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.game_models import Kill, Heal_self
from keyboards.inline.callback_datas import night_cop_callback, night_vote_callback, night_vote_mafia_callback, \
    day_vote_callback, voting_callback, night_vote_cop_callback


def game_go_to_bot_kb():
    go_to_bot_kb = InlineKeyboardMarkup()
    go_to_bot_kb.add(InlineKeyboardButton(text='▶️ Перейти', url=f't.me/brawl_mafia_bot'))
    return go_to_bot_kb


def kb_night_cop(chat_id):
    cop_kb = InlineKeyboardMarkup()
    cop_kb.row(InlineKeyboardButton(text='👁🔎 Проверить',
                                    callback_data=night_cop_callback.new(action='check',
                                                                         chat_id=chat_id)))
    cop_kb.row(InlineKeyboardButton(text='🔫👿 Изгнать',
                                    callback_data=night_cop_callback.new(action='kill',
                                                                         chat_id=chat_id)))
    return cop_kb


def cb_q_cop_check_kb(chat_id, players):
    users_kb = InlineKeyboardMarkup()
    for player in players:
        if player.role != 'cop':
            users_kb.row(
                InlineKeyboardButton(text=f'{player.name}',
                                     callback_data=night_vote_cop_callback.new(action='check',
                                                                               player_id=player.id,
                                                                               chat_id=chat_id)))
    return users_kb


def cb_q_cop_kill_kb(chat_id, players):
    users_kb = InlineKeyboardMarkup()
    for player in players:
        if player.role != 'cop':
            users_kb.row(
                InlineKeyboardButton(text=f'{player.name}',
                                     callback_data=night_vote_cop_callback.new(action='kill',
                                                                               player_id=player.id,
                                                                               chat_id=chat_id)))
    return users_kb


def kb_night_don(chat_obj):
    users_kb = InlineKeyboardMarkup()
    for player in chat_obj.players:
        if player.role not in ['don', 'mafia']:
            users_kb.row(
                InlineKeyboardButton(text=player.name,
                                     callback_data=night_vote_callback.new(player_id=player.id,
                                                                           chat_id=chat_obj.id)))
    return users_kb


def kb_night_doctor(chat_obj):
    users_kb = InlineKeyboardMarkup()
    for player in chat_obj.players:
        if player.id == chat_obj.doctor.id:
            if Heal_self() not in chat_obj.doctor.effects:
                users_kb.row(
                    InlineKeyboardButton(text=player.name,
                                         callback_data=night_vote_callback.new(player_id=player.id,
                                                                               chat_id=chat_obj.id)))
        else:
            users_kb.row(
                InlineKeyboardButton(text=player.name,
                                     callback_data=night_vote_callback.new(player_id=player.id,
                                                                           chat_id=chat_obj.id)))
    return users_kb


def kb_night_whore(chat_obj):
    users_kb = InlineKeyboardMarkup()
    players = chat_obj.players
    for player in players:
        if player.id != chat_obj.whore.id:
            users_kb.row(
                InlineKeyboardButton(text=f'{player.name}',
                                     callback_data=night_vote_callback.new(player_id=player.id,
                                                                           chat_id=chat_obj.id)))
    return users_kb


def kb_night_homeless(chat_obj):
    users_kb = InlineKeyboardMarkup()
    players = chat_obj.players
    for player in players:
        if player.id != chat_obj.homeless.id:
            users_kb.row(
                InlineKeyboardButton(text=player.name,
                                     callback_data=night_vote_callback.new(player_id=player.id,
                                                                           chat_id=chat_obj.id)))
    return users_kb


def kb_night_mafia(chat_obj):
    users_kb = InlineKeyboardMarkup()
    players = chat_obj.players
    for player in players:
        if player.role in ['don', 'mafia']:
            users_kb.row(InlineKeyboardButton(text=f'🤵🏻 {player.name}',
                                              callback_data=night_vote_mafia_callback.new(player_id=player.id,
                                                                                          chat_id=chat_obj.id)))
        else:
            users_kb.row(InlineKeyboardButton(text=player.name,
                                              callback_data=night_vote_mafia_callback.new(player_id=player.id,
                                                                                          chat_id=chat_obj.id)))
    return users_kb


def kb_voting_time_users(chat_id, players, player_obj):
    users_kb = InlineKeyboardMarkup()
    for player in players:
        if player.id != player_obj.id and Kill() not in player.effects:
            users_kb.row(InlineKeyboardButton(text=player.name,
                                              callback_data=day_vote_callback.new(player_id=player.id,
                                                                                  chat_id=chat_id)))
    return users_kb


def kb_voting_time_accept(chat_id, player_obj, likes=0, dislikes=0):
    accept_kb = InlineKeyboardMarkup()
    if likes == 0 and dislikes == 0:
        accept_kb.row(InlineKeyboardButton(text='👍',
                                           callback_data=voting_callback.new(action='like',
                                                                             player_id=player_obj.id,
                                                                             chat_id=chat_id)),
                      InlineKeyboardButton(text='👎',
                                           callback_data=voting_callback.new(action='dislike',
                                                                             player_id=player_obj.id,
                                                                             chat_id=chat_id)))
    else:
        if likes > 0:
            likes_button = InlineKeyboardButton(text=f'👍{likes}',
                                                callback_data=voting_callback.new(action='like',
                                                                                  player_id=player_obj.id,
                                                                                  chat_id=chat_id))
        else:
            likes_button = InlineKeyboardButton(text='👍',
                                                callback_data=voting_callback.new(action='like',
                                                                                  player_id=player_obj.id,
                                                                                  chat_id=chat_id))
        if dislikes > 0:
            dislikes_button = InlineKeyboardButton(text=f'👎{dislikes}',
                                                   callback_data=voting_callback.new(action='dislike',
                                                                                     player_id=player_obj.id,
                                                                                     chat_id=chat_id))
        else:
            dislikes_button = InlineKeyboardButton(text='👎',
                                                   callback_data=voting_callback.new(action='dislike',
                                                                                     player_id=player_obj.id,
                                                                                     chat_id=chat_id))

        accept_kb.row(likes_button, dislikes_button)
    return accept_kb
