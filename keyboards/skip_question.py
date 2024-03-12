from aiogram import types

SKIP_QUESTION_MSG = "Пропустить вопрос"


def get_skip_question_kb():
    kb = [
        [
            types.KeyboardButton(text=SKIP_QUESTION_MSG),
        ],
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Напишите ответ",
    )
