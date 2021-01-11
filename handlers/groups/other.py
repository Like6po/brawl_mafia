from keyboards.inline.other import only_in_conv

from loader import dp, Game


@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), commands=['leave', 'settings', 'extend', 'play', 'close'])
async def not_available_commands(message: types.Message):
    await message.answer('⚠️ Данное действие доступно только в беседах!',
                         reply_markup=only_in_conv())