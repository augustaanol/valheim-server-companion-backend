from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.services.task_events import task_events

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/tasks")
async def task_events_stream(request: Request):
    queue = await task_events.connect()

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break

                message = await queue.get()
                yield f"data: {message}\n\n"
        finally:
            task_events.disconnect(queue)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
