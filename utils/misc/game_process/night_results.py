from aiogram.utils.markdown import hlink, hbold

from data.game_models import Kill, Conv
from loader import bot, db, Game
from utils.misc.game_process.service_defs import msg_night_res_show_homeless_results, msg_day_time_dead_from_mafia, \
    msg_day_time_dead_from_cop, msg_day_time_dead_from_afk
from utils.misc.mailing_process import roles_dict_brawl


async def cop_result(result, chat_obj):
    if result:
        print(result)
        if result[0] == 'cop_check':
            player_obj = chat_obj.get_player(int(result[1]))
            user = await db.get_player(player_obj.id)

            if player_obj.role in ['don', 'mafia'] and \
                    user.documents > 0 and chat_obj.is_active_boosts == 1:
                await db.upd_player(player_obj.id, documents=-1)

                await bot.send_message(chat_obj.cop.id,
                                       f"{hlink(player_obj.name, f'tg://user?id={player_obj.id}')} -"
                                       f" {roles_dict_brawl['peace']}!"
                                       )
                print(f'[{chat_obj.id}] Коп проверил [ ID {player_obj.id}, {player_obj.name},'
                      f' {player_obj.role} ], но был обманут!')
            else:
                await bot.send_message(chat_obj.cop.id,
                                       f"{hlink(player_obj.name, f'tg://user?id={player_obj.id}')}"
                                       f" - {roles_dict_brawl[player_obj.role]}!"
                                       )
                print(f'[{chat_obj.id}] Коп проверил [ ID {player_obj.id}, {player_obj.name}, {player_obj.role} ]')

            await bot.send_message(player_obj.id, 'Кто-то заинтересовался какой ты бравлер...')

        elif result[0] == 'cop_kill':

            player_obj = chat_obj.get_player(int(result[1]))
            await bot.send_message(player_obj.id,
                                   f'{hbold("☠ Вас изгнали! Напишите сюда ваше предсмертное сообщение!")}')
            print(f'[{chat_obj.id}] Коп убивает [ ID {player_obj.id}, {player_obj.name}, {player_obj.role} ]')


async def don_result(result, chat_obj):
    if result:
        print(result)
        if result[0] == 'don_check':
            player_obj = chat_obj.get_player(int(result[1]))
            if player_obj.role == 'cop':
                await bot.send_message(chat_obj.don.id,
                                       f"{hlink(player_obj.name, f'tg://user?id={player_obj.id}')} - Кольт!")
            else:
                await bot.send_message(chat_obj.don.id,
                                       f"{hlink(player_obj.name, f'tg://user?id={player_obj.id}')} - Не Кольт!")
            await bot.send_message(player_obj.id, 'Кто-то заинтересовался какой ты бравлер...')
            print(f'[{chat_obj.id}] Дон проверил [ ID {player_obj.id}, {player_obj.name}, {player_obj.role} ]')


async def mafia_result(result, chat_obj):
    if result:
        print(result)
        if result[0] == 'mafia_kill':
            player_obj = chat_obj.get_player(int(result[1]))
            await bot.send_message(player_obj.id,
                                   f'{hbold("☠ Вас изгнали! Напишите сюда ваше предсмертное сообщение!")}')
            print(f'[{chat_obj.id}] Мафия убивает [ ID {player_obj.id}, {player_obj.name}, {player_obj.role} ]')


async def whore_result(result, chat_obj):
    if result:
        print(result)
        if result[0] == 'whore_go_to':
            player_obj = chat_obj.get_player(int(result[1]))
            await bot.send_message(player_obj.id, 'Пайпер пришла к тебе! С ней ты забудешь обо всём...')
            print(
                f'[{chat_obj.id}] Любовница приходит к [ ID {player_obj.id}, {player_obj.name}, {player_obj.role} ]')


async def homeless_result(result, chat_obj):
    if result:
        print(result)
        if result[0] == 'homeless_go_to':
            player_obj = chat_obj.get_player(int(result[1]))
            await bot.send_message(player_obj.id,
                                   'Барли спросил у вас бутылку пива для своего бара этой ночью.')
            for effect in player_obj.effects:
                if effect == Kill():
                    if effect.killer == 'mafia':
                        await bot.send_message(chat_obj.homeless.id,
                                               msg_night_res_show_homeless_results(player_obj, chat_obj.don))
                    elif effect.killer == 'cop':
                        await bot.send_message(chat_obj.homeless.id,
                                               msg_night_res_show_homeless_results(player_obj, chat_obj.cop))

            else:
                await bot.send_message(chat_obj.homeless.id,
                                       'Вы спокойно спросили бутылку пива и ушли работать в бар дальше.')

            print(f'[{chat_obj.id}] Бомж приходит к [ ID {player_obj.id}, {player_obj.name}, {player_obj.role} ]')


async def doctor_result(result, chat_obj):
    if result:
        print(result)
        player_obj = chat_obj.get_player(int(result[1]))
        if result[0] == 'doctor_heal':
            if player_obj.id == chat_obj.doctor.id:
                await bot.send_message(player_obj.id, 'Вы спасли себя от изгнания! Вот это удача!')
            else:
                await bot.send_message(player_obj.id, 'Пэм спасла вас от изгнания!')
            print(f'[{chat_obj.id}] Доктор лечит [ ID {player_obj.id}, {player_obj.name}, {player_obj.role} ]')
        elif result[0] == 'doctor_not_heal':
            if player_obj.id == chat_obj.doctor.id:
                await bot.send_message(player_obj.id, 'Вы зря беспокоились! Вас не тронули этой ночью!')
            else:
                await bot.send_message(player_obj.id, 'Пэм заходила к вам этой ночью.')
            print(
                f'[{chat_obj.id}] Доктор зря пришел к [ ID {player_obj.id}, {player_obj.name}, {player_obj.role} ]')


async def night_results(chat_obj):
    print(f'[{chat_obj.id}] Ночные результаты! ')
    print(chat_obj)
    result_cop_list = chat_obj.cop_results_night()
    result_don_list = chat_obj.don_results_night()
    result_mafia_list = chat_obj.mafia_results_night()
    result_whore_list = chat_obj.whore_results_night()
    result_homeless_list = chat_obj.homeless_results_night()
    result_doctor_list = chat_obj.doctor_results_night()
    print(chat_obj)
    await cop_result(result_cop_list, chat_obj)
    await don_result(result_don_list, chat_obj)
    await mafia_result(result_mafia_list, chat_obj)
    await whore_result(result_whore_list, chat_obj)
    await homeless_result(result_homeless_list, chat_obj)
    await doctor_result(result_doctor_list, chat_obj)
    print(chat_obj)
    chat_id: Conv = chat_obj.id
    if Game.get_chat(chat_id):
        players = chat_obj.players
        check = False
        for player_dead in players:
            for effect in player_dead.effects:
                if effect == Kill():
                    # chat_obj.kill(player_dead)
                    if effect.killer == 'mafia':
                        await bot.send_message(chat_id,
                                               msg_day_time_dead_from_mafia(player_dead,
                                                                            chat_obj.is_show_dead_roles))
                        check = True

                    if effect.killer == 'cop':
                        await bot.send_message(chat_id,
                                               msg_day_time_dead_from_cop(player_dead,
                                                                          chat_obj.is_show_dead_roles))
                        check = True

                    if effect.killer == 'afk':
                        await bot.send_message(chat_id, msg_day_time_dead_from_afk(player_dead,
                                                                                   chat_obj.is_show_dead_roles))
                    break

        if not check:
            await bot.send_message(chat_id, 'Удивительно, но в эту ночь никого не изгнали из Бравл Сити!')