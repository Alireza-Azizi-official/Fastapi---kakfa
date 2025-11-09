from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class CameraBase(BaseModel):
    name: str
    location: str


class CameraCreate(CameraBase):
    pass


class Camera(CameraBase):
    id: str = Field(..., alias="_id")

    class Confi:
        orm_model = True
