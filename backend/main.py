from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Ambient Bridge")


class DraftIn(BaseModel):
    source: str = "local-ambient-scribe"
    title: str
    content: str


class Draft(DraftIn):
    id: str
    created_at: str
    transferred: bool = False


DRAFTS: List[Draft] = [
    Draft(
        id=str(uuid4()),
        source="local-ambient-scribe (demo)",
        title="Sample Draft: Progress Entry",
        content="### History & Progress\n- Client reports marked improvement.\n- Follow-up scheduled in 14 days.",
        created_at=datetime.now().strftime("%H:%M"),
    )
]


@app.get("/api/drafts", response_model=List[Draft])
def list_drafts():
    return DRAFTS


@app.post("/api/drafts", response_model=Draft)
def create_draft(item: DraftIn):
    draft = Draft(
        id=str(uuid4()),
        created_at=datetime.now().strftime("%H:%M"),
        **item.model_dump(),
    )
    DRAFTS.insert(0, draft)
    return draft


@app.post("/api/drafts/{draft_id}/transferred")
def mark_transferred(draft_id: str):
    for d in DRAFTS:
        if d.id == draft_id:
            d.transferred = True
            return {"status": "ok"}
    raise HTTPException(status_code=404, detail="Draft not found")


app.mount("/", StaticFiles(directory="static", html=True), name="static")
