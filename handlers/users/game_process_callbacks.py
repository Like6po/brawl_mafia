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
    if chat_obj:
        player = chat_obj.get_player(cbq.from_user.id)

        if player and Kill() not in player.effects:

            if chat_obj.phase == 'voting1':
                if Mute() not in player.effects:

                    vote_to_player = chat_obj.get_player(vote_to_id)
                    if vote_to_player and Kill() not in vote_to_player.effects:

                        if vote_to_player.id != player.id:

                            if action in ['like', 'dislike']:
                                if player in chat_obj.accept_votes_dislike:
                                    chat_obj.accept_votes_dislike.remove(player)
                                if player in chat_obj.accept_votes_like:
                                    chat_obj.accept_votes_like.remove(player)
                                if action == 'like':
                                    chat_obj.accept_votes_like.append(player)

                                    print(f'[{chat_obj.id}] Лайк от [ID {player.id}, {player.name}, {player.role}]')
                                elif action == 'dislike':

                                    chat_obj.accept_votes_dislike.append(player)
                                    print(f'[{chat_obj.id}] Дизлайк от [ID {player.id}, {player.name}, {player.role}]')
                                chat_obj.is_new_vote = True

                                if (len(set(chat_obj.accept_votes_like)) + len(set(
                                        chat_obj.accept_votes_dislike)) - 1) >= chat_obj.get_alive_players_count():
                                    chat_obj.is_accept_end = True

                                return await cbq.answer('Выбор сделан!')
                            await cbq.answer()
                        else:
                            return await cbq.answer('Нельзя голосовать против себя!')

                    else:
                        return await cbq.answer('Такого Бравлера нет!')

                else:
                    return await cbq.answer('Вы отдыхаете после Пайпер!')

            else:
                return await cbq.answer('Это доступно только во время голосования!')

        else:
            return await cbq.answer('Вы не участвуете в данной игре!')

    else:
        return await cbq.answer('Игры не существует!')


@dp.callback_query_handler(day_vote_callback.filter(), ChatTypeFilter(types.ChatType.PRIVATE))
async def day_vote(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    vote_to_id = int(callback_data.get('player_id'))
    chat_obj = Game.get_chat(chat_id)
    if chat_obj:
        player = chat_obj.get_player(cbq.from_user.id)

        if player and Kill() not in player.effects:
            if Mute() not in player.effects:
                if chat_obj.phase == 'voting':

                    vote_to_player = chat_obj.get_player(vote_to_id)
                    if vote_to_player and Kill() not in vote_to_player.effects:

                        if player.day_voting_to:
                            return await cbq.answer('Вы уже проголосовали!')
                        player.day_voting_to = vote_to_id
                        chat_obj.day_votes_ids.append(vote_to_id)
                        print(
                            f'[{chat_obj.id}] Игрок [ID {player.id}, {player.name}, {player.role}] '
                            f'проголосовал за [ID {vote_to_player.id}, {vote_to_player.name}, {vote_to_player.role}]')
                        await cbq.message.edit_text('Выбор сделан')
                        if chat_obj.is_show_day_votes:
                            return await dp.bot.send_message(chat_obj.id, f"{hlink(player.name, f'tg://user?id={player.id}')} "
                                                                          f"проголосовал за изгнание"
                                                                          f" {hlink(vote_to_player.name, f'tg://user?id={vote_to_player.id}')}!")

                        else:
                            return await dp.bot.send_message(chat_obj.id, f"{hlink(player.name, f'tg://user?id={player.id}')} "
                                                                          f"проголосовал!")

                    else:
                        return await cbq.answer('Ошибка! Такого Бравлера нет!')

                else:
                    return await cbq.answer('Это доступно только во время голосования!')

            else:
                return await cbq.answer('Вы отдыхаете после Пайпер!')

        else:
            return await cbq.answer('Вы не участвуете в данной игре!')

    else:
        return await cbq.answer('Игры не существует!')


@dp.callback_query_handler(night_cop_callback.filter(), ChatTypeFilter(types.ChatType.PRIVATE))
async def night_cop(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    chat_obj = Game.get_chat(chat_id)
    if chat_obj:
        player = chat_obj.get_player(cbq.from_user.id)

        if player and Kill() not in player.effects:
            if Mute() not in player.effects:
                if chat_obj.phase == 'night':
                    if player.role == 'cop':
                        chat_obj.cop.kill_to = None
                        chat_obj.cop.check_to = None
                        if callback_data.get('action') == 'check':
                            print(f"Коп {player.name} выбрал проверку!")
                            await cbq.message.edit_text(text='Кого вы хотите проверить?',
                                                        reply_markup=cb_q_cop_check_kb(chat_obj.id,
                                                                                       chat_obj.players))

                        elif callback_data.get('action') == 'kill':
                            print(f"Коп {player.name} выбрал убийство")
                            await cbq.message.edit_text(text='Кого вы хотите изгнать?',
                                                        reply_markup=cb_q_cop_kill_kb(chat_obj.id,
                                                                                      chat_obj.players))
                else:
                    return await cbq.answer('Это доступно только ночью!')

            else:
                return await cbq.answer('Вы отдыхаете после Пайпер!')
        else:
            return await cbq.answer('Вы не участвуете в данной игре!')

    else:
        return await cbq.answer('Игры не существует!')


@dp.callback_query_handler(night_vote_mafia_callback.filter(), ChatTypeFilter(types.ChatType.PRIVATE))
async def night_vote_mafia(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    vote_to_id = int(callback_data.get('player_id'))
    chat_obj = Game.get_chat(chat_id)
    if chat_obj:
        player = chat_obj.get_player(cbq.from_user.id)

        if player and Kill() not in player.effects:
            if Mute() not in player.effects:
                if chat_obj.phase == 'night':

                    vote_to_player = chat_obj.get_player(vote_to_id)
                    if vote_to_player:

                        if player.role in ['mafia', 'don']:
                            if player.go_to:
                                return await cbq.answer('Вы уже проголосовали!')
                            if vote_to_id == player.id:
                                return await cbq.answer('Нельзя выбрать себя!')
                            player.go_to = vote_to_id
                            chat_obj.mafia_votes_ids.append(vote_to_id)
                            print(f"Мафия {player.name} проголосовала за {vote_to_player.name}.")

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

                    else:
                        return await cbq.answer('Ошибка! Такого Бравлера нет!')

                else:
                    return await cbq.answer('Это доступно только ночью!')

            else:
                return await cbq.answer('Вы отдыхаете после Пайпер!')
        else:
            return await cbq.answer('Вы не участвуете в данной игре!')

    else:
        return await cbq.answer('Игры не существует!')


@dp.callback_query_handler(night_vote_cop_callback.filter(), ChatTypeFilter(types.ChatType.PRIVATE))
async def night_vote_cop(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    vote_to_id = int(callback_data.get('player_id'))
    action = callback_data.get('action')
    chat_obj = Game.get_chat(chat_id)
    if chat_obj:
        player = chat_obj.get_player(cbq.from_user.id)

        if player and Kill() not in player.effects:
            if Mute() not in player.effects:
                if chat_obj.phase == 'night':

                    vote_to_player = chat_obj.get_player(vote_to_id)
                    if vote_to_player:

                        if player.role == 'cop':
                            if action == 'check':

                                if vote_to_id != player.id:
                                    if player.check_to is None:
                                        player.check_to = vote_to_id
                                        print(f"Коп {player.name} чекнул {vote_to_player.name}.")
                                        await cbq.message.edit_text(text='Выбор сделан!')
                                        await dp.bot.send_message(chat_obj.id,
                                                                  'Кольт пошел на поиски банды Булла...')
                                else:
                                    return await cbq.answer('Нельзя выбрать себя!')

                            elif action == 'kill':

                                if vote_to_id != player.id:
                                    if player.kill_to is None:
                                        player.kill_to = vote_to_id
                                        print(f"Коп {player.name} убил {vote_to_player.name}.")
                                        await cbq.message.edit_text(text='Выбор сделан!')
                                        await dp.bot.send_message(chat_obj.id,
                                                                  'Кольт изгоняет кого-то из Бравл Сити...')

                                else:
                                    return await cbq.answer('Нельзя выбрать себя!')

                    else:
                        return await cbq.answer('Ошибка! Такого Бравлера нет!')

                else:
                    return await cbq.answer('Это доступно только ночью!')

            else:
                return await cbq.answer('Вы отдыхаете после Пайпер!')
        else:
            return await cbq.answer('Вы не участвуете в данной игре!')

    else:
        return await cbq.answer('Игры не существует!')


@dp.callback_query_handler(night_vote_callback.filter(), ChatTypeFilter(types.ChatType.PRIVATE))
async def night_vote(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    vote_to_id = int(callback_data.get('player_id'))
    chat_obj = Game.get_chat(chat_id)
    if chat_obj:
        player = chat_obj.get_player(cbq.from_user.id)

        if player and Kill() not in player.effects:
            if Mute() not in player.effects:
                if chat_obj.phase == 'night':

                    vote_to_player = chat_obj.get_player(vote_to_id)
                    if vote_to_player:

                        if player.role == 'doctor':
                            if vote_to_id == player.id:
                                if Heal_self() in player.effects:
                                    print(f"Доктор {player.name} прогосовал за самоотхил.")
                                    return await cbq.answer(text='Нельзя спасти себя дважды!')

                            player.go_to = vote_to_id
                            print(f"Доктор {player.name} прогосовал за хил {vote_to_player.name}.")
                            await cbq.message.edit_text(text='Выбор сделан!')
                            await dp.bot.send_message(chat_obj.id,
                                                      'Пэм отправилась к нуждающимся в помощи')

                        elif player.role == 'don':
                            if vote_to_id == player.id:
                                return await cbq.answer('Нельзя проверить себя!')

                            elif vote_to_player.role == 'mafia':
                                return await cbq.answer('Нельзя проверять свою банду!')

                            player.check_to = vote_to_id
                            print(f"Дон {player.name} чекнул {vote_to_player.name}.")
                            await cbq.message.edit_text('Выбор сделан!')
                            await dp.bot.send_message(chat_obj.id,
                                                      'Булл отправился в кусты, чтобы проследить за кое-кем...')

                        elif player.role == 'whore':
                            if vote_to_id == player.id:
                                return await cbq.answer('Нельзя выбрать себя!')

                            player.go_to = vote_to_id
                            print(f"Любовница {player.name} пришла к {vote_to_player.name}.")
                            await cbq.message.edit_text('Выбор сделан!')
                            await dp.bot.send_message(chat_obj.id,
                                                      'Пайпер устроила кому-то классную ночь!')

                        elif player.role == 'homeless':
                            if vote_to_id == player.id:
                                return await cbq.answer('Нельзя выбрать себя!')

                            player.go_to = vote_to_id
                            print(f"Божм {player.name} пошел к {vote_to_player.name}.")
                            await cbq.message.edit_text('Выбор сделан!')
                            await dp.bot.send_message(chat_obj.id,
                                                      'Барли пошел искать пиво для своего бара...')

                    else:
                        return await cbq.answer('Ошибка! Такого Бравлера нет!')

                else:
                    return await cbq.answer('Это доступно только ночью!')

            else:
                return await cbq.answer('Вы отдыхаете после Пайпер!')

        else:
            return await cbq.answer('Вы не участвуете в данной игре!')

    else:
        return await cbq.answer('Игры не существует!')
