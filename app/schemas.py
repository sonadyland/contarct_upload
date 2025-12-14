from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Any, Dict

class ContractCreate(BaseModel):
    order_no: str
    content: Dict[str, Any]

class ContractOut(BaseModel):
    id: int
    order_no: str
    content: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DefaultCreate(BaseModel):
    content: Dict[str, Any]

class DefaultOut(BaseModel):
    id: int
    content: Dict[str, Any]
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ContractUpsertResponse(BaseModel):
    data: ContractOut
    message: str