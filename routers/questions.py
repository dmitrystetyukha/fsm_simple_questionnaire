import json
import os
from datetime import datetime

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, ReplyKeyboardRemove
from magic_filter import MagicFilter

from bot import MANAGER_TG_ID, bot
from keyboards import SKIP_QUESTION_MSG
from keyboards.show_question import get_show_question_kb
from keyboards.skip_question import get_skip_question_kb

QUESTIONS_ROUTER = Router()


class SurveyStates(StatesGroup):
    aggreement = State()
    introduction = State()
    chapter_started = State()
    questioning = State()
    question_answered = State()
    # question_skipped = State()
    goodbye = State()


# Загрузка вопросов из файла
with open("questions.json", "r", encoding="utf-8") as f:
    questions = sorted(json.load(f), key=lambda x: x["stage"])


@QUESTIONS_ROUTER.message(
    SurveyStates.introduction,
)
async def process_survey_by_chapter(message: Message, state: FSMContext):
    await state.set_state(SurveyStates.chapter_started)

    data = await state.get_data()

    if "current_chapter_idx" not in data:
        data["current_chapter_idx"] = 0

    current_chapter_idx = data["current_chapter_idx"]

    if current_chapter_idx >= len(questions):
        await finish_dialog(message, state)
        return

    current_chapter = questions[current_chapter_idx]
    current_chapter["questions"] = sorted(
        current_chapter["questions"], key=lambda x: x["stage"]
    )
    data["current_chapter"] = current_chapter

    text = f'{current_chapter_idx + 1}\-й раздел вопросов: *«{questions[current_chapter_idx]["chapter_name"]}»*'
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=get_show_question_kb(),
    )
    await state.set_data(data)


@QUESTIONS_ROUTER.message(
    SurveyStates.chapter_started,
)
async def process_survey_by_question(message: Message, state: FSMContext):
    await state.set_state(SurveyStates.questioning)
    data = await state.get_data()
    if "current_question_idx" not in data:
        data["current_question_idx"] = 0

    current_chapter = data["current_chapter"]
    current_question_idx = data["current_question_idx"]

    if current_question_idx >= len(current_chapter["questions"]):
        await set_next_chapter(state)
        await process_survey_by_chapter(message, state)
        return

    await state.set_data(data)

    await message.answer(
        current_chapter["questions"][current_question_idx]["text"],
        reply_markup=get_skip_question_kb(),
    )


@QUESTIONS_ROUTER.message(
    SurveyStates.questioning, F.text == SKIP_QUESTION_MSG
)
async def skip_question(message: Message, state: FSMContext):
    await set_next_question(state)
    await process_survey_by_question(message, state)


async def set_next_question(state: FSMContext):
    data = await state.get_data()
    data["current_question_idx"] += 1
    await state.set_data(data)


async def set_next_chapter(state: FSMContext):
    data = await state.get_data()
    data["current_chapter_idx"] += 1
    data["current_question_idx"] = 0
    await state.set_data(data)


@QUESTIONS_ROUTER.message(
    SurveyStates.questioning, MagicFilter.len((F.text)) > 1
)
async def process_answer(message: Message, state: FSMContext):
    data = await state.get_data()

    current_chapter_text = data["current_chapter"]["chapter_name"]
    current_question_text = data["current_chapter"]["questions"][
        data["current_question_idx"]
    ]["text"]

    if "answers" not in data:
        data["answers"] = {
            "user": {
                "id": message.from_user.id,
                "username": message.from_user.username,
            },
            current_chapter_text: [
                {
                    "question": current_question_text,
                    "answer": message.text,
                }
            ],
        }
    else:
        if current_chapter_text not in data["answers"]:
            data["answers"][current_chapter_text] = [
                {
                    "question": current_question_text,
                    "answer": message.text,
                }
            ]
        else:
            data["answers"][current_chapter_text].append(
                {
                    "question": current_question_text,
                    "answer": message.text,
                }
            )

    await state.set_data(data)
    await set_next_question(state)
    await process_survey_by_question(message, state)


async def finish_dialog(message: Message, state: FSMContext):
    data = await state.get_data()
    answers = data["answers"]
    filename = f"answers_{message.from_user.id}_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.json"
    with open(
        os.path.join("answers", filename), "w", encoding="utf-8"
    ) as file:
        json.dump(answers, file, ensure_ascii=False, indent=4)

    manager_text = (
        f'@{answers["user"]["username"]} ответил на сообщения. Вот его ответы:'
    )
    file = FSInputFile(os.path.join("answers", filename))
    await bot.send_document(MANAGER_TG_ID, file, caption=manager_text)

    await message.answer(
        f"Ваши ответы обязательно будут просмотрены. Ждите ответа от менеджера",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()
