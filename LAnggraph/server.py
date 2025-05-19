from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from ai_mcp import graph_compiled, initial_state
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    userId: str

@app.post("/chat")
async def chat_endpoint(body: ChatRequest):
    print("[DEBUG] Incoming request body:", body.dict())
    user_input = body.message
    user_id = body.userId
    state = {"user_input": user_input, **initial_state}
    print("[DEBUG] State passed to graph:", state)
    final_state = graph_compiled.invoke(state)
    print("[DEBUG] Final state from graph:", final_state)
    # Defensive: if 'output' is missing, return the whole state for debugging
    output = final_state.get("output", final_state)
    print("[DEBUG] Output returned to client:", output)
    return JSONResponse(content={"output": output})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
