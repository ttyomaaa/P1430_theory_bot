from aiogram import Router
from aiogram.types import Message
from database.database import users_db, tasks_db
router: Router = Router()
from services.code_casar import caesar_decod, caesar, atbash
from services.code_slogan import encrypt, losung
from keyboards.tasks_kb import create_tasks_keyboard

def _check_answer(word_to_check: str, true_word: str) -> bool:
    if true_word.lower() == word_to_check.lower():
        return True
    else:
        return False

# Этот хэндлер будет реагировать на любые сообщения пользователя
# @router.message()
# async def send_echo(message: Message):
#     if users_db[message.from_user.id]['task'] != '':
#         if users_db[message.from_user.id]['task'] in tasks_db['with_answer']:
#             if _check_answer(message.text, users_db[message.from_user.id]['bot_secret']):
#                 await message.answer(f'здорово! {message.text} это правильный ответ',
#                 reply_markup=create_tasks_keyboard('return'))
#                 users_db[message.from_user.id]['bot_secret'] = ''
#                 users_db[message.from_user.id]['task'] = ''
#             else:
#                 await message.answer(text=f'очень жаль, {message.text} это не правильный ответ',
#                                         reply_markup=create_tasks_keyboard('return', 'show_answer'))
#         else:
#             if users_db[message.from_user.id]['task'] == 'code_caesar_message':
#                 key, text = tuple(message.text.split())
#                 key = int(key)
#                 users_db[message.from_user.id]['task'] = ''
#                 await message.answer(f'{caesar(key, text)} \nшифр Цезаря с ключом {key}',
#                                 reply_markup=create_tasks_keyboard('return'))
#             elif users_db[message.from_user.id]['task'] == 'code_atbash_message':
#                 await message.answer(text=f'{atbash(message.text)}\nATBASH шифр для вашего сообщения')
#                 users_db[message.from_user.id]['task'] = ''
#             elif users_db[message.from_user.id]['task'] == 'code_slogan_message':
#                 await message.answer(text=f'{encrypt(message.text)}\nЛозунговый шифр для вашего сообщения\n'
#                                             f'{losung(message.text)} алфавит для вашего сообщения')
#                 users_db[message.from_user.id]['task'] = ''
#
#     else:
#         await message.answer(text='я не понимаю')
    # if users_db[message.from_user.id]['bot_secret'] != '':
    #     if message.text == users_db[message.from_user.id]['bot_secret']:
    #         await message.answer(f'здорово! {message.text} это правильный ответ',
    #         reply_markup=create_tasks_keyboard('more_try', 'return'))
    #         users_db[message.from_user.id]['bot_secret'] = ''
    #     else:
    #         await message.answer(f'очень жаль, {message.text} это не правильный ответ',
    #         reply_markup=create_tasks_keyboard('more_try', 'return'))
    # else:
    #     await message.answer(f'{caesar(5, message.text)} \nшифр Цезаря с ключом 5',
    #     reply_markup=create_tasks_keyboard('more_try', 'return'))