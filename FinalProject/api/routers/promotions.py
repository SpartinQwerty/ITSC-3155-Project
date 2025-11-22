from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import promotions as controller
from ..schemas import promotions as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Promotions"],
    prefix="/promotions"
)

@router.post("/", response_model=schema.PromotionRead)
def create_promotion(request: schema.PromotionCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

@router.get("/", response_model=list[schema.PromotionRead])
def get_promotions(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.PromotionRead)
def get_promotion(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id)

@router.put("/{item_id}", response_model=schema.PromotionRead)
def update_promotion(item_id: int, request: schema.PromotionUpdate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, request)

@router.put("/orders/{order_id}/apply-promo")
def apply_promo(order_id: int, promo_code: str, db: Session = Depends(get_db)):
    return controller.apply_promo(db, order_id, promo_code)

@router.delete("/{item_id}")
def delete_promotion(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, item_id)