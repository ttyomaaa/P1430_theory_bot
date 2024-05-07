from copy import deepcopy

from aiogram import F
from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db, task_db, photo_db, tasks_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData, IsChapterCallbackData, IsTasksCallbackData
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book
from services.code_casar import caesar_decod, caesar, atbash
import random
from keyboards.tasks_kb import create_tasks_keyboard
from keyboards.chapters_kb import create_chapters_keyboard
from aiogram.types import FSInputFile
from fsm.create_fsm import FSMReadSolve
router: Router = Router()

#router.message.filter(IsTasksCallbackData())
#
# @router.callback_query(F.data == 'code_caesar')
# async def process_tasks_press(callback: CallbackQuery):
#     users_db[callback.from_user.id]['task'] = callback.data
#
#     origin_word = random.choice(task_db[users_db[callback.from_user.id]['chapter']][1])
#     caesar_key = random.randint(1, 10)
#     coded_word = caesar(caesar_key, origin_word)
#     users_db[callback.from_user.id]['bot_secret'] = coded_word
#
#     await callback.message.answer(text=f'{LEXICON[callback.data]}\n'
#                                         f'{origin_word} с ключом {caesar_key}',
#                                 reply_markup=create_tasks_keyboard('return'))
#     await callback.answer()
#
# @router.callback_query(F.data == 'decode_caesar')
# async def process_tasks_press(callback: CallbackQuery):
#     users_db[callback.from_user.id]['task'] = callback.data
#
#     origin_word = random.choice(task_db[users_db[callback.from_user.id]['chapter']][1])
#     caesar_key = random.randint(1, 10)
#     coded_word = caesar(caesar_key, origin_word)
#     users_db[callback.from_user.id]['bot_secret'] = origin_word
#
#     await callback.message.answer(text=f'{LEXICON[callback.data]}\n'
#                                         f'расшифруй {coded_word} с ключом {caesar_key}',
#                                 reply_markup=create_tasks_keyboard('return'))
#     await callback.answer()
#
# @router.callback_query(F.data == 'code_caesar_message')
# async def process_edit_press(callback: CallbackQuery):
#     users_db[callback.from_user.id]['task'] = callback.data
#     await callback.message.answer(
#                 text=f'{LEXICON[callback.data]}\n',
#                 reply_markup=create_tasks_keyboard('return'))
#     await callback.answer()
#
# @router.callback_query(F.data == 'code_atbash_message')
# async def process_edit_press(callback: CallbackQuery):
#     users_db[callback.from_user.id]['task'] = callback.data
#     await callback.message.answer(
#                 text=f'{LEXICON[callback.data]}', reply_markup=create_tasks_keyboard('return'))
#     await callback.answer()
#
# @router.callback_query(F.data == 'code_atbash')
# async def process_tasks_press(callback: CallbackQuery):
#     users_db[callback.from_user.id]['task'] = callback.data
#
#     origin_word = random.choice(task_db[users_db[callback.from_user.id]['chapter']][1])
#     coded_word = atbash(origin_word)
#     users_db[callback.from_user.id]['bot_secret'] = coded_word
#
#     await callback.message.answer_photo(photo=FSInputFile('images/imageinter1.png'),caption=f'{LEXICON[callback.data]}\n'
#                                         f'{origin_word}',
#                                 reply_markup=create_tasks_keyboard('return'))
#     await callback.answer()
#
# @router.callback_query(F.data == 'decode_atbash')
# async def process_tasks_press(callback: CallbackQuery):
#     users_db[callback.from_user.id]['task'] = callback.data
#
#     origin_word = random.choice(task_db[users_db[callback.from_user.id]['chapter']][1])
#     coded_word = atbash(origin_word)
#     users_db[callback.from_user.id]['bot_secret'] = origin_word
#
#     await callback.message.answer_photo(photo=FSInputFile('images/imageinter1.png'),
#                                         caption=f'{LEXICON[callback.data]}\n'
#                                         f'{coded_word}',
#                                 reply_markup=create_tasks_keyboard('return'))
#     await callback.answer()
#
# @router.callback_query(F.data == 'code_slogan_message')
# async def process_edit_press(callback: CallbackQuery):
#     users_db[callback.from_user.id]['task'] = callback.data
#     await callback.message.answer(
#                 text=f'{LEXICON[callback.data]}\n',
#                 reply_markup=create_tasks_keyboard('return'))
#     await callback.answer()
#
# @router.callback_query(F.data == 'decode_akros')
# async def process_tasks_press(callback: CallbackQuery):
#     users_db[callback.from_user.id]['task'] = callback.data
#
#     n = random.choice([1, 2])
#     if n == 1:
#         origin_word = 'Руина чти'
#     else:
#         origin_word = 'Вадиму Шершеневичу'
#     users_db[callback.from_user.id]['bot_secret'] = origin_word
#
#     await callback.message.answer(text=f'{LEXICON[callback.data]}\n'
#                                         f'{task_db[2][n]}',
#                                 reply_markup=create_tasks_keyboard('return'))
#     await callback.answer()