from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 唯一的 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contracts", response_model=schemas.ContractUpsertResponse)
def upload_contract(payload: schemas.ContractCreate, db: Session = Depends(get_db)):
    obj, updated = crud.upsert_contract(db, order_no=payload.order_no, content=payload.content)
    return {"data": obj, "message": "覆盖成功" if updated else "创建成功"}

@app.get("/contracts/{order_no}", response_model=schemas.ContractOut)
def get_contract(order_no: str, db: Session = Depends(get_db)):
    obj = crud.get_contract_by_order_no(db, order_no=order_no)
    if not obj:
        raise HTTPException(status_code=404, detail="Contract not found")
    return obj

@app.post("/default", response_model=schemas.DefaultOut)
def upload_default(payload: schemas.DefaultCreate, db: Session = Depends(get_db)):
    obj = crud.set_default_contract(db, content=payload.content)
    return obj

@app.get("/default", response_model=schemas.DefaultOut)
def get_default(db: Session = Depends(get_db)):
    obj = crud.get_active_default_contract(db)
    if not obj:
        raise HTTPException(status_code=404, detail="Default contract not found")
    return obj