import logging

from aiogram import types
from aiogram.utils.markdown import hbold, hlink

from data.game_models import Kill
from loader import dp, Game
from utils.misc.mailing_process import roles_dict_brawl


@dp.errors_handler()
async def errors_handler(update: types.update.Update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """
    from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                          CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                          MessageTextIsEmpty, RetryAfter,
                                          CantParseEntities, MessageCantBeDeleted, BadRequest,
                                          NotEnoughRightsToPinMessage)

    if isinstance(exception, CantDemoteChatCreator):
        logging.debug("Can't demote chat creator")
        return True

    if isinstance(exception, BadRequest):
        logging.exception(f'BadRequest: {exception} \nUpdate: {update}')

        if exception.args[0].lower() in ['not enough rights to change chat permissions',
                                         'not enough rights to manage pinned messages in the chat',
                                         "message can't be deleted"]:
            await dp.bot.send_message(update.message.chat.id, f'Для адекватной работы мне необходимы '
                                                              f'права {hbold("Блокировка участников")}, '
                                                              f'{hbold("Закрепление сообщений")} '
                                                              f'и {hbold("Удаление сообщений")}!\n'
                                                              f'Верните меня в беседу и выдайте нужные права!')
            Game.remove_chat(Game.get_chat(update.message.chat.id))
            await dp.bot.leave_chat(update.message.chat.id)
        return True

    if isinstance(exception, MessageNotModified):
        logging.debug('Message is not modified')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.debug('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.debug('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.info(f'Unauthorized: {exception}')
        if exception.args[0] == 'Forbidden: bot is not a member of the supergroup chat':
            Game.remove_chat(Game.get_chat(update.message.chat.id))
        if exception.args[0] == 'Forbidden: bot was blocked by the user':
            result = Game.search_player(update.message.from_user.id)
            if not result:
                return True
            chat_obj, player_obj = result

            await dp.bot.send_message(chat_obj.id,
                                      f"{hlink(player_obj.name, f'tg://user?id={player_obj.id}')}"
                                      f" забомбил 🔥 и заблочил меня!\n"
                                      f"Его персонаж был - {roles_dict_brawl[player_obj.role]}")

            chat_obj.kill(player_obj, Kill('afk'))
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    logging.exception(f'Update: {update} \n{exception}')
