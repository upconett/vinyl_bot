from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import User as AIOgramUser

from database.models.User import LangTypes


async def subscription_rate(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            texts = ['1 Месяц', '6 Месяцев', '12 Месяцев', 'Назад']
        case LangTypes.EN:
            texts = ['1 Month', '6 Months', '12 Months', 'Back']
    btn_subscription_rate_month = InlineKeyboardButton(text=texts[0], callback_data='subscription_rate_1')
    btn_subscription_rate_3months = InlineKeyboardButton(text=texts[1], callback_data='subscription_rate_6')
    btn_subscription_rate_forever = InlineKeyboardButton(text=texts[2], callback_data='subscription_rate_12')
    btn_back = InlineKeyboardButton(text=texts[3], callback_data='profile')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_subscription_rate_month],
            [btn_subscription_rate_3months],
            [btn_subscription_rate_forever],
            [btn_back]
        ]
    )
    

async def subscription_payment_method(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU: text_back = 'Назад'
        case LangTypes.EN: text_back = 'Back'
    btn_subscription_payment_method_yoomoney = InlineKeyboardButton(
        text='YooMoney', callback_data='subscription_payment_method_yoomoney')
    btn_subscription_payment_method_paypal = InlineKeyboardButton(
        text='PayPal', callback_data='subscription_payment_method_paypal')
    btn_back = InlineKeyboardButton(text=text_back, callback_data='subscription')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_subscription_payment_method_yoomoney],
            [btn_subscription_payment_method_paypal],
            [btn_back]
        ]
    )


async def subscription_payment(lang: LangTypes, payment_link: str) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            texts = ['Оплатить', 'Я оплатил ✅', 'Назад']
        case LangTypes.EN:
            texts = ['Pay', 'Done ✅', 'Back']
    btn_subscription_payment_buy = InlineKeyboardButton(text=texts[0], url=payment_link)
    btn_subscription_payment_check = InlineKeyboardButton(text=texts[1], callback_data='subscription_check')
    btn_back = InlineKeyboardButton(text=texts[2], callback_data='subscription')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_subscription_payment_buy],
            [btn_subscription_payment_check],
            [btn_back]
        ]
    )

    
