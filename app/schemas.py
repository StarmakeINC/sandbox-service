from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date

class ScenarioCreate(BaseModel):
    text: str
    temp_id: Optional[str] = None

class ScenarioRequest(BaseModel):
    scenario_text: str

class ScenarioResponse(ScenarioCreate):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class UserMessage(BaseModel):
    user_message: str