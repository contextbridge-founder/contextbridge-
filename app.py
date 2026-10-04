import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from anthropic import AsyncAnthropic

app = FastAPI()

# 1. Initialize the premium enterprise Anthropic connector safely
client = AsyncAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

@app.get("/")
async def root():
    return {"status": "healthy", "service": "ContextBridge Gateway"}

@app.post("/engine/sync")
async def engine_sync(request: Request):
    try:
        # Accept the incoming payload data packet from the user
        payload = await request.json()
        
        # Verify our OpenAPI Blueprint Shield required fields are present
        if "user_id" not in payload or "raw_statement" not in payload:
            return JSONResponse(
                status_code=422,
                content={"detail": [{"msg": "Field required", "loc": ["body", "user_id"]}]}
            )
            
        broken_log_payload = payload.get("text_to_fix", "")
        
        # 2. Route the broken data payload straight to the Anthropic industry gold standard
        message = await client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            messages=[{"role": "user", "content": broken_log_payload}]
        )
        
        # 3. Return the clean, database-ready payload straight back to the client
        return {
            "user_id": payload.get("user_id"),
            "raw_statement": payload.get("raw_statement"),
            "text_to_fix": message.content.text
        }
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
