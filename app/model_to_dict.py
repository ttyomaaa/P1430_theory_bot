from datetime import timedelta


def question_answers_to_dict(question, answers):
    return {
        'id_question': question.id_question,
        'id_chapter': question.id_chapter,
        'q_number': question.q_number,
        'question': question.question,
        'q_file': question.q_file,
        'answers': [
            {
                'id_answer': answer.id_answer,
                'a_number': answer.a_number,
                'answer': answer.answer,
                'is_correct': answer.is_correct
            }
            for answer in answers
        ]
    }


def forms_data_to_dict(forms_data):
    return {
        'id_forms_data': forms_data.id_forms_data
    }


def results_to_dict(results):
    return {
        'id_forms_data': results.id_forms_data,
        'result': results.result,
        'created_date': (results.created_date+timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
        'id_chapter': results.id_chapter
    }


def reports_to_dict(reports):
    return {
        'id_forms_data': reports.id_forms_data,
        'user_tg_id': reports.user_tg_id,
        'id_tg': reports.id_tg
    }

def id_to_dict(reports):
    return {
        'id_tg': reports.id_tg
    }
