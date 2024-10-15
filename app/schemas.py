from pydantic import BaseModel

class UserInput(BaseModel):
    message: str