from aiogram import types

SHOW_QUESTIONS_MSG = "Показать вопросы раздела"


def get_show_question_kb():
    kb = [
        [
            types.KeyboardButton(text=SHOW_QUESTIONS_MSG),
        ],
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
