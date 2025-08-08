import asyncio
import json
import os
import re
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

# FastAPI app
app = FastAPI()

# Regex pattern to match NER lines
ner_pattern = re.compile(r'^(NAME|GENDER|DOB|PROFILE|ABOUT|INTERESTS): (.+)$')


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"Client connected: {websocket.client}")

    try:
        # Path to where `last.py` is located
        cwd_path = os.path.dirname(os.path.abspath(__file__))

        # Start the subprocess
        process = await asyncio.create_subprocess_exec(
            sys.executable, "last.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd_path
        )
    except Exception as e:
        error_msg = f"[Subprocess Error] {type(e).__name__}: {e}"
        print(error_msg)
        await websocket.send_json({'error': error_msg})
        await websocket.close()
        return

    async def read_stream(stream, stream_name):
        while True:
            line = await stream.readline()
            if not line:
                break
            decoded = line.decode("utf-8").strip()
            print(f"{stream_name}: {decoded}")

            match = ner_pattern.match(decoded)
            if match:
                label, value = match.groups()
                payload = {"label": label, "value": value}
                print(f"Sending to client: {payload}")
                await websocket.send_json(payload)
            elif stream_name == "STDERR":
                await websocket.send_json({'error': decoded})

    try:
        await asyncio.gather(
            read_stream(process.stdout, "STDOUT"),
            read_stream(process.stderr, "STDERR")
        )
    except WebSocketDisconnect:
        print(f"Client disconnected: {websocket.client}")
    finally:
        await process.wait()
        print(f"Subprocess finished for client: {websocket.client}")


@app.get("/")
async def root():
    return {"status": "WebSocket server is running"}
