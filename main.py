from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
import uvicorn
import os
from pathlib import Path

app = FastAPI()

# Serve frontend HTML (if exists)
@app.get("/")
async def get():
    index_path = Path("index.html")
    if index_path.exists():
        return HTMLResponse(index_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>FastAPI WebSocket Server Running</h1>")

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📥 Received from client: {data}")

            try:
                parsed = json.loads(data)  # Try to parse incoming JSON
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "error": "Invalid JSON format"
                }))
                continue

            # Example: respond with structured JSON
            response = {
                "label": "name",
                "value": "Mux User",
                "received": parsed
            }
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        print("⚡ Client disconnected")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        reload=False
    )
