from app.core.celery import celery_app


@celery_app.task
def parse_vacancies():
    return "Vacancies parsed successfully!"
