from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    competency_crud,
    competency_ipr_crud,
    education_crud,
    education_task_crud,
    goal_crud,
    specialty_crud,
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
    competencies = new_draft_dict.pop("competence")
    if competencies is None:
        return new_draft_dict
    for comp in competencies:
        comp_id = await competency_crud.get_id_by_name(comp, session)
        connection = {"competency_id": comp_id, "ipr_id": ipr_id}
        schema = CompetencyIprCreate.parse_obj(connection)
        await competency_ipr_crud.create(schema, session)
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
            for education in educations:
                education_id = await education_crud.get_id_by_name(
                    education["name"], session
                )
                education_task = {"task_id": task_id, "education_id": education_id}
                eduSchema = EduTaskCreate.parse_obj(education_task)
                await education_task_crud.create(eduSchema, session)
    return new_draft_dict


async def get_foreign_keys_by_names(new_draft_dict: dict, session) -> dict:
    """
    Вспомогательная функция для получения внешних ключей по именам
    предоставленных в запросе.
    """
    goal = new_draft_dict["goal"]
    if goal is not None:
        goal_id = await goal_crud.get_id_by_name(goal, session)
        new_draft_dict["goal_id"] = goal_id
    specialty = new_draft_dict["specialty"]
    if specialty is not None:
        specialty_id = await specialty_crud.get_id_by_name(specialty, session)
        new_draft_dict["specialty_id"] = specialty_id
    return new_draft_dict
