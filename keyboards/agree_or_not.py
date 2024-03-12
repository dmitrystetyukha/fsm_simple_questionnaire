from aiogram import types

AGREE_MSG = "Да, продолжим"
NOT_AGREE_MSG = "Нет, прекратить"


def get_agree_or_not_kb():
    kb = [
        [
            types.KeyboardButton(text=AGREE_MSG),
            types.KeyboardButton(text=NOT_AGREE_MSG),
        ],
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите вариант ответа",
    )
