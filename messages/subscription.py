from database.models.User import LangTypes


def subscription_rate(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU: return 'Выберите тариф\n\n1 месяц - 250⭐\n6 месяцев -20% - 1200⭐\n12 месяцев -30% - 2100⭐'
        case LangTypes.EN: return 'Choose plan\n\n1 month - 250⭐\n6 months -20% - 1200⭐\n12 months -30% - 2100⭐'


def subscription_already(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU: return '✅ Подписка уже оформлена'
        case LangTypes.EN: return '✅ You are already subscribed'

    
def stars_todo(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU: return '⭐ TG Stars скоро...'
        case LangTypes.EN: return '⭐ TG Stars soon...'


def subscription_pay_heading(lang: LangTypes, rate: int) -> str:
    match lang:
        case LangTypes.RU:
            return f'Подписка на {rate} {"Месяц" if rate == 1 else "Месяцев"}'
        case LangTypes.EN:
            return f'{rate} {"Month" if rate == 1 else "Months"} Subscription'


def subscription_pay_message(lang: LangTypes, rate: int) -> str:
    match lang:
        case LangTypes.RU:
            return f'Покупка подписки на {rate} {"Месяц" if rate == 1 else "Месяцев"}'
        case LangTypes.EN:
            return f'Purchasing a {rate} {"Month" if rate == 1 else "Months"} subscription'


def successful_payment(lang: LangTypes) -> str: 
    match lang:
        case LangTypes.RU: return '😄 Спасибо за покупку подписки 🌠'
        case LangTypes.EN: return '😄 Thank you for subscription 🌠'
