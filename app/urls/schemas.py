from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class ShortUrlCreate(BaseModel):
    url: HttpUrl


class ShortUrlRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    short_code: str
    target_url: str
    number_of_creations: int
    created_at: datetime
    last_created_at: datetime
