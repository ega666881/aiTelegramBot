

class StartLocale: 
    @staticmethod
    def getStartMessage(): 
        return f"Продолжая, вы соглашаетесь с условиями использования\n\
            пожалуйста, выберите язык: "
    
    @staticmethod
    def getMainMenuMessage():
        return "🏠 Главное меню\nВыберите нужный раздел 👇"


    @staticmethod
    def getMainMenuKeyboardText():
        return [
                'Профиль',
                '💡 GPTs/Claude/Gemini',
                '🔊 Аудио с ИИ',
                '🎨 Дизайн с ИИ',
                '🎬 Видео будущего',
            ]
    


class ProfileLocale:
    @staticmethod
    def getProfileKeyboardText():
        return [
            'Купить токены'
        ]

    @staticmethod
    def getProfileMenuText(tokens: int):
        return f"Профиль\nБаланс токенов: {tokens}"

    @staticmethod
    def getBuyTokensText(amount, currency):
        return f"Покупка токенов\n1 токен = {amount} {currency}\nВведите количество токенов для покупки"

    @staticmethod
    def getSelectPaymentMethodText():
        return f"Выберите способ оплаты"

class TextModelsLocale:
    @staticmethod
    def getHelloMessage():
        return """💡 GPTs/Claude/Gemini

🎙️ Голосом, ✍️ текстом, 🌅 изображением — задавайте любые вопросы удобным способом и SYNTX тут же найдёт решение + 🌐 выход в интернет (только 4 версия модели)."""

    @staticmethod
    def getMainButtons():
        return [
            'Выбрать модель',
            '◀️Назад'
        ]

class PaymentLocale:
    @staticmethod
    def getTypesPaymentsTitles():
        return {
            "tokens": 'Покупка токенов'
        }
    
    @staticmethod
    def getPayCheckText(amount: int, currency: str): 
        return f"Ваш чек на оплату\nСумма: {amount} {currency}"

    @staticmethod
    def getErrorsAmountTexts():
        return [
            '❌ Пожалуйста, введите целое число (например: 5, 10, 50).',
            '❌ Сумма должна быть больше 0. Пожалуйста, введите корректное число.'
        ]
    
    @staticmethod
    def getSuccessPaymentTokensText(amount: int):
        return f"✅ Оплата прошла успешно\nВам начислено {amount} токенов"


class SharedTexts:
    @staticmethod
    def getSharedTexts(): 
        return {
            "cancel": "Отмена",
            "pay": "Оплатить",
        } 

class RuLocale:
    start_locale: StartLocale
    profile_locale: ProfileLocale
    shared_texts: SharedTexts
    payment_locale: PaymentLocale
    text_models_locale: TextModelsLocale

    def __init__(self) -> None:
        self.start_locale = StartLocale()
        self.profile_locale = ProfileLocale()
        self.shared_texts = SharedTexts()
        self.payment_locale = PaymentLocale()
        self.text_models_locale = TextModelsLocale()

ru_locale = RuLocale()