
from aiogram import types
from aiogram.dispatcher.filters import ForwardedMessageFilter


from data.game_models import Dead_day, Kill, Mute
from filters import GroupFilter
from loader import Game, dp


@dp.message_handler(GroupFilter(),
                    ForwardedMessageFilter(is_forwarded=True))
async def any_messages(message: types.Message):
    chat_obj = Game.get_chat(message.chat.id)
    if chat_obj:
        await message.delete()


@dp.message_handler(GroupFilter(),
                    content_types=[types.ContentType.TEXT, types.ContentType.PHOTO, types.ContentType.VIDEO,
                                   types.ContentType.VOICE, types.ContentType.ANIMATION, types.ContentType.DOCUMENT,
                                   types.ContentType.STICKER])
async def any_messages(message: types.Message):
    chat_obj = Game.get_chat(message.chat.id)
    if chat_obj:
        player_obj = chat_obj.get_player(message.from_user.id)
        # если есть такой игрок
        if player_obj:
            if Kill() in player_obj.effects or Mute() in player_obj.effects:
                await message.delete()

            elif chat_obj.phase == 'night':
                await message.delete()

        else:
            if chat_obj.phase != 'starting' and not chat_obj.is_nonplayers_talk:
                await message.delete()
