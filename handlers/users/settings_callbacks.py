
from aiogram import types

from keyboards.inline.callback_datas import settings_callback, settings_mute_dead_callback, \
    settings_mute_no_players_callback, settings_reg_time_callback, settings_night_time_callback, \
    settings_day_time_callback, settings_voting_time_callback, settings_accept_time_callback, settings_pin_callback, \
    settings_boosts_callback, settings_show_roles_callback, settings_show_votes_callback

from keyboards.inline.settings import settings_kb_mute, settings_kb_show_to_admin, settings_kb_mute_dead, \
    settings_kb_mute_no_players, settings_kb_timings, settings_kb_reg_time, settings_kb_some, settings_kb_nighttime, \
    settings_kb_daytime, settings_kb_voting_time, settings_kb_accept_time, settings_kb_pin, settings_kb_boosts, \
    settings_kb_show_roles, settings_kb_show_votes
from loader import dp, db


@dp.callback_query_handler(settings_callback.filter())
async def settings_cbq(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = callback_data.get('action')

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action == 'exit':
        await cbq.message.edit_text('Настройки сохранены!')
    elif action == 'menu':
        await cbq.message.edit_text("Какие параметры беседы вы хотите поменять?",
                                    reply_markup=settings_kb_show_to_admin(chat_id))
    elif action == 'mute':
        await cbq.message.edit_text('Здесь вы можете настроить, чьи сообщения я буду удалять во время игры.',
                                    reply_markup=settings_kb_mute(chat_id))
    elif action == 'mute_dead':
        await cbq.message.edit_text('Удалять сообщения тех, кого изгнали?',
                                    reply_markup=settings_kb_mute_dead(chat_id))

    elif action == 'mute_not_players':
        await cbq.message.edit_text('Удалять сообщения тех пользователей, которые не играют?',
                                    reply_markup=settings_kb_mute_no_players(chat_id))

    elif action == 'timings':
        await cbq.message.edit_text('Здесь можно настроить тайминги фаз.',
                                    reply_markup=settings_kb_timings(chat_id))

    elif action == 'reg_time':
        await cbq.message.edit_text('Время отводимое на регистрацию пользователей (в секундах).\n'
                                    'Команда /extend продливает время регистрации на время в 2 раза меньшее,'
                                    ' чем общее время регистрации.',
                                    reply_markup=settings_kb_reg_time(chat_id))

    elif action == 'night_time':
        await cbq.message.edit_text('Время отводимое на ночь (в секундах).',
                                    reply_markup=settings_kb_nighttime(chat_id))

    elif action == 'day_time':
        await cbq.message.edit_text('Время отводимое на дневное обсуждение (в секундах).',
                                    reply_markup=settings_kb_daytime(chat_id))

    elif action == 'voting_time':
        await cbq.message.edit_text('Время отводимое на дневное голосование (в секундах).',
                                    reply_markup=settings_kb_voting_time(chat_id))

    elif action == 'accept_time':
        await cbq.message.edit_text('Время отводимое на подтверждение результатов голосования (в секундах).',
                                    reply_markup=settings_kb_accept_time(chat_id))

    elif action == 'some':
        await cbq.message.edit_text('Остальные параметры:',
                                    reply_markup=settings_kb_some(chat_id))

    elif action == 'pin':
        await cbq.message.edit_text('Закреплять ли сообщение с регистрацией?',
                                    reply_markup=settings_kb_pin(chat_id))

    elif action == 'boosts':
        await cbq.message.edit_text('Включить бусты (поддельные документы и активные роли)?',
                                    reply_markup=settings_kb_boosts(chat_id))

    elif action == 'show_roles':
        await cbq.message.edit_text('Показывать роли игроков, которые выбыли из игры?',
                                    reply_markup=settings_kb_show_roles(chat_id))

    elif action == 'show_votes':
        await cbq.message.edit_text('Показывать кто за кого голосует на дневном голосовании?',
                                    reply_markup=settings_kb_show_votes(chat_id))
    else:
        await cbq.answer('Сообщите администратору об ошибке N143...')


@dp.callback_query_handler(settings_mute_dead_callback.filter())
async def stg_mute_dead(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = callback_data.get('action')

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in ['yes', 'no']:
        if action == 'yes':
            await db.set_chat(chat_id, is_dead_talk=0)
        elif action == 'no':
            await db.set_chat(chat_id, is_dead_talk=1)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Здесь вы можете настроить, чьи сообщения я буду удалять во время игры.',
                                    reply_markup=settings_kb_mute(chat_id))
    else:
        await cbq.answer('Ошибка stg_mute_dead')


@dp.callback_query_handler(settings_mute_no_players_callback.filter())
async def stg_mute_no_players(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = callback_data.get('action')

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in ['yes', 'no']:
        if action == 'yes':
            await db.set_chat(chat_id, is_nonplayers_talk=0)
        elif action == 'no':
            await db.set_chat(chat_id, is_nonplayers_talk=1)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Здесь вы можете настроить, чьи сообщения я буду удалять во время игры.',
                                    reply_markup=settings_kb_mute(chat_id))
    else:
        await cbq.answer('Ошибка stg_mute_no_players')


@dp.callback_query_handler(settings_reg_time_callback.filter())
async def stg_reg_time(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = int(callback_data.get('action'))

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in [30, 45, 60, 80, 120, 240]:
        await db.set_chat(chat_id, register_time=action)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Здесь можно настроить тайминги фаз.',
                                    reply_markup=settings_kb_timings(chat_id))
    else:
        await cbq.answer('Ошибка stg_reg_time')


@dp.callback_query_handler(settings_night_time_callback.filter())
async def stg_night_time(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = int(callback_data.get('action'))

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in [30, 45, 60, 80, 120, 240]:
        await db.set_chat(chat_id, night_time=action)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Здесь можно настроить тайминги фаз.',
                                    reply_markup=settings_kb_timings(chat_id))
    else:
        await cbq.answer('Ошибка stg_night_time')


@dp.callback_query_handler(settings_day_time_callback.filter())
async def stg_day_time(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = int(callback_data.get('action'))

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in [30, 45, 60, 80, 120, 240]:
        await db.set_chat(chat_id, day_time=action)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Здесь можно настроить тайминги фаз.',
                                    reply_markup=settings_kb_timings(chat_id))
    else:
        await cbq.answer('Ошибка stg_day_time')


@dp.callback_query_handler(settings_voting_time_callback.filter())
async def stg_voting_time(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = int(callback_data.get('action'))

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in [30, 45, 60, 80, 120, 240]:
        await db.set_chat(chat_id, vote_time=action)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Здесь можно настроить тайминги фаз.',
                                    reply_markup=settings_kb_timings(chat_id))
    else:
        await cbq.answer('Ошибка stg_voting_time')


@dp.callback_query_handler(settings_accept_time_callback.filter())
async def stg_accept_time(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = int(callback_data.get('action'))

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in [30, 45, 60, 80, 120, 240]:
        await db.set_chat(chat_id, accept_time=action)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Здесь можно настроить тайминги фаз.',
                                    reply_markup=settings_kb_timings(chat_id))
    else:
        await cbq.answer('Ошибка stg_accept_time')


@dp.callback_query_handler(settings_pin_callback.filter())
async def stg_pin(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = callback_data.get('action')

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in ['yes', 'no']:
        if action == 'yes':
            await db.set_chat(chat_id, is_pin_register=1)
        elif action == 'no':
            await db.set_chat(chat_id, is_pin_register=0)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Остальные параметры:',
                                    reply_markup=settings_kb_some(chat_id))
    else:
        await cbq.answer('Ошибка stg_pin')


@dp.callback_query_handler(settings_boosts_callback.filter())
async def stg_boosts(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = callback_data.get('action')

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in ['yes', 'no']:
        if action == 'yes':
            await db.set_chat(chat_id, is_active_boosts=1)
        elif action == 'no':
            await db.set_chat(chat_id, is_active_boosts=0)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Остальные параметры:',
                                    reply_markup=settings_kb_some(chat_id))
    else:
        await cbq.answer('Ошибка stg_boosts')


@dp.callback_query_handler(settings_show_roles_callback.filter())
async def stg_show_roles(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = callback_data.get('action')

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in ['yes', 'no']:
        if action == 'yes':
            await db.set_chat(chat_id, is_show_dead_roles=1)
        elif action == 'no':
            await db.set_chat(chat_id, is_show_dead_roles=0)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Остальные параметры:',
                                    reply_markup=settings_kb_some(chat_id))
    else:
        await cbq.answer('Ошибка stg_show_roles')


@dp.callback_query_handler(settings_show_votes_callback.filter())
async def stg_show_votes(cbq: types.CallbackQuery, callback_data: dict):
    chat_id = int(callback_data.get('chat_id'))
    action = callback_data.get('action')

    if cbq.from_user not in [member.user for member in await dp.bot.get_chat_administrators(chat_id)]:
        await cbq.answer('Вы уже не являетесь администратором чата!')
        return await cbq.message.delete()

    if action in ['yes', 'no']:
        if action == 'yes':
            await db.set_chat(chat_id, is_show_day_votes=1)
        elif action == 'no':
            await db.set_chat(chat_id, is_show_day_votes=0)
        await cbq.answer('Успешно!')
        await cbq.message.edit_text('Остальные параметры:',
                                    reply_markup=settings_kb_some(chat_id))
    else:
        await cbq.answer('Ошибка stg_show_votes')
