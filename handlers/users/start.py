import re

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, ChatTypeFilter
from data.game_models import Player
from keyboards.inline.callback_datas import start_callback
from keyboards.inline.help import help_kb
from keyboards.inline.start import start_kb
from loader import dp, Game, db


@dp.message_handler(CommandStart(deep_link=re.compile(r"-[\d]+")), ChatTypeFilter(types.ChatType.PRIVATE))
async def start_deep(message: types.Message):
    user = await db.get_player(message.from_user.id)
    result = Game.search_player(message.from_user.id)
    deep = message.get_args()
    if not result:
        chat_obj = Game.get_chat(int(deep.split(' ')[0]))
        if not chat_obj:
            return await message.answer('❌ Вы не можете присоединиться к несуществующей игре!')
        else:
            if chat_obj.phase is not 'starting':
                await message.answer('❌ Игра уже началась!')
            else:
                if chat_obj.get_registered_player(message.from_user.id):
                    return await message.answer('⚠️ Вы уже присоединились!')
                if len(chat_obj.registered) > 11:
                    return await message.answer('👥 Невозможно присоединиться, максимальное количество игроков!')

                if user.active_roles > 0 and chat_obj.is_active_boosts:
                    await db.upd_user(message.from_user.id, active_role=-1)
                    chat_obj.register_player(Player(message.from_user.id,
                                                    user_name=message.from_user.full_name,
                                                    active_role=1))
                else:
                    chat_obj.register_player(Player(message.from_user.id,
                                                    user_name=message.from_user.full_name))
                # передаем флаг, что нужно обновить сообщение регистрации
                chat_obj.is_new_player_join = True
                # отвечаем, что игрок зарегистрирован
                await message.answer('✅ Вы успешно присоединились к игре!')
                # если игроков 12 или больше
                if len(chat_obj.registered) >= 12:
                    # досрочно завершаем регистрацию
                    chat_obj.register_is_end_ahead_of_time = True
    else:
        await message.answer('❌ Вы не можете играть более чем в 1 группе одновременно!')


@dp.message_handler(CommandStart(), ChatTypeFilter(types.ChatType.PRIVATE))
async def start(message: types.Message):
    await message.answer('Привет🤘! Я бот-ведущий игры мафия🤵🏻 с элементами Brawl Stars! '
                         'Для начала работы меня необходимо добавить в беседу и выдать права администратора🤖!\n',
                         reply_markup=start_kb())


@dp.callback_query_handler(start_callback.filter(type='help'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text('ℹ️ Здесь вы можете получить информацию с помощью кнопок!',
                                reply_markup=help_kb())
