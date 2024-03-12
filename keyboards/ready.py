from aiogram import types

READY_MSG = "Я готов(а)"


def get_ready_to_questions_kb():
    kb = [
        [
            types.KeyboardButton(text=READY_MSG),
        ],
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажмите «"
        + READY_MSG
        + "», если Вы готовы отвечать на вопросы",
    )
