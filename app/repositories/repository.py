from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Any
from app.models.models import Question, Answer, Form, FormsData


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _create(self, model_table, **kwargs):
        instance = model_table(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def _update(self, model_table, condition, **kwargs):
        stmt = update(model_table).values(**kwargs).where(condition)
        await self.session.execute(stmt)

    async def _all(self, model_table):
        stmt = select(model_table)
        entities = await self.session.execute(stmt)
        return entities.scalars()

    async def _filter(self, model_tabel, condition):
        stmt = select(model_tabel).filter(condition)
        entities = await self.session.execute(stmt)
        return entities.scalars()


class FormRepository(BaseRepository):
    async def _get_entity_by_fields(self, model_table: Any, **kwargs) -> Any:
        condition = [
            getattr(model_table, key).ilike(f'{value}')
            for key, value in kwargs.items()
        ]
        stmt = select(model_table).where(*condition)
        entity = await self.session.execute(stmt)
        return entity.scalar()

    async def _get_entity_by_id(self, model_table: Any, key, value):
        stmt = select(model_table).where(getattr(model_table, key) == value)
        entity = await self.session.execute(stmt)
        return entity.scalars()

    async def add_question(self, **kwargs) -> int:
        question = await self._create(Question, **kwargs)
        return question

    async def add_answer(self, **kwargs) -> int:
        answer = await self._create(Answer, **kwargs)
        return answer

    async def get_questions(self):
        questions = await self._all(Question)
        return questions

    async def get_answers(self, id_question):
        condition = Answer.id_question == id_question
        answers = await self._filter(Answer, condition)
        return answers

    async def get_results(self):
        forms_data = await self._all(FormsData)
        return forms_data

    async def get_all_forms(self):
        forms_data = await self._all(Form)
        return forms_data

    async def get_results_by_user(self, username):
        forms_data = await self._get_entity_by_id(Form, key='user_tg_id', value=username)
        await self.session.flush()
        return forms_data

    async def get_results_by_chapter(self, id_chapter: int):
        forms_data = await self._get_entity_by_id(FormsData, key='id_chapter', value=id_chapter)
        await self.session.flush()
        return forms_data if forms_data else None

    async def get_questions_by_chapter(self, id_chapter: int):
        questions = await self._get_entity_by_id(Question, key='id_chapter', value=id_chapter)
        await self.session.flush()
        return questions if questions else None

    async def create_form(self, id_forms_data, **kwargs):
        form = await self._create(Form, id_forms_data=id_forms_data, **kwargs)
        return form

    async def create_forms_data(self, **kwargs):
        forms_data = await self._create(FormsData, **kwargs)
        return forms_data

    async def update_result(self, id_forms_data, **kwargs):
        condition = FormsData.id_forms_data == id_forms_data
        await self._update(FormsData, condition, **kwargs)
