import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .controllers import payments
from .routers import index as indexRoute
from .models import model_loader
from .schemas import payments
from .dependencies.config import conf
from .dependencies.database import engine, get_db


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)

@app.post("/payments/", response_model=payments, tags=["Payments"])
def create_payment(payment: payments.PaymentsCreate, db: Session = Depends(get_db)):
    return payment.create(db=db, payment=payment)

@app.get("/payments/", response_model=list[payments], tags=["Payments"])
def read_all_payments(db: Session = Depends(get_db)):
    return payments.read_all_payments(db=db)

@app.get("/payments/", response_model=payments, tags=["Payments"])
def read_one_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = payments.read_payment(payment_id=payment_id, db=db)

@app.put("/payments/", response_model=payments, tags=["Payments"])
def update_payment(payment_id: int, payment: payments.PaymentsUpdate, db: Session = Depends(get_db)):
    payment_db = payments.read_payment(db,payment_id=payment_id)
    if payment_db is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment.update(db=db, payment=payment, payment_id=payment_id)

@app.delete("/payments/", response_model=payments, tags=["Payments"])
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = payments.read_payment(payment_id=payment_id, db=db)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment.delete(db=db, payment_id=payment_id)

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)