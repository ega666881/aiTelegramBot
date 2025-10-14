from .locales.ru import RuLocale, ru_locale
from .locales.eng import EngLocale, eng_locale


def getLocale(lang: str) -> RuLocale:
    match (lang):
        case 'ru':
            return ru_locale
        
        case 'en':
            return eng_locale
        
        case _:
            raise ValueError(f"Unsupported language: {lang}")