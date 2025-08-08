from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import uvicorn
import os

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📥 Received from client: {data}")

            try:
                parsed = json.loads(data)  # Parse incoming JSON
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "label": "error",
                    "value": "Invalid JSON format"
                }))
                continue

            # Only send back valid label/value
            if "label" in parsed and "value" in parsed:
                await websocket.send_text(json.dumps(parsed))
            else:
                await websocket.send_text(json.dumps({
                    "label": "error",
                    "value": "Missing 'label' or 'value'"
                }))

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
