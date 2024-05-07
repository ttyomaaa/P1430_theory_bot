from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from lexicon.lexicon import LEXICON_TASKS
from database.database import  users_db


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and 'del'         \
            in callback.data and callback.data[:-3].isdigit()


class IsChapterCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and 'chapter'         \
            in callback.data and callback.data[7:].isdigit()

class IsTasksCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and callback.data in LEXICON_TASKS[users_db[callback.from_user.id]['chapter']]