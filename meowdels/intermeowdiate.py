from pydantic import BaseModel
from typing import Any

class LayoutBlock(BaseModel):
    page: int
    text: str
    font_size: float
    all_caps: bool
    has_bold: bool
    bbox: list[float, float, float, float]

    x0: float
    x1: float
    y1: float
    y0: float

class TableData(BaseModel):
    page: int
    rows: list[list[Any]]

class DetectedHeader(BaseModel):
    text: str
    page: int
    confidence: float

class IntermeowdiateRep(BaseModel):
    raw_text: str
    layout_blocks: list[LayoutBlock]
    tables: list[TableData]
    detected_headers: list[DetectedHeader]
    