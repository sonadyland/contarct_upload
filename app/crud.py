from sqlalchemy.orm import Session
from .models import Contract, DefaultContract

def upsert_contract(db: Session, order_no: str, content: dict) -> tuple[Contract, bool]:
    obj = db.query(Contract).filter(Contract.order_no == order_no).first()
    if obj:
        obj.content = content
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj, True
    obj = Contract(order_no=order_no, content=content)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj, False

def get_contract_by_order_no(db: Session, order_no: str) -> Contract | None:
    return db.query(Contract).filter(Contract.order_no == order_no).first()

def set_default_contract(db: Session, content: dict) -> DefaultContract:
    db.query(DefaultContract).filter(DefaultContract.is_active == True).update({DefaultContract.is_active: False})
    obj = DefaultContract(content=content, is_active=True)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_active_default_contract(db: Session) -> DefaultContract | None:
    return db.query(DefaultContract).filter(DefaultContract.is_active == True).order_by(DefaultContract.id.desc()).first()