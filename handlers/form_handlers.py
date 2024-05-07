from aiogram import Router, F
from handlers.user_handlers import _get_book_data
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.get_data_service import get_questions_by_chapter, get_reports_user, get_results, get_users
from aiogram.filters import StateFilter, and_f
from app.create_data_service import create_form, create_forms_data, update_result_and_chapter
from aiogram.types import BufferedInputFile
from stats import get_stats, buf
from settings import bot
from handlers.user_handlers import process_help_cmd
import datetime

from fsm.create_fsm import FSMReadSolve

router: Router = Router()


async def clear_msg_error(msg, result, current_id, form, id_chapter, state):
    current_state = await state.get_state()
    await state.clear()
    await state.set_state(current_state)
    await state.update_data(msg=msg, result=result, current_id=current_id, form=form, id_chapter=id_chapter)


def check_answer(text, ans):
    for a in ans:
        if a['answer'] == text:
            return [True, a['id_answer']]
    return [False, 0]


def get_score(result, form):
    score = 0

    for res in result:
        for id_question, id_answer in res.items():
            for answers in form:
                for a in answers['answers']:
                    if a['id_answer'] == id_answer:
                        if a['is_correct']:
                            score += 1
    return score


def reply_keyboard_tests(answers: list) -> ReplyKeyboardMarkup:

    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    for i in range(len(answers)):
        kb_builder.row(KeyboardButton(text=answers[i]))
    kb_builder.row(KeyboardButton(text='🔙 Назад'), KeyboardButton(text='❌ Выход'))

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


async def send_test(form, current_id, message):
    a = []
    q = ''
    file = None
    for questions in form:
        if questions['q_number'] == current_id:
            q = str(questions['q_number']) + '. ' + questions['question']
            if questions['q_file']:
                file = questions['q_file']
            answers = questions['answers']
            for answer in answers:
                a.append(answer['answer'])
            break
    if file:
        msg = await message.answer_photo(
            caption=q,
            photo=FSInputFile(file),
            reply_markup=reply_keyboard_tests(a)
        )
    else:
        msg = await message.answer(
            text=q,
            reply_markup=reply_keyboard_tests(a)
        )
    return msg


@router.callback_query(F.data == 'form', ~StateFilter(FSMReadSolve.solve_task))
async def process_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    id_chapter = await _get_book_data(state, 'chapter')
    await state.clear()
    await state.set_state(FSMReadSolve.form)
    form = await get_questions_by_chapter(int(id_chapter))
    current_id = 1
    msg = await send_test(form, current_id, callback.message)
    await state.update_data(current_id=current_id, result=[], msg=msg, form=form, id_chapter=id_chapter)


@router.message(StateFilter(FSMReadSolve.form))
async def process_form(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    try:
        await data['msg_error'].delete()
    except KeyError:
        pass
    else:
        await clear_msg_error(data["msg"], data["result"], data['current_id'], data['form'], data["id_chapter"], state)
    await data['msg'].delete()

    current_id = data['current_id']
    form = data['form']

    if message.text == "❌ Выход":
        await state.clear()
        await state.set_state(FSMReadSolve.choose_action)
        await process_help_cmd(message)
        return
    if message.text == "🔙 Назад":
        if current_id != 1:
            current_id -= 1

        result = data['result']
        if result:
            result.pop()
        msg = await send_test(form, current_id, message)
        await state.update_data(current_id=current_id, result=result, msg=msg)
        return

    for qs in form:
        if qs['q_number'] == current_id:
            answer_check = qs['answers']
            break

    flag = check_answer(message.text, answer_check)

    if not flag[0]:
        msg_error = await message.answer(
            text="Такой ответ не предусмотрен!",
            reply_markup=None
        )
        msg = await send_test(form, current_id, message)
        await state.update_data(msg=msg, msg_error=msg_error)
        return

    result = data['result']
    result.append({current_id: flag[1]})
    await state.update_data(result=result)
    current_id += 1

    if current_id == (len(form)+1):
        data = await state.get_data()
        forms_data = await create_forms_data()
        id_forms_data = forms_data['id_forms_data']
        await create_form(result=data['result'],
                          id_forms_data=id_forms_data,
                          user_tg_id=message.from_user.username,
                          id_tg=message.from_user.id)

        score = get_score(result=data['result'], form=form)

        await update_result_and_chapter(id_forms_data=id_forms_data, result=score, id_chapter=data["id_chapter"], created_date=datetime.datetime.utcnow())
        await message.answer(
            text=f"Тест успешно завершен.\nРезультат: {score}/{len(form)}.",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
        await state.set_state(FSMReadSolve.choose_action)
        await message.answer(
            text="Чтобы вернуться к чтению воспользуйтесь командой /chapters",
            reply_markup=None
        )
        return

    msg = await send_test(form, current_id, message)
    await state.update_data(current_id=current_id, msg=msg)


@router.message(StateFilter(FSMReadSolve.form))
async def clean_message(message: Message):
    await message.delete()
