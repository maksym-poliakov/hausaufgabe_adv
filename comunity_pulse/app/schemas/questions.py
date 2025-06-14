from pydantic import BaseModel, Field
from app.schemas.categories import CategoryBase

class QuestionCreate(BaseModel):
    text: str = Field(...,description="Text of the question", max_length=140)
    category: str = Field(...,max_length=50)


class QuestionDelete(BaseModel):
    question_id: int = Field(...)


class QuestionUpdate(QuestionCreate):
    pass

class QuestionSchema(BaseModel):
    id: int
    text: str
    category: str


class QuestionResponse(QuestionSchema):
    pass



