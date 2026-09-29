from pydantic import BaseModel, Field


class UserInput(BaseModel):
    user_id: str
    username: str
    age: int = Field(gt=0, le=120)
    weight: float = Field(gt=0)
    goal: str
    intensity: str


class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str