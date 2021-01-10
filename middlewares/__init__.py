from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
#from .data import DataMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    #dp.middleware.setup(DataMiddleware())
