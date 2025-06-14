
from pydantic import BaseModel, Field
from typing import Any

class MessageResponse(BaseModel):
    message: Any = Field(...)
