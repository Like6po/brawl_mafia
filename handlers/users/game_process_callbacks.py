from aiogram import types
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.utils.markdown import hlink

from data.game_models import Kill, Mute, Heal_self
from keyboards.inline.callback_datas import night_cop_callback, night_vote_callback, night_vote_cop_callback, \
    night_vote_mafia_callback, day_vote_callback, voting_callback
from keyboards.inline.game_process import cb_q_cop_check_kb, cb_q_cop_kill_kb
from loader import dp, Game


@dp.callback_query_handler(voting_callback.filter())
async def day_vote_voting(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    vote_to_id = int(callback_data.get('player_id'))
    action = callback_data.get('action')

    chat_obj = Game.get_chat(chat_id)
    if not chat_obj:
        return await cbq.answer('Игры не существует!')
    if chat_obj.phase != 'voting1':
        return await cbq.answer('Это доступно только во время голосования!')

    player = chat_obj.get_player(cbq.from_user.id)
    if not player:
        return await cbq.answer('Вы не участвуете в данной игре!')
    if Kill() in player.effects:
        return await cbq.answer('Изгнанные не голосуют!')
    if Mute() in player.effects:
        return await cbq.answer('Вы отдыхаете после Пайпер!')

    vote_to_player = chat_obj.get_player(vote_to_id)
    if not vote_to_player:
        return await cbq.answer('Такого Бравлера нет!')
    if Kill() in vote_to_player.effects:
        return await cbq.answer('Этот бравлер уже изгнан!')

    if vote_to_player.id == player.id:
        return await cbq.answer('Нельзя голосовать против себя!')

    if action in ['like', 'dislike']:
        if player in chat_obj.accept_votes_dislike:
            chat_obj.accept_votes_dislike.remove(player)

        if player in chat_obj.accept_votes_like:
            chat_obj.accept_votes_like.remove(player)

        if action == 'like':
            chat_obj.accept_votes_like.append(player)

        elif action == 'dislike':
            chat_obj.accept_votes_dislike.append(player)

        chat_obj.is_new_vote = True

        if (len(set(chat_obj.accept_votes_like)) + len(set(
                chat_obj.accept_votes_dislike)) - 1) >= chat_obj.get_alive_players_count():
            chat_obj.is_accept_end = True

        return await cbq.answer('Выбор сделан!')
    await cbq.answer()


@dp.callback_query_handler(day_vote_callback.filter(), ChatTypeFilter(types.ChatType.PRIVATE))
async def day_vote(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    vote_to_id = int(callback_data.get('player_id'))

    chat_obj = Game.get_chat(chat_id)
    if not chat_obj:
        return await cbq.answer('Игры не существует!')
    if chat_obj.phase != 'voting':
        return await cbq.answer('Это доступно только во время голосования!')

    player = chat_obj.get_player(cbq.from_user.id)
    if not player:
        return await cbq.answer('Вы не участвуете в данной игре!')
    if player.day_voting_to:
        return await cbq.answer('Вы уже проголосовали!')
    if Kill() in player.effects:
        return await cbq.answer('Изгнанные не голосуют!')
    if Mute() in player.effects:
        return await cbq.answer('Вы отдыхаете после Пайпер!')

    vote_to_player = chat_obj.get_player(vote_to_id)
    if not vote_to_player:
        return await cbq.answer('Ошибка! Такого Бравлера нет!')
    if Kill() in vote_to_player.effects:
        return await cbq.answer('Этот бравлер уже изгнан!')
    if vote_to_player.id == player.id:
        return await cbq.answer('Нельзя голосовать против себя!')

    player.day_voting_to = vote_to_id
    chat_obj.day_votes_ids.append(vote_to_id)

    await cbq.message.edit_text('Выбор сделан')
    if chat_obj.is_show_day_votes:
        return await dp.bot.send_message(chat_obj.id, f"{hlink(player.name, f'tg://user?id={player.id}')} "
                                                      f"проголосовал за изгнание"
                                                      f" {hlink(vote_to_player.name, f'tg://user?id={vote_to_player.id}')}!")

    else:
        return await dp.bot.send_message(chat_obj.id, f"{hlink(player.name, f'tg://user?id={player.id}')} "
                                                      f"проголосовал!")


@dp.callback_query_handler(night_cop_callback.filter(), ChatTypeFilter(types.ChatType.PRIVATE))
async def night_cop(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = callback_data.get('action')

    chat_obj = Game.get_chat(chat_id)
    if not chat_obj:
        return await cbq.answer('Игры не существует!')
    if chat_obj.phase != 'night':
        return await cbq.answer('Это доступно только ночью!')

    player = chat_obj.get_player(cbq.from_user.id)
    if not player:
        return await cbq.answer('Вы не участвуете в данной игре!')
    if player.role != 'cop':
        return await cbq.answer('Вы не Кольт!')
    if Kill() in player.effects:
        return await cbq.answer('Изгнанные не выбирают!')
    if Mute() in player.effects:
        return await cbq.answer('Вы отдыхаете после Пайпер!')

    chat_obj.cop.kill_to = None
    chat_obj.cop.check_to = None
    if action == 'check':

        await cbq.message.edit_text(text='Кого вы хотите проверить?',
                                    reply_markup=cb_q_cop_check_kb(chat_obj.id,
                                                                   chat_obj.players))
    elif action == 'kill':

        await cbq.message.edit_text(text='Кого вы хотите изгнать?',
                                    reply_markup=cb_q_cop_kill_kb(chat_obj.id,
                                                                  chat_obj.players))


@dp.callback_query_handler(night_vote_mafia_callback.filter(), ChatTypeFilter(types.ChatType.PRIVATE))
async def night_vote_mafia(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    vote_to_id = int(callback_data.get('player_id'))

    chat_obj = Game.get_chat(chat_id)
    if not chat_obj:
        return await cbq.answer('Игры не существует!')
    if chat_obj.phase != 'night':
        return await cbq.answer('Это доступно только ночью!')

    player = chat_obj.get_player(cbq.from_user.id)
    if not player:
        return await cbq.answer('Вы не участвуете в данной игре!')
    if player.role not in ['mafia', 'don']:
        return await cbq.answer('Это доступно только банде Булла!')
    if player.go_to:
        return await cbq.answer('Вы уже проголосовали!')
    if Kill() in player.effects:
        return await cbq.answer('Изгнанные не голосуют!')
    if Mute() in player.effects:
        return await cbq.answer('Вы отдыхаете после Пайпер!')

    vote_to_player = chat_obj.get_player(vote_to_id)
    if not vote_to_player:
        return await cbq.answer('Ошибка! Такого Бравлера нет!')
    if vote_to_player.id == player.id:
        return await cbq.answer('Нельзя выбрать себя!')

    player.go_to = vote_to_id
    chat_obj.mafia_votes_ids.append(vote_to_id)

    await cbq.message.edit_text('Выбор сделан!')

    for mafia in chat_obj.mafia:
        await dp.bot.send_message(mafia.id,
                                  f"{hlink(player.name, f'tg://user?id={player.id}')} "
                                  f"проголосовал за "
                                  f"{hlink(vote_to_player.name, f'tg://user?id={vote_to_player.id}')}")
    if chat_obj.don:
        await dp.bot.send_message(chat_obj.don.id,
                                  f"{hlink(player.name, f'tg://user?id={player.id}')} "
                                  f"проголосовал за "
                                  f"{hlink(vote_to_player.name, f'tg://user?id={vote_to_player.id}')}")


@dp.callback_query_handler(night_vote_cop_callback.filter(), ChatTypeFilter(types.ChatType.PRIVATE))
async def night_vote_cop(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    vote_to_id = int(callback_data.get('player_id'))
    action = callback_data.get('action')

    chat_obj = Game.get_chat(chat_id)
    if not chat_obj:
        return await cbq.answer('Игры не существует!')
    if chat_obj.phase != 'night':
        return await cbq.answer('Это доступно только ночью!')

    player = chat_obj.get_player(cbq.from_user.id)
    if not player:
        return await cbq.answer('Вы не участвуете в данной игре!')
    if player.role != 'cop':
        return await cbq.answer('Вы не Кольт!')
    if player.check_to:
        return await cbq.answer('Вы уже сделали выбор!')
    if Kill() in player.effects:
        return await cbq.answer('Изгнанные не голосуют!')
    if Mute() in player.effects:
        return await cbq.answer('Вы отдыхаете после Пайпер!')

    vote_to_player = chat_obj.get_player(vote_to_id)
    if not vote_to_player:
        return await cbq.answer('Ошибка! Такого Бравлера нет!')
    if vote_to_player.id == player.id:
        return await cbq.answer('Нельзя выбрать себя!')

    if action == 'check':
        player.check_to = vote_to_id

        await cbq.message.edit_text(text='Выбор сделан!')
        await dp.bot.send_message(chat_obj.id,
                                  'Кольт пошел на поиски банды Булла...')
    elif action == 'kill':
        player.kill_to = vote_to_id

        await cbq.message.edit_text(text='Выбор сделан!')
        await dp.bot.send_message(chat_obj.id,
                                  'Кольт изгоняет кого-то из Бравл Сити...')


@dp.callback_query_handler(night_vote_callback.filter(), ChatTypeFilter(types.ChatType.PRIVATE))
async def night_vote(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    vote_to_id = int(callback_data.get('player_id'))

    chat_obj = Game.get_chat(chat_id)
    if not chat_obj:
        return await cbq.answer('Игры не существует!')
    if chat_obj.phase != 'night':
        return await cbq.answer('Это доступно только ночью!')

    player = chat_obj.get_player(cbq.from_user.id)
    if not player:
        return await cbq.answer('Вы не участвуете в данной игре!')
    if Kill() in player.effects:
        return await cbq.answer('Изгнанные не голосуют!')
    if Mute() in player.effects:
        return await cbq.answer('Вы отдыхаете после Пайпер!')

    vote_to_player = chat_obj.get_player(vote_to_id)
    if not vote_to_player:
        return await cbq.answer('Ошибка! Такого Бравлера нет!')

    if player.role == 'doctor':
        if vote_to_id == player.id:
            if Heal_self() in player.effects:

                return await cbq.answer('Нельзя спасти себя дважды!')

        player.go_to = vote_to_id

        await cbq.message.edit_text('Выбор сделан!')
        await dp.bot.send_message(chat_obj.id,
                                  'Пэм отправилась к нуждающимся в помощи')

    elif player.role == 'don':
        if vote_to_id == player.id:
            return await cbq.answer('Нельзя проверить себя!')

        elif vote_to_player.role == 'mafia':
            return await cbq.answer('Нельзя проверять свою банду!')

        player.check_to = vote_to_id

        await cbq.message.edit_text('Выбор сделан!')
        await dp.bot.send_message(chat_obj.id,
                                  'Булл отправился в кусты, чтобы проследить за кое-кем...')

    elif player.role == 'whore':
        if vote_to_id == player.id:
            return await cbq.answer('Нельзя выбрать себя!')

        player.go_to = vote_to_id

        await cbq.message.edit_text('Выбор сделан!')
        await dp.bot.send_message(chat_obj.id,
                                  'Пайпер устроила кому-то классную ночь!')

    elif player.role == 'homeless':
        if vote_to_id == player.id:
            return await cbq.answer('Нельзя выбрать себя!')

        player.go_to = vote_to_id

        await cbq.message.edit_text('Выбор сделан!')
        await dp.bot.send_message(chat_obj.id,
                                  'Барли пошел искать пиво для своего бара...')
