from database.models.User import LangTypes


async def subscription_rate(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Выберите тариф'
        case LangTypes.EN:
            return 'Choose plan'


async def subscription_payment_method(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Выберите метод оплаты'
        case LangTypes.EN:
            return 'Choose payment method'


async def subscription_payment(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Перейдите по ссылке чтобы оплатить'
        case LangTypes.EN:
            return 'Follow the link to pay'
