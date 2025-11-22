from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import menu as controller
from ..schemas import menu as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Menu'],
    prefix="/menu"
)


@router.post("/", response_model=schema.Menu)
def create(request: schema.MenuCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Menu])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{menu_id}", response_model=schema.Menu)
def read_one(menu_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, menu_id=menu_id)


@router.put("/{menu_id}", response_model=schema.Menu)
def update(menu_id: int, request: schema.MenuUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, menu_id=menu_id, request=request)


@router.delete("/{menu_id}", status_code=204)
def delete(menu_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, menu_id=menu_id)