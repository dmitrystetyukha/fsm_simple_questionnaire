from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import (
    AGREE_MSG,
    NOT_AGREE_MSG,
    get_agree_or_not_kb,
    get_ready_to_questions_kb,
)
from routers.questions import SurveyStates

AGREEMENT_ROUTER = Router()


@AGREEMENT_ROUTER.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(SurveyStates.aggreement)
    await message.answer(
        "Привет! Я задам Вам несколько вопросов. Ответы на них ускорят наже взаимодействие. \nДля начала немного формальности. \n\nСогласны ли Вы на обработку Ваших ответов и персональных данных в рамках нашего сотрудничества?",
        reply_markup=get_agree_or_not_kb(),
    )


@AGREEMENT_ROUTER.message(SurveyStates.aggreement, F.text == AGREE_MSG)
async def agree_message(message: Message, state: FSMContext):
    await state.set_state(SurveyStates.introduction)
    await message.answer(
        "Это здорово\!\nТогда приготовьтесь ответить на несколько вопросов\. Они будут разбиты на несколько разделов\. Если не хотите отвечать \- просто нажмите *«Пропустить»*",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_ready_to_questions_kb(),
    )


@AGREEMENT_ROUTER.message(SurveyStates.aggreement, F.text == NOT_AGREE_MSG)
async def disagree_message(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Очень жаль. В таком случае, я не могу продолжать...\nДо свидания!",
        reply_markup=ReplyKeyboardRemove(),
    )
