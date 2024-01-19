from typing import Optional

from pydantic import AnyUrl, BaseModel


class EducationsDB(BaseModel):
    name: Optional[str]
    url: Optional[AnyUrl]
    status: Optional[str]