from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    id: int
    name: str

class CategoryCreate(BaseModel):
    name: str = Field(...,max_length=50)

class CategoryUpdate(CategoryCreate):
    pass

class CategoryDelete(BaseModel):
    id: int = Field(...)
