from bson import ObjectId
from fastapi import APIRouter, Depends, Header, HTTPException

from app.auth import create_jwt, verify_jwt
from app.db import get_collection
from app.kafka_manager import kafka_manager
from app.models import CameraCreate, UserCreate, UserLogin

router = APIRouter()
users_col = get_collection("users")
cameras_col = get_collection("cameras")


def get_current_user(x_access_token: str = Header(...)):
    user = verify_jwt(x_access_token)
    if not user:
        raise HTTPException(status_code=401, detail="invalid token")
    return user


@router.get("/", tags=["root"])
async def root():
    return {"message": "fastapi + kafka + mongodb is running successfully"}


@router.post("/register", tags=["Auth"])
def register_user(user: UserCreate):
    if users_col.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="user alreay exists")
    users_col.insert_one(
        {"_id": str(ObjectId()), "username": user.username, "password": user.password}
    )
    token = create_jwt(user.username)
    return {"token": token}


@router.post("/login", tags=["Auth"])
def login(user: UserLogin):
    db_user = users_col.find_one({"username": user.username})
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = create_jwt(user.username)
    return {"token": token}


@router.post("/cameras", tags=["Cameras"])
async def create_camera(
    camera: CameraCreate, username: str = Depends(get_current_user)
):
    camera_doc = {
        "_id": str(ObjectId()),
        "name": camera.name,
        "location": camera.location,
        "owner": username,
    }
    cameras_col.insert_one(camera_doc)
    await kafka_manager.send_event({"events": "camera_created", "data": camera_doc})
    return {"message": "camera created", "camera": camera_doc}


@router.get("/list_cameras", tags=["Cameras"])
def list_cameras(username: str = Depends(get_current_user)):
    return list(
        cameras_col.find({"owner": username}, {"_id": 1, "name": 1, "location": 1})
    )


@router.delete('/cameras/{camera_id}', tags=['Cameras'])
async def  delete_camera(camera_id: str, username: str = Depends(get_current_user)):
    camera = cameras_col.find_one({"_id": camera_id, "owner": username})
    if not camera:
        raise HTTPException(status_code=404, detail="camera not found")
    cameras_col.delete_one({"_id": camera_id})
    await kafka_manager.send_event({"event": "camera_deleted", "data": {"_id": camera_id}})
    return {"message": "camera deleted"}