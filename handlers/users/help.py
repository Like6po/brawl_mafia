from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, ChatTypeFilter

from data.db_models import User
from keyboards.inline.callback_datas import help_callback
from keyboards.inline.help import help_kb, help_back_kb, help_roles_kb, help_roles_back_kb
from keyboards.inline.start import start_kb
from loader import dp


@dp.message_handler(CommandHelp(), ChatTypeFilter(types.ChatType.PRIVATE))
async def help_msg(message: types.Message):
    await message.answer('ℹ️ Здесь вы можете получить информацию с помощью кнопок!',
                         reply_markup=help_kb())


@dp.callback_query_handler(help_callback.filter(type='menu'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text('Привет🤘! Я бот-ведущий игры мафия🤵🏻 с элементами Brawl Stars! '
                                'Для начала работы меня необходимо добавить в беседу и выдать права администратора🤖!\n',
                                reply_markup=start_kb())


@dp.callback_query_handler(help_callback.filter(type='kb'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text('ℹ️ Здесь вы можете получить информацию с помощью кнопок!',
                                reply_markup=help_kb())


@dp.callback_query_handler(help_callback.filter(type='phase'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text("🌗 В игре есть две основных фазы:\n\n"
                                "☀️ День:\nДень делится на две части. Первая часть - часть обсуждения. "
                                "Все Бравлеры могут писать в чат и обсуждать свои дальнейшие действия. "
                                "Вторая часть - часть голосования. "
                                "Бравлеры могут отдать голос за изгнания из Бравл Сити "
                                "подозреваемого ими другого Бравлера. "
                                "Если за какого-то из Бравлеров набирается большинство голосов, "
                                "то его кандидатура выставляется на вторую часть голосования, "
                                "где каждый Бравлер (кроме обвиняемого) может проголосовать за изгнание, "
                                "либо за помилование. Если набирается больше голосов 'за', "
                                "то Бравлер изгоняется из Бравл Сити без права на последнее слово.\n\n"
                                "🌑 Ночь:\nС ночью проще. Населяющие Бравл Сити Шелли бездействуют, "
                                "а другие Бравлеры производят свои внутриигровые действия. "
                                "После окончания ночи озвучиваются ее результаты (был ли кто-то изгнан Бандой Булла), "
                                "оперируя которыми можно вычислить членов Банды Булла.\nУдачной игры!",
                                reply_markup=help_back_kb())


@dp.callback_query_handler(help_callback.filter(type='roles'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text('Доступные Бравлеры:',
                                reply_markup=help_roles_kb())


@dp.callback_query_handler(help_callback.filter(type='peace'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text('🙎‍♀️ Шелли (Мирный Житель):\n'
                                'Спит ночью и не совершает каких либо действий, '
                                'днём активно участвует в дискуссии и в голосовании.',
                                reply_markup=help_roles_back_kb())


@dp.callback_query_handler(help_callback.filter(type='don'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text("🐃 Булл (Дон):\nПросыпается ночью также как и каждый Ворон чтобы выбрать жертву. "
                                "Помимо этого, если в Бравл Сити есть Булл, каждую ночь он может проверить "
                                "одного Бравлера, является ли он Кольтом. "
                                "Днём как и все остальные игроки участвует в дискуссии и агитирует "
                                "Бравлеров голосовать против других мирных Бравлеров.",
                                reply_markup=help_roles_back_kb())


@dp.callback_query_handler(help_callback.filter(type='doctor'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text("🚑👩🏼‍⚕️ Пэм (Доктор):\nПросыпается ночью и выбирает, кого будет спасать от "
                                "изгнания из Бравл Сити этой ночью. Если она выбирает Бравлера, которого хотела "
                                "выгнать Банда Булла этой ночью, то этот бравлер остаётся в городе. "
                                "Не может спасти от изгнания себя более 1 раза за игру.",
                                reply_markup=help_roles_back_kb())


@dp.callback_query_handler(help_callback.filter(type='whore'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text("☂️💃 Пайпер (Любовница):\nПросыпается ночью, выбирает любого Бравлера с "
                                "кем бы она хотела провести ночь и приходит к нему домой. Днем и на следующую "
                                "ночь Бравлер не сможет совершать какие-либо действия (даже писать в чат днём).",
                                reply_markup=help_roles_back_kb())


@dp.callback_query_handler(help_callback.filter(type='mafia'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text("🦅 Ворон (Мафия):\nЧлен Банды Булла. Просыпается ночью, чтобы выбрать, кого из "
                                "Бравлеров изгнать из Бравл Сити. Днём как и все остальные Бравлеры участвует в "
                                "голосовании и агитирует игроков голосовать против других мирных Бравлеров.",
                                reply_markup=help_roles_back_kb())


@dp.callback_query_handler(help_callback.filter(type='cop'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text("🔫🕵️ Кольт (Комиссар):\nПросыпается ночью и делает выбор: изгнать Бравлера "
                                "из Бравл Сити или проверить, кем он является. "
                                "Его цель - изгнать всю Банду Булла из Бравл Сити.",
                                reply_markup=help_roles_back_kb())


@dp.callback_query_handler(help_callback.filter(type='homeless'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text("🍾 Барли (Бомж):\nЯвляется обычным мирным жителем, однако,по ночам у него в баре "
                                "кончается пиво, поэтому ему приходится ходить к кому-то в гости за пивом. "
                                "Если он спросит пиво у кого-то из тех, кого захотят изгнать этой ночью из "
                                "Бравл Сити, то Барли обязательно заметит обидчика!",
                                reply_markup=help_roles_back_kb())


@dp.callback_query_handler(help_callback.filter(type='suicide'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text("💣 Тик (Самоубийца):\nЯвляется одиночкой, который не смог завести друзей в "
                                "Бравл Сити. Ему так надоела атмосфера Бравл Сити, что хочется его покинуть, "
                                "однако, Тик сумасшедший, поэтому зациклился на идее, что его должны выгнать "
                                "из Бравл Сити на двевном голосовании.",
                                reply_markup=help_roles_back_kb())


@dp.callback_query_handler(help_callback.filter(type='premium'))
async def cbq_help(cbq: types.CallbackQuery):
    await cbq.message.edit_text("Премиум версия бота включает в себя:\n"
                                "- Отдельный сервер\n"
                                "- Ваше имя бота\n"
                                "- Ваша аватарка бота\n"
                                "- Возможность ограничить доступ к боту только для вас\n\n"
                                "Стоимость - 10$ в месяц.\n"
                                "Обращаться за покупкой к @tih_kot\n\n"
                                "За доплату возможна кастомизация бота (новый язык), "
                                "новые роли, изменение логики бота.",
                                reply_markup=help_back_kb())
