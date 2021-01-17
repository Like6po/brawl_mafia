from aiogram import types
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.utils.markdown import hbold, hlink

from data.game_models import Kill
from keyboards.inline.other import only_in_conv
from loader import dp, Game
from utils.misc.game_process.service_defs import try_send


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=['leave', 'settings', 'extend', 'play', 'close'])
async def not_available_commands(message: types.Message):
    await message.answer('⚠️ Данное действие доступно только в беседах!',
                         reply_markup=only_in_conv())


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE))
async def not_available_commands(message: types.Message):
    result = Game.search_player(message.from_user.id)

    if result:
        # получаем объекты беседы и игрока, если он играет
        chat_obj = result[0]
        player_obj = result[1]

        # если ночь
        if chat_obj.phase == 'night':
            # если роль игрока - дон
            if player_obj.role == 'don':
                # если есть мафия
                if chat_obj.mafia:
                    # для каждой мафии
                    for mafia in chat_obj.mafia:
                        # отправляем сообщение дона всем мафиози
                        if len(message.text) > 1000:
                            message.text = message.text[:1000] + " ....."
                        return await try_send(player_obj=mafia,
                                              text=f"{hlink(player_obj.name, f'tg://user?id={player_obj.id}')}: "
                                                   f"{hbold(message.text)}",
                                              chat_obj=chat_obj)

            # если роль игрока - мафия
            elif player_obj.role == 'mafia':
                # если есть дон
                if chat_obj.don:
                    if len(message.text) > 1000:
                        message.text = message.text[:1000] + " ....."
                    await try_send(player_obj=chat_obj.don,
                                   text=f"{hlink(player_obj.name, f'tg://user?id={player_obj.id}')}: "
                                        f"{hbold(message.text)}",
                                   chat_obj=chat_obj)

                # для каждой мафии
                for mafia in chat_obj.mafia:
                    # всем кроме отправителя
                    if mafia.id != player_obj.id:
                        if len(message.text) > 1000:
                            message.text = message.text[:1000] + " ....."
                        # отправляем сообщения мафии всем мафиози
                        await try_send(player_obj=mafia,
                                       text=f"{hlink(player_obj.name, f'tg://user?id={player_obj.id}')}: "
                                            f"{hbold(message.text)}",
                                       chat_obj=chat_obj)

        # если не ночь
        elif chat_obj.phase in ['day', 'voting', 'voting1']:
            # если предсмертный крик есть у юзера

            if Kill() in player_obj.effects:
                # он добивается
                try:
                    chat_obj.kill(player_obj)
                except Exception as e:
                    print(e)
                # кричит что то всем
                if len(message.text) > 1000:
                    message.text = message.text[:1000] + " ....."
                await dp.bot.send_message(chat_obj.id,
                                          f"☠️ Кто-то слышал, как 🙎‍♂️ Бравлер"
                                          f" {hlink(player_obj.name, f'tg://user?id={player_obj.id}')}"
                                          f" кричал перед поражением:\n{hbold(message.text)}")
                await message.answer('☠ Передал ваше предсмертное сообщение жителям!')
