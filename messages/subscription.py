from database.models.User import LangTypes


def subscription_rate(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Выберите тариф'
        case LangTypes.EN:
            return 'Choose plan'


def subscription_already(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return '✅ Подписка уже оформлена'
        case LangTypes.EN:
            return '✅ You are already subscribed'


def subscription_payment_method(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Выберите метод оплаты'
        case LangTypes.EN:
            return 'Choose payment method'


def subscription_payment(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Перейдите по ссылке чтобы оплатить'
        case LangTypes.EN:
            return 'Follow the link to pay'


def payment_fault(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Вы ещё не оплатили ❌'
        case LangTypes.EN:
            return 'You haven\'t paid yet ❌'


def payment_success(lang: LangTypes) -> str:
    match lang:
        case LangTypes.RU:
            return 'Спасибо за покупку ✅'
        case LangTypes.EN:
            return 'Thank you for your purchase ✅'