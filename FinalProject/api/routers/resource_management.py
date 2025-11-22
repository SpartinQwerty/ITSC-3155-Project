from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import resource_management as controller
from ..schemas import resource_management as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Resources"],
    prefix="/resources"
)

@router.post("/", response_model=schema.ResourceManagementRead)
def create_resource(request: schema.ResourceManagementCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

@router.get("/", response_model=list[schema.ResourceManagementRead])
def get_resources(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.ResourceManagementRead)
def get_resource(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)

@router.put("/{item_id}", response_model=schema.ResourceManagementRead)
def update_resource(item_id: int, request: schema.ResourceManagementUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)

@router.delete("/{item_id}")
def delete_resource(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)