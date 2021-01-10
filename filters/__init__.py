from aiogram import Dispatcher


from .is_group import GroupFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(GroupFilter)
