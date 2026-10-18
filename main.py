
from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any

app = FastAPI()

API_KEY = "ak_jyevucgz1piihm2h48pv0wno"
EMAIL = "25f1002516@ds.study.iitm.ac.in"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)


class AnalyticsRequest(BaseModel):
    events: list[dict[str, Any]]


@app.post("/analytics")
async def analytics(
    body: AnalyticsRequest,
    x_api_key: str | None = Header(default=None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = body.events
    user_totals = defaultdict(float)
    revenue = 0.0

    for event in events:
        user = event.get("user")
        amount = float(event.get("amount", 0))

        if amount > 0:
            revenue += amount
            user_totals[user] += amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len({event.get("user") for event in events}),
        "revenue": round(revenue, 2),
        "top_user": top_user,
    }

