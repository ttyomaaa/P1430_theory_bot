from aiogram import Router, F
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
router = Router()


class StatesForm(StatesGroup):
    start = State()
    form = State()


async def merge_to_report(username, mode=False):
    forms = await get_reports_user(username)
    if not forms:
        if mode:
            return [{}]
        return "отсутствуют."
    results = await get_results()
    reports_string = f"\n"
    reports = []
    flag = 0
    for result in results:
        for form in forms:
            if result['id_forms_data'] == form['id_forms_data']:
                flag = 1
                break
            else:
                flag = 0
        if flag == 1:
            reports.append(
                 {
                    'id_chapter': result['id_chapter'],
                    'result': result['result'],
                    'created_date': result['created_date']
                 }
            )
            reports_string += f"Глава: {result['id_chapter']} - Балл: {result['result']} - Дата: {result['created_date']}\n"

    if mode:
        return reports
    return reports_string


async def send_publication(text: str):
    users = await get_users()
    result = []
    for user in users:
        for key, value in user.items():
            if value not in result:
                result.append(value)
    for tg_id in result:
        try:
            await bot.send_message(text=text, chat_id=tg_id)
        except:
            pass
