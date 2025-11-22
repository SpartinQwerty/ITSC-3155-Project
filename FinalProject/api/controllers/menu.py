from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import menu as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_menu = model.Menu(
        dish=request.dish,
        ingredients=request.ingredients,
        price=request.price,
        calories=request.calories,
        category=request.category,
        description=request.description,
        is_vegetarian=request.is_vegetarian
    )
    try:
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_menu

def read_all(db: Session):
    try:
        return db.query(model.Menu).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, menu_id: int):
    try:
        menu_item = db.query(model.Menu).filter(model.Menu.id == menu_id).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return menu_item

def update(db: Session, menu_id: int, request):
    try:
        menu_item = db.query(model.Menu).filter(model.Menu.id == menu_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return menu_item.first()

def delete(db: Session, menu_id: int):
    try:
        menu_item = db.query(model.Menu).filter(model.Menu.id == menu_id)
        if not menu_item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        menu_item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
