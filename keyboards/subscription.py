from aiogram.types import InlineKeyboardMarkup, LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods.create_invoice_link import CreateInvoiceLink

from create_bot import bot
from messages import subscription as messages
from database.models.User import LangTypes


async def subscription_rate(lang: LangTypes) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            texts = ['1 Месяц', '6 Месяцев', '12 Месяцев', 'Назад']
        case LangTypes.EN:
            texts = ['1 Month', '6 Months', '12 Months', 'Back']

    async def invoice(rate: int, currency: int):
        prices = [LabeledPrice(label="XTR", amount=currency)]  
        return await bot(CreateInvoiceLink(
            title=messages.subscription_pay_heading(lang, rate),
            description=messages.subscription_pay_message(lang, rate),  
            prices=prices,  
            provider_token="",  
            payload=f'subscription_for_{rate}_months',  
            currency="XTR",  
        ))
        
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=texts[0] + ' | 1 ⭐', url=await invoice(1, 1))
    keyboard.button(text=texts[1] + ' | 2 ⭐', url=await invoice(6, 2))
    keyboard.button(text=texts[2] + ' | 3 ⭐', url=await invoice(12, 3))
    keyboard.button(text=texts[3], callback_data='profile')
    keyboard.adjust(1, repeat=True)

    return keyboard.as_markup()
    
    
def subscription_pay(lang: LangTypes, currency: int) -> InlineKeyboardMarkup:
    match lang:
        case LangTypes.RU:
            text = 'Назад'
        case LangTypes.EN:
            text = 'Back'
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f'{currency} ⭐', pay=True)
    keyboard.button(text=text, callback_data='subscription')
    return keyboard.as_markup()