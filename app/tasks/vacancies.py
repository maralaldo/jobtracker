from app.core.celery import celery_app


@celery_app.task(name="app.tasks.parse_vacancies")
def parse_vacancies():
    import asyncio
    from app.core.database import AsyncSessionLocal
    from app.crud import filters as filters_crud
    from app.crud import vacancies as vacancy_crud
    from app.crud import users as user_crud
    from app.parsers.hh import fetch_vacancies_for_filter
    from app.tasks.notifications import send_message_async
    from app.schemas.vacancy import VacancyCreate as VacancyCreateSchema

    async def _main():
        async with AsyncSessionLocal() as db:
            filters = await filters_crud.get_all_filters(db)
            # map user_id -> list[vacancy_dict]
            user_new = {}

            for f in filters:
                items = fetch_vacancies_for_filter(f, pages=1)
                for it in items:
                    if not it.get("url"):
                        continue
                    exists = await vacancy_crud.get_vacancy_by_url(db, it["url"])
                    if exists:
                        continue
                    # create vacancy using your VacancyCreate schema shape
                    vac_in = VacancyCreateSchema(
                        title=it["title"] or "No title",
                        company=it.get("company") or "",
                        location=it.get("location"),
                        salary=None,
                        url=it["url"],
                        source=it.get("source") or "hh.ru",
                    )
                    await vacancy_crud.create_vacancy(db, vac_in)
                    user_new.setdefault(f.user_id, []).append(it)

            for user_id, vacs in user_new.items():
                user = await user_crud.get_user(db, user_id)
                if not user or not user.telegram_id:
                    continue
                text_lines = []
                for v in vacs:
                    text_lines.append(f"{v.get('title')} — {v.get('company')}\n{v.get('url')}")
                text = "New vacancies matching your filters:\n\n" + "\n\n".join(text_lines)
                await send_message_async(user.telegram_id, text)

    asyncio.run(_main())
