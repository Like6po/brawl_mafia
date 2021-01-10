from aiogram import types


from filters import GroupFilter
from loader import Game, dp


@dp.message_handler(GroupFilter(),
                    content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_member(message: types.Message):
    members_list = message.new_chat_members
    for user in members_list:
        if user.id == (await dp.bot.get_me()).id:
            await message.answer('Привет🤘! Я бот-ведущий игры мафия🤵🏻 с элементами Brawl Stars!\n'
                                 '⚠️ Для адекватной работы мне остро необходимы права администратора!\n'
                                 'Дополнительную информацию можно найти по команде /help в личных сообщениях со мной!')
        else:
            chat_obj = Game.get_chat(message.chat.id)
            if chat_obj:
                if chat_obj.phase in ['day', 'night']:
                    await message.answer(f"💬 {user.get_mention()}, добро пожаловать!"
                                         f"\nВ данный момент идет игра, вам нужно подождать 🕗, "
                                         f"пока она закончится! "
                                         f"А пока вы можете ознакомиться с ℹ️ правилами игры: /help")
                elif chat_obj.phase == 'starting':
                    await message.answer(f"💬 {user.get_mention()}, добро пожаловать!\n"
                                         f"В данный момент идет подбор игроков, вы можете 🎭 присоединиться!")
            else:
                await message.answer(f"💬 {user.get_mention()}, добро ожаловать!\n"
                                     f"В данный момент не идет игры, "
                                     f"вы можете ознакомиться с ℹ️ правилами игры: /help.")


@dp.message_handler(content_types=[types.ContentType.GROUP_CHAT_CREATED])
async def group_created(message: types.Message):
    await message.answer('Привет🤘! Я бот-ведущий игры мафия🤵🏻 с элементами Brawl Stars!\n'
                         '⚠️ Для адекватной работы мне остро необходимы права администратора!\n'
                         'Дополнительную информацию можно найти по команде /help в личных сообщениях со мной!')