from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from vk_api import VkApi

from data.config import vk_api_service_key, qiwi_public_key
from keyboards.inline.callback_datas import shop_callback


def generate_link_to_pay(user_id, amount):
    link = f"https://oplata.qiwi.com/" \
           f"create?" \
           f"publicKey={qiwi_public_key}" \
           f"&amount=30" \
           f"&comment=brawl_mafia:{amount}:{user_id}" \
           f"&successUrl=https://t.me/brawl_mafia_bot"
    #return link
    return VkApi(token=vk_api_service_key).get_api().utils.getShortLink(url=link)['short_url']


def shop_kb():
    kb_obj = InlineKeyboardMarkup()
    key_docs = InlineKeyboardButton(text='🛒📂 Документы (💎 30)',
                                    callback_data=shop_callback.new(type='document'))
    key_gems = InlineKeyboardButton(text='🕵️‍♂️ Активная роль(💎 60)',
                                    callback_data=shop_callback.new(type='active_role'))
    key_back = InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=shop_callback.new(type='back'))
    kb_obj.row(key_docs)
    kb_obj.row(key_gems)
    kb_obj.row(key_back)
    return kb_obj


def gems_kb(user_id):
    kb_obj = InlineKeyboardMarkup()
    kb_obj.row(InlineKeyboardButton(text="💎 100 - 30р",
                                    url=generate_link_to_pay(user_id, 30)))
    kb_obj.row(InlineKeyboardButton(text="💎 300 - 80р",
                                    url=generate_link_to_pay(user_id, 80)))
    kb_obj.row(InlineKeyboardButton(text="💎 500 - 120р",
                                    url=generate_link_to_pay(user_id, 120)))
    kb_obj.row(InlineKeyboardButton(text="💎 1000 - 250р",
                                    url=generate_link_to_pay(user_id, 250)))
    kb_obj.row(InlineKeyboardButton(text="💎 2500 - 600р",
                                    url=generate_link_to_pay(user_id, 600)))
    kb_obj.row(InlineKeyboardButton(text="💎 5000 - 1000р",
                                    url=generate_link_to_pay(user_id, 1000)))
    kb_obj.row(InlineKeyboardButton(text="✅ОПЛАТИЛ!!!✅",
                                    callback_data=shop_callback.new(type='pay')))
    kb_obj.row(InlineKeyboardButton(text='↩️ Назад',
                                    callback_data=shop_callback.new(type='back')))
    return kb_obj
