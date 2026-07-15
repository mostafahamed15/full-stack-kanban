from pydantic import BaseModel
from typing import Dict, List, Optional


class Card(BaseModel):
    id: str
    title: str
    details: str


class Column(BaseModel):
    id: str
    title: str
    cardIds: List[str]


class BoardData(BaseModel):
    columns: List[Column]
    cards: Dict[str, Card]


class AiBoardUpdate(BaseModel):
    columns: List[Column]
    cards: Dict[str, Card]


class AiChatResponse(BaseModel):
    message: str
    applied: bool
    board: Optional[BoardData] = None
