from app.decorators import enter_session
from app.repositories.repository import FormRepository
from app.model_to_dict import forms_data_to_dict

@enter_session
async def add_questions_and_answers(form: dict, **kwargs):
    session = kwargs.pop('session')
    rep = FormRepository(session)
    try:
        for question_data, answers in form.items():
            try:
                question_data[3]
            except IndexError:
                res = await rep.add_question(id_chapter=question_data[0], q_number=question_data[1],
                                             question=question_data[2])
            else:
                res = await rep.add_question(id_chapter=question_data[0], q_number=question_data[1],
                                             question=question_data[2], q_file=question_data[3])
            for a_number, answer, is_correct in answers:
                await rep.add_answer(id_question=res.id_question, a_number=a_number, answer=answer, is_correct=is_correct)

    except Exception as e:
        print(e)
        print('Ошибка при записи вопросов и ответов в бд')


@enter_session
async def create_forms_data(**kwargs):
    session = kwargs.pop('session')
    rep = FormRepository(session)
    try:
        forms_data = await rep.create_forms_data(**kwargs)
        return forms_data_to_dict(forms_data)
    except Exception as e:
        print(e)
        print('Ошибка при создании анкеты')


@enter_session
async def create_form(result: list, id_forms_data, user_tg_id, id_tg, **kwargs):
    session = kwargs.pop('session')
    rep = FormRepository(session)

    try:
        for res in result:
            for id_question, id_answer in res.items():
                await rep.create_form(
                    user_tg_id=user_tg_id,
                    id_forms_data=id_forms_data,
                    id_question=id_question,
                    id_answer=id_answer,
                    id_tg=id_tg
                )

    except Exception as e:
        print(e)
        print('Ошибка при записи ответов анкеты')


@enter_session
async def update_result_and_chapter(**kwargs):
    session = kwargs.pop('session')
    rep = FormRepository(session)
    try:
        await rep.update_result(id_forms_data=kwargs['id_forms_data'], result=kwargs['result'], id_chapter=kwargs['id_chapter'], created_date=kwargs['created_date'])
    except Exception as e:
        print(e)
        print('ошибка при обновлении результата')
