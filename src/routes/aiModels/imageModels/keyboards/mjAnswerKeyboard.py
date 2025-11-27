from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def mjAnswerKeyboard(buttonsTexts: list, imageUrls: list[str]):
    buttons = []

    counter = 1
    for url in imageUrls:
        buttons.append(
            [
                InlineKeyboardButton(url=url, text=f'Download image {counter}'),
            ],
        )
        counter += 1
    
    buttons.append(
        [
            InlineKeyboardButton(text=buttonsTexts[0], callback_data="select_mj"),
        ],
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
