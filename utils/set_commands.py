from aiogram.types import BotCommand


async def set_commands(dp):
    await dp.bot.set_my_commands([BotCommand('start', 'Начать игру!'),
                                 BotCommand('help', 'Помощь по командам!'),
                                  BotCommand('leave', 'Покинуть игру!'),
                                  BotCommand('extend', 'Продлить регистрацию!'),
                                  BotCommand('close', 'Закончить игру!'),
                                  BotCommand('play', 'Закончть регистрацию досрочно!'),
                                  BotCommand('settings', 'Настройки беседы!')])
