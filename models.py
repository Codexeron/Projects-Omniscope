from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class PerformanceDetail(BaseModel):
    ttfb_seconds: float = Field(..., description="Time To First Byte")
    total_size_kb: float = Field(..., description="Toplam sayfa boyutu")
    is_gzip: bool = Field(False, description="Gzip sıkıştırması var mı")

class SecurityDetail(BaseModel):
    ssl_valid: bool
    ssl_issuer: Optional[str] = None
    has_hsts: bool
    has_xframe: bool
    has_xcontent_type: bool

class SeoDetail(BaseModel):
    has_title: bool
    title_length: int
    has_meta_description: bool
    meta_description_length: int
    has_h1: bool
    h1_count: int

class OmniReport(BaseModel):
    meta: Dict[str, Any] = Field(..., description="Analiz meta verileri")
    scores: Dict[str, float] = Field(..., description="6 eksende puanlar (0-100)")
    details: Dict[str, Any] = Field(..., description="Detaylı ham veriler")
    status: str = Field("success", description="success veya error")
    error_msg: Optional[str] = None
