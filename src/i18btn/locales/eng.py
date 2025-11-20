class StartLocale:
    @staticmethod
    def getStartMessage():
        return "By continuing, you agree to the Terms of Use.\nPlease select your language: "

    @staticmethod
    def getMainMenuMessage():
        return "🏠 Main Menu\nChoose the section you need 👇"

    @staticmethod
    def getMainMenuKeyboardText():
        return [
            'Profile',
            '💡 GPTs / Claude / Gemini',
            '🔊 AI Audio',
            '🎨 AI Design',
            '🎬 Future Video',
        ]


class ProfileLocale:
    @staticmethod
    def getProfileKeyboardText():
        return [
            'Buy tokens'
        ]

    @staticmethod
    def getProfileMenuText(tokens: int):
        return f"Profile\nToken balance: {tokens}"

    @staticmethod
    def getBuyTokensText(amount, currency):
        return f"Buy tokens\n1 token = {amount} {currency}\nEnter the number of tokens to purchase"

    @staticmethod
    def getSelectPaymentMethodText():
        return "Select payment method"


class AIModelsLocale:
    @staticmethod
    def getWaitAnswerText():
        return "AI is processing your request..."

    @staticmethod
    def getSelectModelText():
        return "Select a model:"

    @staticmethod
    def getChangeModalText(modelName: str):
        return f"You selected: <b>{modelName}</b>\nSend your request in the chat"


class TextModelsLocale:
    @staticmethod
    def getHelloMessage():
        return """💡 GPTs / Claude / Gemini

Speak 🎙️, type ✍️, or upload an image 🌅 — ask anything in your preferred way and get an instant solution + 🌐 web access (only available with version 4 models)."""

    @staticmethod
    def getMainButtons():
        return [
            'Choose model',
            '◀️ Back'
        ]


class PaymentLocale:
    @staticmethod
    def getTypesPaymentsTitles():
        return {
            "tokens": 'Buy tokens'
        }

    @staticmethod
    def getPayCheckText(amount: int, currency: str):
        return f"Your payment receipt\nAmount: {amount} {currency}"

    @staticmethod
    def getErrorsAmountTexts():
        return [
            '❌ Please enter a whole number (e.g.: 5, 10, 50).',
            '❌ The amount must be greater than 0. Please enter a valid number.'
        ]

    @staticmethod
    def getSuccessPaymentTokensText(amount: int):
        return f"✅ Payment successful\n{amount} tokens have been added to your account"


class SharedTexts:
    @staticmethod
    def getSharedTexts():
        return {
            "cancel": "Cancel",
            "pay": "Pay",
        }


class EngLocale:
    start_locale: StartLocale
    profile_locale: ProfileLocale
    shared_texts: SharedTexts
    payment_locale: PaymentLocale
    text_models_locale: TextModelsLocale
    ai_models_locale: AIModelsLocale

    def __init__(self) -> None:
        self.ai_models_locale = AIModelsLocale()
        self.start_locale = StartLocale()
        self.profile_locale = ProfileLocale()
        self.shared_texts = SharedTexts()
        self.payment_locale = PaymentLocale()
        self.text_models_locale = TextModelsLocale()


eng_locale = EngLocale()