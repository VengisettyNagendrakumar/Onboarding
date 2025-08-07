import asyncio
import websockets
import sys
import json
import re

# Regex pattern to match NER lines
ner_pattern = re.compile(r'^(NAME|GENDER|DOB|PROFILE|ABOUT|INTERESTS): (.+)$')

async def handle_websocket(websocket, path):
    print(f"Client connected: {websocket.remote_address}")

    try:
        # Run try3.py as a subprocess
        process = await asyncio.create_subprocess_exec(
            sys.executable, 'last.py',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd='E:/Machine Learning/ML Tasks(meetx)/Onboarding algorithm/Nova/nova sonic'
        )
    except Exception as e:
        error_msg = f"[Subprocess Error] {type(e).__name__}: {e}"
        print(error_msg)
        await websocket.send(json.dumps({'error': error_msg}))
        return

    async def read_stream(stream, stream_name):
        while True:
            line = await stream.readline()
            if not line:
                break
            decoded = line.decode('utf-8').strip()
            print(f"{stream_name}: {decoded}")  # Debug log

            match = ner_pattern.match(decoded)
            if match:
                label, value = match.groups()
                payload = {'label': label, 'value': value}
                print(f"Sending to client: {payload}")
                await websocket.send(json.dumps(payload))
            elif stream_name == "STDERR":
                await websocket.send(json.dumps({'error': decoded}))

    try:
        await asyncio.gather(
            read_stream(process.stdout, "STDOUT"),
            read_stream(process.stderr, "STDERR")
        )
    finally:
        await process.wait()
        print(f"Client disconnected: {websocket.remote_address}")

async def main():
    server = await websockets.serve(handle_websocket, '0.0.0.0', 5000)
    print("WebSocket server running at ws://localhost:5000")
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
