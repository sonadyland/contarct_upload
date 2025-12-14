from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, func
from .database import Base

class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(255), nullable=False, unique=True, index=True)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class DefaultContract(Base):
    __tablename__ = "default_contracts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)