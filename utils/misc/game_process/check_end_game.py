import random

from aiogram.utils.markdown import hlink

from data.game_models import Kill, Dead_day, Don
from loader import Game, db, bot
from utils.misc.mailing_process import roles_dict_brawl


async def check_end_game(chat_id, chat_obj):
    mafia = 0
    piece = 0
    for player in chat_obj.players:
        if Kill() not in player.effects:
            if player.role in ['don', 'mafia']:
                mafia += 1
            else:
                piece += 1

    print(f"mafia = {mafia}, piece = {piece}")
    text_results_win = 'Победители:'
    text_results_lose = 'Проигравшие:'

    if mafia >= piece:
        for player in chat_obj.players:
            if player.role in ['mafia', 'don']:
                if Kill() not in player.effects:
                    text_results_win += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                        f" - {roles_dict_brawl[player.role]}"
                    await db.upd_player(player.id, wins=1, money=20)
                else:
                    text_results_lose += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                         f" - {roles_dict_brawl[player.role]}"
                    await db.upd_player(player.id, loses=1)
            else:
                text_results_lose += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                     f" - {roles_dict_brawl[player.role]}"
                await db.upd_player(player.id, loses=1)

        for player in chat_obj.dead_players:
            if player.role == 'suicide':
                if Dead_day() in player.effects:
                    text_results_win += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                        f" - {roles_dict_brawl[player.role]}"
                    await db.upd_player(player.id, wins=1, money=20)
                else:
                    text_results_lose += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                         f" - {roles_dict_brawl[player.role]}"
                    await db.upd_player(player.id, loses=1)
            else:
                text_results_lose += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                     f" - {roles_dict_brawl[player.role]}"
                await db.upd_player(player.id, loses=1)

        Game.remove_chat(chat_obj)
        await bot.send_message(chat_id,
                               f'🔫👿 Банда Булла победила!\n{text_results_win}\n\n{text_results_lose}')
        return True

    elif chat_obj.day > 20:

        for player in chat_obj.players:
            if player.role in ['suicide', 'don', 'mafia']:
                text_results_lose += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                     f" - {roles_dict_brawl[player.role]}"
            else:
                text_results_win += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                    f" - {roles_dict_brawl[player.role]}"
        for player in chat_obj.dead_players:
            if player.role == 'suicide' and Dead_day() in player.effects:
                text_results_win += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                    f" - {roles_dict_brawl[player.role]}"
            else:
                text_results_lose += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                     f" - {roles_dict_brawl[player.role]}"
        Game.remove_chat(chat_obj)
        await bot.send_message(chat_id,
                               f'👨‍🦰 Мирные Бравлеры победили!\n{text_results_win}\n\n{text_results_lose}')
        return True

    elif mafia == 0:

        for player in chat_obj.players:
            if player.role == 'suicide':
                text_results_lose += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                     f" - {roles_dict_brawl[player.role]}"
            else:
                if Kill() not in player.effects:
                    text_results_win += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                        f" - {roles_dict_brawl[player.role]}"
                else:
                    text_results_lose += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                         f" - {roles_dict_brawl[player.role]}"
        for player in chat_obj.dead_players:
            if player.role == 'suicide' and Dead_day() in player.effects:
                text_results_win += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                    f" - {roles_dict_brawl[player.role]}"
            else:
                text_results_lose += f"\n{hlink(player.name, f'tg://user?id={player.id}')}" \
                                     f" - {roles_dict_brawl[player.role]}"
        Game.remove_chat(chat_obj)
        await bot.send_message(chat_id,
                               f'👨‍🦰 Мирные Бравлеры победили!\n{text_results_win}\n\n{text_results_lose}')
        return True

    if not chat_obj.don:
        if chat_obj.mafia:
            player_obj = random.choice(chat_obj.mafia)
            chat_obj.mafia.remove(player_obj)
            chat_obj.players.remove(player_obj)
            chat_obj.don = Don(player_obj)
            chat_obj.players.append(chat_obj.don)

