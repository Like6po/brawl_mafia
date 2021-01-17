import asyncio

from aiogram import types
from aiogram.utils.exceptions import RetryAfter, Unauthorized
from aiogram.utils.markdown import hlink

from data.game_models import Kill
from keyboards.inline.game_process import kb_night_cop, kb_night_don, kb_night_doctor, kb_night_whore, \
    kb_night_homeless, kb_night_mafia, kb_voting_time_users, game_go_to_bot_kb

roles_dict_brawl = {'peace': '🙎‍♀️ Шелли',
                    'mafia': '🦅 Ворон',
                    'cop': '🔫🕵️ Кольт',
                    'doctor': '🚑👩🏼‍⚕️ Пэм',
                    'homeless': '🍾 Барли',
                    'whore': '☂️💃 Пайпер',
                    'don': '🐃 Булл',
                    'suicide': '💣 Тик'}


def game_msg_text_role(role: str, mafia_list: list, don) -> str:
    if role not in ['mafia', 'don']:
        return f'📢 Вы - {roles_dict_brawl[role]}'
    else:
        text_team = ''
        if don:
            text_team += f'{hlink(don.name, f"tg://user?id={don.id}")} - {roles_dict_brawl[don.role]}'
        if mafia_list:
            for player in mafia_list:
                text_team += f'\n{hlink(player.name, f"tg://user?id={player.id}")} - {roles_dict_brawl[player.role]}'

        return f'📢 Вы - {roles_dict_brawl[role]}\nБанда Булла:\n{text_team}'


async def mailing_roles_to_players(chat_obj, bot):
    for player in chat_obj.players:
        try:
            await bot.send_message(player.id,
                                   game_msg_text_role(player.role,
                                                      chat_obj.mafia,
                                                      chat_obj.don))

        except RetryAfter as e:
            await asyncio.sleep(e.timeout)
        except Unauthorized:
            await bot.send_message(chat_obj.id,
                                   f"{hlink(player.name, f'tg://user?id={player.id}')}"
                                   f" забомбил 🔥 и заблочил меня!\n"
                                   f"Его персонаж был - {roles_dict_brawl[player.role]}")
            chat_obj.kill(player, Kill('afk'))
        await asyncio.sleep(0.2)


async def mailing_night_messages_to_players(chat_obj, chat_id, bot):
    if chat_obj.cop and Kill() not in chat_obj.cop.effects:
        try:
            await bot.send_message(chat_obj.cop.id,
                                   '❗️ Вам нужно сделать выбор!\n'
                                   'Бездумно изгнать 🔫👿 из Бравл Сити или расчетливо проверить 👁🔎?',
                                   reply_markup=kb_night_cop(chat_id))

        except RetryAfter as e:
            await asyncio.sleep(e.timeout)
        except Unauthorized:
            await bot.send_message(chat_obj.id,
                                   f"{hlink(chat_obj.cop.name, f'tg://user?id={chat_obj.cop.id}')}"
                                   f" забомбил 🔥 и заблочил меня!\n"
                                   f"Его персонаж был - {roles_dict_brawl[chat_obj.cop.role]}")
            chat_obj.kill(chat_obj.cop, Kill('afk'))
        await asyncio.sleep(0.1)

    if chat_obj.don and chat_obj.cop and Kill() not in chat_obj.cop.effects:
        try:
            await bot.send_message(chat_obj.don.id,
                                   'Вам нужно вычислить 🔫🕵️ Кольта!\nКого хотите пробить 📞 по своим связям?',
                                   reply_markup=kb_night_don(chat_obj))

        except RetryAfter as e:
            await asyncio.sleep(e.timeout)
        except Unauthorized:
            await bot.send_message(chat_obj.id,
                                   f"{hlink(chat_obj.don.name, f'tg://user?id={chat_obj.don.id}')}"
                                   f" забомбил 🔥 и заблочил меня!\n"
                                   f"Его персонаж был - {roles_dict_brawl[chat_obj.don.role]}")
            chat_obj.kill(chat_obj.don, Kill('afk'))
        await asyncio.sleep(0.1)

    if chat_obj.doctor and Kill() not in chat_obj.doctor.effects:
        try:
            await bot.send_message(chat_obj.doctor.id,
                                   '🚑👩🏼‍⚕️ Вы можете спасти кого-то от изгнания, но нужно угадать, кого хотят изгнать 🔫!'
                                   '\nКого попытаетесь спасти 💼?',
                                   reply_markup=kb_night_doctor(chat_obj))

        except RetryAfter as e:
            await asyncio.sleep(e.timeout)
        except Unauthorized:
            await bot.send_message(chat_obj.id,
                                   f"{hlink(chat_obj.doctor.name, f'tg://user?id={chat_obj.doctor.id}')}"
                                   f" забомбил 🔥 и заблочил меня!\n"
                                   f"Его персонаж был - {roles_dict_brawl[chat_obj.doctor.role]}")
            chat_obj.kill(chat_obj.doctor, Kill('afk'))
        await asyncio.sleep(0.1)

    if chat_obj.whore and Kill() not in chat_obj.whore.effects:
        try:
            await bot.send_message(chat_obj.whore.id,
                                   '☂️💃 Вы можете устроить кому-то прекрасную ночь, '
                                   'от которой придется оправляться целые сутки 🕑!\n'
                                   'К кому хотите заскочить 🔜?',
                                   reply_markup=kb_night_whore(chat_obj))

        except RetryAfter as e:
            await asyncio.sleep(e.timeout)
        except Unauthorized:
            await bot.send_message(chat_obj.id,
                                   f"{hlink(chat_obj.whore.name, f'tg://user?id={chat_obj.whore.id}')}"
                                   f" забомбил 🔥 и заблочил меня!\n"
                                   f"Его персонаж был - {roles_dict_brawl[chat_obj.whore.role]}")
            chat_obj.kill(chat_obj.whore, Kill('afk'))
        await asyncio.sleep(0.1)

    if chat_obj.homeless and Kill() not in chat_obj.homeless.effects:
        try:
            await bot.send_message(chat_obj.homeless.id,
                                   '🍾 В вашем баре закончились бутылки пива!\n'
                                   'У кого спросить лишнюю бутылку?',
                                   reply_markup=kb_night_homeless(chat_obj))

        except RetryAfter as e:
            await asyncio.sleep(e.timeout)
        except Unauthorized:
            await bot.send_message(chat_obj.id,
                                   f"{hlink(chat_obj.homeless.name, f'tg://user?id={chat_obj.homeless.id}')}"
                                   f" забомбил 🔥 и заблочил меня!\n"
                                   f"Его персонаж был - {roles_dict_brawl[chat_obj.homeless.role]}")
            chat_obj.kill(chat_obj.homeless, Kill('afk'))
        await asyncio.sleep(0.1)

    # если есть мафия
    if chat_obj.mafia:
        for mafia in chat_obj.mafia:
            # если мафиозник не убит
            if Kill() not in mafia.effects:
                try:
                    await bot.send_message(mafia.id,
                                           '🦅 Вы на сходке банды Булла! '
                                           'Кого из жителей Бравл Сити вы хотите незаконно 🔫 изгнать?',
                                           reply_markup=kb_night_mafia(chat_obj))

                except RetryAfter as e:
                    await asyncio.sleep(e.timeout)
                except Unauthorized:
                    await bot.send_message(chat_obj.id,
                                           f"{hlink(mafia.name, f'tg://user?id={mafia.id}')}"
                                           f" забомбил 🔥 и заблочил меня!\n"
                                           f"Его персонаж был - {roles_dict_brawl[mafia.role]}")
                    chat_obj.kill(mafia, Kill('afk'))
                await asyncio.sleep(0.1)

    if chat_obj.don and Kill() not in chat_obj.don.effects:
        try:
            await bot.send_message(chat_obj.don.id,
                                   '🦅 Вы на сходке банды Булла! '
                                   'Кого из жителей Бравл Сити вы хотите незаконно 🔫 изгнать?',
                                   reply_markup=kb_night_mafia(chat_obj))

        except RetryAfter as e:
            await asyncio.sleep(e.timeout)
        except Unauthorized:
            await bot.send_message(chat_obj.id,
                                   f"{hlink(chat_obj.don.name, f'tg://user?id={chat_obj.don.id}')}"
                                   f" забомбил 🔥 и заблочил меня!\n"
                                   f"Его персонаж был - {roles_dict_brawl[chat_obj.don.role]}")
            chat_obj.kill(chat_obj.don, Kill('afk'))
        await asyncio.sleep(0.1)


async def mailing_day_messages_to_players(chat_id, chat_obj, bot) -> types.Message:
    for player in chat_obj.players:
        if Kill() not in player.effects:
            try:
                await bot.send_message(player.id,
                                       'Кого вы хотите изгнать?',
                                       reply_markup=kb_voting_time_users(chat_id, chat_obj.players, player))

            except RetryAfter as e:
                await asyncio.sleep(e.timeout)
            except Unauthorized:
                await bot.send_message(chat_obj.id,
                                       f"{hlink(player.name, f'tg://user?id={player.id}')}"
                                       f" забомбил 🔥 и заблочил меня!\n"
                                       f"Его персонаж был - {roles_dict_brawl[player.role]}")
                chat_obj.kill(player, Kill('afk'))
            await asyncio.sleep(0.1)
    try:
        message_voting: types.Message = await bot.send_message(chat_id,
                                                               'Время дневного голосования! Кого вы хотите изгнать?',
                                                               reply_markup=game_go_to_bot_kb())
        return message_voting
    except RetryAfter as e:
        await asyncio.sleep(e.timeout)
    await asyncio.sleep(0.1)
