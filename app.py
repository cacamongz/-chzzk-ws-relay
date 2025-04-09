import asyncio
import websockets
import aiohttp
import json
import os

PORT = int(os.environ.get("PORT", 8765))
BROADCAST_ID = os.environ.get("BROADCAST_ID", "d7ddd7585a271e55159ae47c0ce9a9dd")
REMOTE_WS_URL = f"wss://kr-ss.chzzk.naver.com/ws/chat/v1?broadcastId={BROADCAST_ID}"

async def relay(websocket, path):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(REMOTE_WS_URL) as remote_ws:
            async def from_remote():
                async for msg in remote_ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        try:
                            payload = json.loads(msg.data)
                            if payload.get("type") == "chat":
                                await websocket.send(json.dumps(payload["data"]))
                        except Exception:
                            pass

            async def from_browser():
                async for _ in websocket:
                    pass

            await asyncio.gather(from_remote(), from_browser())

async def main():
    print(f"✅ 중계 서버 실행 중 (포트 {PORT})")
    await websockets.serve(relay, "0.0.0.0", PORT)
    await asyncio.Future()  # keep running

if __name__ == "__main__":
    asyncio.run(main())
