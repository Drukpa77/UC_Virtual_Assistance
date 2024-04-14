from fastapi import FastAPI, WebSocket
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from src.model import BM25, DocumentRanker
from src.config import TrainerConfig
from src.tokenizer import preprocess_text
import os
import json
from typing import TypedDict
import nltk
import pandas as pd
import torch
from transformers import AutoTokenizer
import numpy as np

class MessageParams(TypedDict):
    value: str

class MessagePacket(TypedDict):
    type: str
    params: MessageParams

trainer_config = TrainerConfig()
# set hugging face cache
os.environ['HF_HOME'] = trainer_config.cache_dir
nltk.data.path.append(trainer_config.nltk_dir)

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', cache_dir=trainer_config.cache_dir)
app = FastAPI()
bm25_model = BM25("./outputs/bm25")

df_windows = pd.read_csv("./data/data_cleaned.csv")
ranker_model = DocumentRanker("bert-base-uncased", trainer_config)
ranker_model.load_state_dict(torch.load("./outputs/ranker.bin", map_location=torch.device('cpu')))
ranker_model.eval()

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

def rank_document(question: str):
    query = preprocess_text(question).lower()
    top_n, bm25_scores = bm25_model.get(query, top=50)
    texts = [preprocess_text(df_windows.answer.values[i]) for i in top_n]
    question = preprocess_text(question)
    ranking_preds = ranker_model.predict(question, texts, tokenizer)
    ranking_scores = ranking_preds * bm25_scores

    best_idxs = np.argsort(ranking_scores)[-10:]
    ranking_scores = np.array(ranking_scores)[best_idxs]
    texts = np.array(texts)[best_idxs]
    return texts[len(texts) - 1]


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
            message = packet_data["params"]["value"]
            if packet_data["type"] == "message:send":
                ans = rank_document(message)
                resp = {"type": "room:message", "params": {"payload": {"message": ans}}}
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
