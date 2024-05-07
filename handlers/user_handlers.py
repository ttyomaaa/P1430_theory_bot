from copy import deepcopy

from aiogram import F
from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart,  StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db, task_db, photo_db
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
from aiogram.types import InputMediaPhoto
from aiogram.types import BufferedInputFile
from stats import get_stats, buf
from lexicon.lexicon import LEXICON
from fsm.create_fsm import FSMReadSolve
from utils import merge_to_report


router: Router = Router()


async def _save_book_data(state: FSMContext, **kwargs):
    #print(f'kwargs {kwargs}')
    for key, value in kwargs.items():
        await state.update_data(**{key:value})

async def _get_book_data(state: FSMContext, key):
    data = await state.get_data()
    book_data = data.get(key)
    return book_data

async def _fill_state(state: FSMContext, data):
    await _save_book_data(state, **data)


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())#, StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(LEXICON['/start'])
    # p = await state.get_data()
    # print(p)
    #await state.clear()
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
        await _fill_state(state, user_dict_template)
    await state.set_state(FSMReadSolve.choose_action)
    await state.update_data(user_db=users_db[message.from_user.id])
    #current_state = await state.get_state()


@router.message(StateFilter(default_state))
async def process_not_start_command(message: Message):
    await message.answer(LEXICON['~start'])

# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command(commands='beginning'), ~StateFilter(FSMReadSolve.solve_task))
async def process_beginning_command(message: Message, state: FSMContext):
    #await _save_book_data(state, chapter=1, page=1)
    users_db[message.from_user.id]['page'] = 1
    users_db[message.from_user.id]['chapter'] = 1
    chapter = users_db[message.from_user.id]['chapter']
    page = users_db[message.from_user.id]['page']
    text = book[chapter][page]
    await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{page}/{len(book[chapter])}',
                    'forward', chapter=chapter))
    await state.set_state(FSMReadSolve.read_text)
    await state.update_data(user_db=users_db[message.from_user.id])

# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'), ~StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])


# @router.message(Command(commands='cheat'))
# async def process_cheat_command(message:Message):
#     await message.answer(LEXICON['/cheat'])

# @router.message(Text(text=['ошибка']))
# async def process_ask_mistakes(message: Message):
#              await message.answer(text ='ошибки нет')

@router.message(Command(commands='chapters'), ~StateFilter(default_state))
async def process_help_cmd(message: Message):
    await message.answer(LEXICON['/chapters'], reply_markup=create_chapters_keyboard())


@router.callback_query(F.data == 'main_return', ~StateFilter(default_state))
async def process_main_return(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(LEXICON['/chapters'], reply_markup=create_chapters_keyboard())

@router.callback_query(F.data == 'audio', ~StateFilter(default_state))
async def process_audio(callback: CallbackQuery, state: FSMContext):
    chapter = users_db[callback.from_user.id]['chapter']
    page = users_db[callback.from_user.id]['page']
    await callback.message.answer_audio(FSInputFile(f"audio/{chapter}p{page}.mp3", f"chapter{chapter}"))
    await callback.message.answer(LEXICON['audio'], reply_markup=create_chapters_keyboard())

# def _able_to_edit(message: Message):


# def _change_msg(message: Message):
#     page = users_db[message.from_user.id]['page']
#     chapter = users_db[message.from_user.id]['chapter']
#     text = book[chapter][page]


# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands=['continue']), ~StateFilter(FSMReadSolve.solve_task))
async def process_continue_command(message: Message, state: FSMContext):
    page = await _get_book_data(state, 'page')
    users_db[message.from_user.id]['page'] = page
    chapter = await _get_book_data(state, 'chapter')
    users_db[message.from_user.id]['chapter'] = chapter
    text = book[chapter][page]
    keyboard = create_pagination_keyboard(
                    'backward',
                    f'{page}/{len(book[chapter])}',
                    'forward', chapter=chapter)
    if chapter in photo_db.keys() and page in photo_db[chapter].keys():
        photo = FSInputFile(photo_db[chapter][page])
        await message.delete()
        await message.answer_photo(photo=photo, caption=text,
                                    reply_markup=keyboard)
    else:
        await message.answer(text=text,
                                reply_markup=keyboard)
    await state.set_state(FSMReadSolve.read_text)
    #await state.update_data(user_db=users_db[message.from_user.id])

@router.callback_query(IsChapterCallbackData(), ~StateFilter(FSMReadSolve.solve_task))
async def process_forward_press(callback: CallbackQuery, state: FSMContext):
    chapter = int(callback.data[7:])
    users_db[callback.from_user.id]['chapter'] = chapter
    page = 1
    users_db[callback.from_user.id]['page'] = page
    text = book[chapter][page]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
                'backward',
                f'{page}/{len(book[chapter])}',
                'forward', chapter=chapter))
    await callback.answer()
    await state.set_state(FSMReadSolve.read_text)
    #await state.update_data(user_db=users_db[message.from_user.id])
    await _save_book_data(state, chapter=chapter)



# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == 'forward', ~StateFilter(FSMReadSolve.solve_task))
async def process_forward_press(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if users_db[callback.from_user.id]['page'] < len(book[users_db[callback.from_user.id]['chapter']]):
        users_db[callback.from_user.id]['page'] += 1
        page = users_db[callback.from_user.id]['page']
        chapter = users_db[callback.from_user.id]['chapter']
        text = book[chapter][page]

        keyboard = create_pagination_keyboard(
                            'backward',
                            f'{page}/{len(book[chapter])}',
                            'forward', chapter=chapter)
        if chapter in photo_db.keys() and page in photo_db[chapter].keys():

            await callback.message.delete()
            await callback.message.answer_photo(photo=FSInputFile(photo_db[chapter][page]),
                                                caption=text, reply_markup=keyboard)
            # else:
            #     print('1EDIT')
            #     await bot.edit_message_media(chat_id=callback.message.chat.id,
            #                                 message_id=callback.message.message_id,
            #                                 media=photo,
            #                                 reply_markup=keyboard)
        else:
            # if callback.message.photo == []:
                # print('DELETE')
            await callback.message.delete()
            await callback.message.answer(text=text,
                                            reply_markup=keyboard)
            # else:
            #     print('EDIT')
            #     await callback.message.edit_text(text=text,
            #                                     reply_markup=keyboard)
    await callback.answer()
    await state.set_state(FSMReadSolve.read_text)
    #await state.update_data(user_db=users_db[message.from_user.id])
    await _save_book_data(state, chapter=chapter, page=page)
    p = await state.get_data()
    print(p)

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == 'backward', ~StateFilter(FSMReadSolve.solve_task))
async def process_backward_press(callback: CallbackQuery, state: FSMContext):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        page = users_db[callback.from_user.id]['page']
        chapter = users_db[callback.from_user.id]['chapter']
        text = book[chapter][page]
        if chapter in photo_db.keys() and page in photo_db[chapter].keys():
            await callback.message.delete()
            photo=FSInputFile(photo_db[chapter][page])
            await callback.message.answer_photo(photo=photo,caption=text,
            reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{page}/{len(book[chapter])}',
                        'forward', chapter=users_db[callback.from_user.id]['chapter']))
        else:
            if callback.message.photo != []:
                await callback.message.delete()
                await callback.message.answer(text=text,
                    reply_markup=create_pagination_keyboard(
                            'backward',
                            f'{page}/{len(book[chapter])}',
                            'forward', chapter=users_db[callback.from_user.id]['chapter']))
            else:
                await callback.message.edit_text(
                    text=text,
                    reply_markup=create_pagination_keyboard(
                            'backward',
                            f'{page}/{len(book[chapter])}',
                            'forward', chapter=users_db[callback.from_user.id]['chapter']))
    #     page = users_db[callback.from_user.id]['page']
    #     chapter = users_db[callback.from_user.id]['chapter']
    #     text = book[chapter][page]
    #     await callback.message.edit_text(
    #             text=text,
    #             reply_markup=create_pagination_keyboard(
    #                 'backward',
    #                 f'{page}/{len(book[chapter])}',
    #                 'forward'))
    await callback.answer()
    await state.set_state(FSMReadSolve.read_text)
    #await state.update_data(user_db=users_db[message.from_user.id])
    await _save_book_data(state, chapter=chapter, page=page)

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData(), ~StateFilter(FSMReadSolve.solve_task))
async def process_bookmark_press(callback: CallbackQuery, state: FSMContext):
    text = book[users_db[callback.from_user.id]['chapter']][int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                    'forward', chapter=users_db[callback.from_user.id]['chapter']))
    await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
                text=LEXICON[callback.data],
                reply_markup=create_edit_keyboard(
                                *users_db[callback.from_user.id]["bookmarks"]))
    await callback.answer()

# @router.callback_query(IsTasksCallbackData())
# async def process_tasks_press(callback: CallbackQuery):
#     users_db[callback.from_user.id]['task'] = callback.data
#     await callback.message.answer(text=f'{LEXICON[callback.data]}',
#                                 reply_markup=create_tasks_keyboard('more_try', 'return'))
#     await callback.answer()

# @router.callback_query(Text(text='task'))
# async def process_task_press(callback: CallbackQuery):
#     origin_word = random.choice(task_db[users_db[callback.from_user.id]['chapter']][1])
#     caesar_key = random.randint(1, 10)
#     coded_word = caesar(caesar_key, origin_word)
#     users_db[callback.from_user.id]['bot_secret'] = coded_word
#     await callback.message.answer(
#                 text=f'расшифруй {origin_word} с ключом {caesar_key}',
#                 reply_markup=create_tasks_keyboard('more_try', 'return'))
#     await callback.answer()

@router.callback_query(F.data == 'more_try')
async def process_more_task_press(callback: CallbackQuery):
    origin_word = random.choice(task_db[users_db[callback.from_user.id]['chapter']][1])
    caesar_key = random.randint(1, 10)
    coded_word = caesar(caesar_key, origin_word)
    users_db[callback.from_user.id]['bot_secret'] = coded_word
    await callback.message.answer(
                text=f'расшифруй {origin_word} с ключом {caesar_key}',
                reply_markup=create_tasks_keyboard('more_try', 'return'))

    await callback.answer()


@router.callback_query(F.data == 'show_answer')
async def process_showanswer_press(callback: CallbackQuery):
    coded_word = users_db[callback.from_user.id]['bot_secret']
    await callback.message.answer(text=f'Правильный ответ {coded_word}',
                reply_markup=create_tasks_keyboard('return'))

    await callback.answer()

@router.callback_query(F.data == 'return')
async def process_edit_press(callback: CallbackQuery, state: FSMContext):
    text = book[users_db[callback.from_user.id]['chapter']][users_db[callback.from_user.id]['page']]
    page = users_db[callback.from_user.id]['page']
    chapter = users_db[callback.from_user.id]['chapter']
    text = book[chapter][page]
    if chapter in photo_db.keys() and page in photo_db[chapter].keys():
        await callback.message.delete()
        photo = FSInputFile(photo_db[chapter][page])
        await callback.message.answer_photo(photo=photo,caption=text,
        reply_markup=create_pagination_keyboard(
                    'backward',
                    f'{page}/{len(book[chapter])}',
                    'forward', chapter=users_db[callback.from_user.id]['chapter']))
    else:
        if callback.message.photo != []:
            await callback.message.delete()
            await callback.message.answer(text=text,
                reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{page}/{len(book[chapter])}',
                        'forward', chapter=users_db[callback.from_user.id]['chapter']))
        else:
            await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{page}/{len(book[chapter])}',
                        'forward', chapter=users_db[callback.from_user.id]['chapter']))
    await callback.answer()
    await state.set_state(FSMReadSolve.read_text)

# @router.callback_query(Text(text='code_cesar'))
# async def process_edit_press(callback: CallbackQuery):
#     await callback.message.answer(
#                 text=f'напишите сообщение', reply_markup=create_tasks_keyboard('more_try', 'return'))
#     await callback.answer()

# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


@router.message(Command(commands=['stats']), ~StateFilter(FSMReadSolve.solve_task))
async def process_stats(message: Message, state: FSMContext):

    report = f"Результаты для пользователя {message.from_user.username}: "
    report += await merge_to_report(message.from_user.username)
    await message.answer(text=report)

    await get_stats()
    buf.seek(0)
    res = BufferedInputFile(buf.getvalue(), "img1.png")
    await message.answer_photo(
        caption="Общая статистика\n\n"
                "Чтобы вернуться к чтению воспользуйтесь командой /chapters",
        photo=res
    )

# # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# # "отменить" во время работы со списком закладок (просмотр и редактирование)
# @router.callback_query(Text(text='cancel'))
# async def process_cancel_press(callback: CallbackQuery):
#     await callback.message.edit_text(text=LEXICON['cancel_text'])
#     await callback.answer()


# # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# # с закладкой из списка закладок к удалению
# @router.callback_query(IsDelBookmarkCallbackData())
# async def process_del_bookmark_press(callback: CallbackQuery):
#     users_db[callback.from_user.id]['bookmarks'].remove(
#                                                     int(callback.data[:-3]))
#     if users_db[callback.from_user.id]['bookmarks']:
#         await callback.message.edit_text(
#                     text=LEXICON['/bookmarks'],
#                     reply_markup=create_edit_keyboard(
#                             *users_db[callback.from_user.id]["bookmarks"]))
#     else:
#         await callback.message.edit_text(text=LEXICON['no_bookmarks'])
#     await callback.answer()


# from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton

# if users_db[callback.from_user.id]['mediagroup'] != '':
#     await callback.message.delete(message_id=users_db[callback.from_user.id]['mediagroup'])
#     #callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=users_db[callback.from_user.id]['mediagroup'])
#     users_db[callback.from_user.id]['mediagroup'] = ''

    #isinstance(photo_db[chapter][page], list):

# media_group = []
# for i, photo in enumerate(photo_db[chapter][page]):
#     media_group.append(InputMediaPhoto(type='photo', media=FSInputFile(photo), caption='' if i == 0 else ''))
# #await callback.message.delete()

            # sent_message = await callback.message.answer_media_group(media=media_group)
            # print(f'sent_message {int(sent_message[0].message_id)}')
            # users_db[callback.from_user.id]['mediagroup'] = int(sent_message[0].message_id)
            # file_info = await bot.send_photo(chat_id=callback.message.chat.id, photo=FSInputFile(photo_db[chapter][page]))
            # print('FILE_INFO', file_info)
            # photo=InputMediaPhoto(media=file_info.photo[-1].file_id, caption=text)
            # print(callback.message)
            # print(callback.message.photo )
            #if callback.message.photo == None:
                #print('1DELETE')


# # Этот хэндлер будет срабатывать на команду "/bookmarks"
# # и отправлять пользователю список сохраненных закладок,
# # если они есть или сообщение о том, что закладок нет
# @router.message(Command(commands='bookmarks'))
# async def process_bookmarks_command(message: Message):
#     if users_db[message.from_user.id]["bookmarks"]:
#         await message.answer(
#             text=LEXICON[message.text],
#             reply_markup=create_bookmarks_keyboard(
#                 *users_db[message.from_user.id]["bookmarks"]))
#     else:
#         await message.answer(text=LEXICON['no_bookmarks'])