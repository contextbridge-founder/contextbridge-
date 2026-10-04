import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from anthropic import AsyncAnthropic

app = FastAPI()

client = AsyncAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

@app.get("/")
async def root():
    return {"status": "healthy", "service": "ContextBridge Gateway"}

@app.post("/engine/sync")
async def engine_sync(request: Request):
    try:
        payload = await request.json()
        if "user_id" not in payload or "raw_statement" not in payload:
            return JSONResponse(
                status_code=422,
                content={"detail": [{"msg": "Field required", "loc": ["body", "user_id"]}]}
            )
        broken_log_payload = payload.get("text_to_fix", "")
        message = await client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1500,
            messages=[{"role": "user", "content": broken_log_payload}]
        )
        return {
            "user_id": payload.get("user_id"),
            "raw_statement": payload.get("raw_statement"),
            "text_to_fix": message.content.text
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
