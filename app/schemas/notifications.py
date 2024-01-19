from pydantic import AnyUrl, BaseModel, constr


class NotificationGet(BaseModel):
    id: int
    idUrl: AnyUrl
    task_id: int
    message: constr(max_length=128)
