from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_CHAPTERS

# Функция, генерирующая клавиатуру для страницы книги
def create_chapters_keyboard() -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
                    text=LEXICON_CHAPTERS[button], callback_data=button)
                    for button in LEXICON_CHAPTERS.keys()], width = 1)
    return kb_builder.as_markup()