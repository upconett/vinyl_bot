from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def subscription_rate() -> InlineKeyboardMarkup:
    btn_subscription_rate_month = InlineKeyboardButton(text='Месяц', callback_data='subscription_rate_month')
    btn_subscription_rate_3months = InlineKeyboardButton(text='3 Месяца', callback_data='subscription_rate_3months')
    btn_subscription_rate_forever = InlineKeyboardButton(text='Бессрочно', callback_data='subscription_rate_forever')
    btn_back = InlineKeyboardButton(text='Назад', callback_data='profile')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_subscription_rate_month],
            [btn_subscription_rate_3months],
            [btn_subscription_rate_forever],
            [btn_back]
        ]
    )
    

def subscription_payment_method() -> InlineKeyboardMarkup:
    btn_subscription_payment_method_yoomoney = InlineKeyboardButton(
        text='Yoomoney', callback_data='subscription_payment_method_yoomoney')
    btn_subscription_payment_method_paypal = InlineKeyboardButton(
        text='PayPal', callback_data='subscription_payment_method_paypal')
    btn_back = InlineKeyboardButton(text='Назад', callback_data='subscription')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_subscription_payment_method_yoomoney],
            [btn_subscription_payment_method_paypal],
            [btn_back]
        ]
    )


def subscription_payment() -> InlineKeyboardMarkup:
    btn_subscription_payment_buy = InlineKeyboardButton(
        text='Оплатить', url='sublimit.ru'
    )
    btn_back = InlineKeyboardButton(text='Назад', callback_data='subscription')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_subscription_payment_buy],
            [btn_back]
        ]
    )

    
