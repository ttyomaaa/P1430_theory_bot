from app.decorators import enter_session
from app.model_to_dict import question_answers_to_dict, results_to_dict, reports_to_dict, id_to_dict
from app.repositories.repository import FormRepository
from typing import Optional


@enter_session
async def get_reports_user(username="ttyomaaa", **kwargs):
    session = kwargs.pop('session')
    rep = FormRepository(session)
    try:
        reports = await rep.get_results_by_user(username=username)
        result = [
            reports_to_dict(report)
            for report in reports
        ]
        return result
    except Exception as e:
        print(e)
        print('При получении отчета по пользователм возникла ошибка')


@enter_session
async def get_questions_by_chapter(id_chapter, **kwargs) -> Optional[list]:
    session = kwargs.pop('session')
    rep = FormRepository(session)
    try:
        questions = await rep.get_questions_by_chapter(id_chapter)
        result = [
            question_answers_to_dict(question, await rep.get_answers(id_question=question.id_question))
            for question in questions
        ]
        return result if result else None
    except Exception as e:
        print(e)
        print('Ошибка при получении вопросов и ответов из бд')
        return None


@enter_session
async def get_results(**kwargs) -> Optional[list]:
    session = kwargs.pop('session')
    rep = FormRepository(session)
    try:
        forms = await rep.get_results()
        result = [
            results_to_dict(form)
            for form in forms
        ]
        return result if result else None
    except Exception as e:
        print(e)
        print('Ошибка при получении результатов из бд')
        return None


@enter_session
async def get_results_by_chapter(id_chapter, **kwargs):
    session = kwargs.pop('session')
    rep = FormRepository(session)
    try:
        forms = await rep.get_results_by_chapter(id_chapter)
        result = [
            results_to_dict(form)
            for form in forms
        ]
        return result if result else None
    except Exception as e:
        print(e)
        print('Ошибка при получении результатов из бд')
        return None


@enter_session
async def get_users(**kwargs):
    session = kwargs.pop('session')
    rep = FormRepository(session)
    try:
        reports = await rep.get_all_forms()
        result = [
            id_to_dict(report)
            for report in reports
        ]
        return result
    except Exception as e:
        print(e)
        print('При получении отчета по пользователям возникла ошибка')
