from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class OmniReport(BaseModel):
    meta: Dict[str, Any] = Field(..., description="Analiz meta verileri")
    scores: Dict[str, float] = Field(..., description="8 eksende puanlar (0-100)")
    details: Dict[str, Any] = Field(..., description="Detaylı ham veriler")
    status: str = Field("success", description="success veya error")
    error_msg: Optional[str] = None
