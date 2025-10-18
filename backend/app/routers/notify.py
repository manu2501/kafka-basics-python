import asyncio
import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from jose import jwt, JWTError

from sqlalchemy.orm import Session
from ..deps import get_current_user, get_db
from ..models import User
from ..events import subscribe, unsubscribe
from ..auth import JWT_SECRET, JWT_ALGORITHM

router = APIRouter(prefix="/notify", tags=["notify"]) 


@router.get("/me")
async def sse_me(token: Optional[str] = None, user: Optional[User] = Depends(get_current_user), db: Session = Depends(get_db)):
    # Allow token via query param to support EventSource
    if user is None:
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = int(payload.get("sub"))
            user = db.query(User).get(user_id)
            if not user:
                raise HTTPException(status_code=401, detail="Unauthorized")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    queue = subscribe(user.id)

    async def event_stream():
        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"
        finally:
            unsubscribe(user.id, queue)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
