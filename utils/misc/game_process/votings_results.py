from loader import bot
from utils.misc.game_process.voting_accept import voting_accept


async def voting_results(chat_id, chat_obj):
    print(f'[{chat_obj.id}] Результаты голосования!')
    votes = chat_obj.day_votes_ids
    maximum = 0
    result = 0
    for element in votes:
        if votes.count(element) > maximum:
            maximum = votes.count(element)
            result = element

    for element in votes:
        if (votes.count(element) == maximum and result != element) or votes == []:
            print(f'[{chat_obj.id}] Жители разошлись во мнении!')

            return await bot.send_message(chat_id, 'Бравлеры не пришли к общему решению и никого не изгнали.')

    else:
        if result == 0:
            print(f'[{chat_obj.id}] Жители разошлись во мнении!')

            return await bot.send_message(chat_id, 'Бравлеры не пришли к общему решению и никого не изгнали.')

        else:
            player_obj = chat_obj.get_player(result)
            if player_obj:
                print(
                    f'[{chat_obj.id}] Жители решают, вешать ли [ ID {player_obj.id}, {player_obj.name}, {player_obj.role}]!')
                return await voting_accept(chat_id, chat_obj, player_obj)

