from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    competency_ipr_crud,
    education_task_crud,
    ipr_crud,
    task_crud,
)
from app.schemas.ipr import CompetencyIprCreate
from app.schemas.task import TaskCreate, EduTaskCreate


async def add_competencies(
    new_draft_dict: dict, ipr_id: int, session: AsyncSession
) -> dict:
    """
    Вспомогательная функция для создания связи между ИПР и компетенциями
    при сохранении черновика ИПР.
    """
    await competency_ipr_crud.remove_all_competencies_from_ipr(ipr_id, session)
    competencies = new_draft_dict.pop("competency")
    if competencies is None:
        return new_draft_dict
    for competency in competencies:
        connection = {"competency": competency, "ipr_id": ipr_id}
        schema = CompetencyIprCreate.parse_obj(connection)
        await competency_ipr_crud.create(schema, session)
    return new_draft_dict


async def update_tasks(draft_dict: dict, ipr_id, session) -> dict:
    """
    Вспомогательная функци создания заданий для ИПР и связи их с соответсвующим
    ИПР при сохранении черновика ИПР или при редактировании ИПР.
    """
    await ipr_crud.remove_all_tasks_from_ipr(ipr_id, session)
    tasks = draft_dict.pop("tasks")
    if tasks is None:
        return draft_dict
    for task_in in tasks:
        educations = task_in.pop("educations")
        task_in["ipr_id"] = ipr_id
        new_task = TaskCreate.parse_obj(task_in)
        task = await task_crud.create(new_task, session)

        if educations is not None:
            for education_id in educations:
                education_task = {"task_id": task.id, "education_id": education_id}
                education_task = EduTaskCreate.parse_obj(education_task)
                await education_task_crud.create(education_task, session)
    return draft_dict
