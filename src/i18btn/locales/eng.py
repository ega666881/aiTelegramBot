

class StartLocale: 
    @staticmethod
    def getStartMessage(): 
        return f"By continuing, you agree to the terms of use\nPlease select a language:"

    @staticmethod
    def getMainMenuMessage():
        return "🏠 Main menu\nSelect the appropriate section 👇"

    @staticmethod
    def getMainMenuKeyboardText():
        return [
                'Profile',
                '💡 GPTs/Claude/Gemini',
                '🔊 AI Audio',
                '🎨 AI Design',
                '🎬 Video of the Future',
            ]
    

class ProfileLocale:
    @staticmethod
    def getProfileKeyboardText():
        return [
            'Buy tokens'
        ]

    def getProfileMenuText(tokens):
        return f"Profile\nToken balance: {tokens}"

    @staticmethod
    def getBuyTokensText(amount, currency):
        return f"Token purchase\n1 token = {amount} {currency}\nEnter the number of tokens to purchase"

    @staticmethod
    def getSelectPaymentMethodText():
        return f"Select payment method"

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
            '❌ Please enter a whole number (e.g., 5, 10, 50).',
            '❌ The amount must be greater than 0. Please enter a valid number.'
        ]
    
    @staticmethod
    def getSuccessPaymentTokensText(amount: int):
        return f"✅ Payment successful\nYou have been credited with {amount} tokens"


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

    def __init__(self) -> None:
        self.start_locale = StartLocale()
        self.profile_locale = ProfileLocale()
        self.shared_texts = SharedTexts()
        self.payment_locale = PaymentLocale()

eng_locale = EngLocale()
