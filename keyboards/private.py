from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start() -> InlineKeyboardMarkup:
    btn_create_album = InlineKeyboardButton(text='Создать альбом', callback_data='create_album')
    btn_create_vinyl = InlineKeyboardButton(text='Создать пластинку', callback_data='create_vinyl')
    btn_profile = InlineKeyboardButton(text='Профиль', callback_data='profile')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_create_album],
            [btn_create_vinyl],
            [btn_profile]
        ]
    )


def profile() -> InlineKeyboardMarkup:
    btn_language = InlineKeyboardButton(text='Язык', callback_data='language')
    btn_subscription = InlineKeyboardButton(text='Оформить подписку', callback_data='subscription')
    btn_back = InlineKeyboardButton(text='Назад', callback_data='start')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_language],
            [btn_subscription],
            [btn_back]
        ]
    )


def language() -> InlineKeyboardMarkup:
    btn_language_russian = InlineKeyboardMarkup(text='Russian', callback_data='language_russian')
    btn_language_english = InlineKeyboardMarkup(text='English', callback_data='language_english')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [btn_language_russian],
            [btn_language_english],
        ]
    )


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

    
