from fastapi import FastAPI, WebSocket
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from src.model import BM25
from src.config import TrainerConfig
import os
import json
from typing import TypedDict

class MessageParams(TypedDict):
    value: str

class MessagePacket(TypedDict):
    type: str
    params: MessageParams

trainer_config = TrainerConfig()
# set hugging face cache
os.environ['HF_HOME'] = trainer_config.cache_dir

app = FastAPI()
bm25_model = BM25("./outputs/bm25")

class ConnectionManager:
    def __init__(self):
        self.active_connection: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connection.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connection:
            await connection.send_text(message)


manager = ConnectionManager()

@app.get("/")
async def get_root():
    return{"message": "welcome to the chatbot server!"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id:str):
    await manager.connect(websocket)
    try:
        while True:
            packet_data = await websocket.receive_text()
            packet_data = json.loads(packet_data)
            if packet_data["type"] == "message:send":
                resp = {"type": "room:message", "params": {"payload": {"message": "hi"}}}
                await manager.send_personal_message(json.dumps(resp), websocket)
                #await manager.send_personal_message(f"You wrote: {data}", websocket)
    
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
