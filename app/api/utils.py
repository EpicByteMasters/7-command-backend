from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.validators import check_task_exists_in_ipr

from app.crud import (
    competency_ipr_crud,
    education_task_crud,
    file_crud,
    task_crud,
    user_crud,
    ipr_crud,
)
from app.models import Ipr
from app.schemas.task import FileCreate, TaskCreate, EduTaskCreate


async def add_competencies(
    new_draft_dict: dict, ipr_id: int, session: AsyncSession
) -> dict:
    """
    Вспомогательная функция для создания связи между ИПР и компетенциями
    при сохранении черновика ИПР.
    """
    new_competencies = new_draft_dict.pop("competency", None)
    if new_competencies is None:
        return new_draft_dict
    await competency_ipr_crud.update_competencies(ipr_id,
                                                  new_competencies,
                                                  session)

    return new_draft_dict


async def create_tasks(new_draft_dict: dict, ipr_id, session) -> dict:
    """
    Вспомогательная функци создания заданий для ИПР и связи их с соответсвующим
    ИПР при сохранении черновика ИПР.
    """
    tasks = new_draft_dict.pop("tasks")
    if tasks is None:
        return new_draft_dict
    for task in tasks:
        educations = task.pop("educations")
        task["ipr_id"] = ipr_id
        new_task = TaskCreate.parse_obj(task)
        task = await task_crud.create(new_task, session)
        task_id = task.id
        if educations is not None:
            for education_id in educations:
                education_task = {"task_id": task_id, "education_id": education_id}
                eduSchema = EduTaskCreate.parse_obj(education_task)
                await education_task_crud.create(eduSchema, session)
    return new_draft_dict


async def update_tasks(draft_dict: dict, ipr_id, session) -> dict:
    """
    Вспомогательная функци создания заданий для ИПР и связи их с соответсвующим
    ИПР при сохранении черновика ИПР или при редактировании ИПР.
    """
    tasks = draft_dict.pop("tasks", None)
    if tasks is None:
        return draft_dict
    for task_in in tasks:
        task_id = task_in.pop("id", None)
        educations = task_in.pop("education", None)
        if task_id is None:
            task_in["ipr_id"] = ipr_id
            new_task = TaskCreate.parse_obj(task_in)
            task = await task_crud.create(new_task, session)
        else:
            old_task = await task_crud.get(task_id, session)
            updated_data = TaskCreate.parse_obj(task_in)
            task = await task_crud.update(updated_data, old_task, session)

        if educations is None:
            return draft_dict
        for education_id in educations:
            education_task = {
                "task_id": task.id,
                "education_id": education_id
            }
            education_task = EduTaskCreate.parse_obj(education_task)
            await education_task_crud.create(education_task, session)
    return draft_dict


async def update_task_employee(tasks, ipr, session):
    for task in tasks:
        task_id = task.get("id")
        files = task.pop("file", None)
        db_task = await check_task_exists_in_ipr(task_id, ipr.id, session)
        task = TaskCreate.parse_obj(task)
        if files is not None:
            for file in files:
                file["ipr_id"] = ipr.id
                file = FileCreate.parse_obj(file)
                await file_crud.create(file, session)
        await task_crud.update(task, db_task, session)


async def demote_user_as_mentor(ipr_id: int,
                                old_mentor_id: int,
                                session: AsyncSession):
    query = (
        select(Ipr).where(
            Ipr.id != ipr_id,
            Ipr.ipr_status_id == "IN_PROGRESS",
            Ipr.mentor_id == old_mentor_id
        )
    )
    iprs = await session.execute(query)
    iprs = iprs.scalar()
    if iprs is not None:
        return
    old_mentor = await user_crud.get(old_mentor_id, session)
    old_mentor.is_mentor = False
    session.add(old_mentor)
    await session.commit()
    await session.refresh(old_mentor)
