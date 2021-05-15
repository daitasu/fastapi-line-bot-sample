import app.settings as settings
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from fastapi import Request, BackgroundTasks
from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi

router = APIRouter()

line_api = AioLineBotApi(channel_access_token=settings.CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(channel_secret=settings.CHANNEL_SECRET)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


async def handle_events(events):
    for event in events:
        try:
            await line_api.reply_message_async(
                event.reply_token,
                TextMessage(text=f"You said: {event.message.text}"))
        except Exception as err:
            print(err)
            pass


@router.get("/items/{item_id}")
def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    return {"item_id": item_id, "q": q, "short": short}


@router.put("/items/{item_id}")
def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    print(result)
    if q:
        result.update({"q": q})
    return result


@app.post("/callback")
async def callback(request: Request, background_tasks: BackgroundTasks) -> str:
    signature = request.headers.get("X-Line-Signature", "")
    events = parser.parse(
        (await request.body()).decode("utf-8"), signature
    )
    background_tasks.add_task(handle_events, events=events)

    return "ok"
