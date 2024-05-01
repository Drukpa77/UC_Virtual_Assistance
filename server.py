from fastapi import FastAPI, WebSocket
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from src.model import BM25, DocumentRanker
from src.config import TrainerConfig, EnvConfig
from src.tokenizer import preprocess_text
import os
import json
from typing import TypedDict
import nltk
import pandas as pd
import torch
from transformers import AutoTokenizer
import numpy as np
import uuid
from src.entity import Message
from src.config import load_dotenv
from src.cache import Cache


class MessageParams(TypedDict):
    value: str

class MessagePacket(TypedDict):
    type: str
    params: MessageParams

load_dotenv(".env")
trainer_config = TrainerConfig()
env_config = EnvConfig()
cache = Cache(env_config)
# set hugging face cache
os.environ['HF_HOME'] = trainer_config.cache_dir
nltk.data.path.append(trainer_config.nltk_dir)

tokenizer = AutoTokenizer.from_pretrained(env_config.HF_MODEL, cache_dir=trainer_config.cache_dir)
app = FastAPI()
bm25_model = BM25(env_config.bm25_model)

df_windows = pd.read_csv("./data/data_cleaned.csv")
ranker_model = DocumentRanker(env_config.HF_MODEL, trainer_config)
ranker_model.load_state_dict(torch.load(env_config.document_model, map_location=torch.device('cpu')))
ranker_model.eval()


DEFAULT_RESPONSE = """I'm sorry, I couldn't find an answer to your question. It's possible that I may not have enough information to help you with this specific query. Here are a few suggestions: \n
- Try rephrasing your question in a different way to see if I can better understand what you're looking for. \n
- You can also check our help section on our website for more information. \n
- If you prefer, I can connect you with a human agent who may be able to assist you further. \n

Thank you for reaching out! Please feel free to ask if you have any other questions or need assistance with anything else."""


class Connection:
    def __init__(self, connection: WebSocket):
        self.connection = connection
        self.session = uuid.uuid4()

    async def send_message(self, message: str):
        await self.connection.send_text(message)

class ConnectionManager:
    def __init__(self):
        self.active_connection: List[Connection] = []

    async def connect(self, connection: Connection):
        await connection.connection.accept()
        #await websocket.accept()
        self.active_connection.append(connection)

    def disconnect(self, connection: Connection):
        self.active_connection.remove(connection)

    async def send_personal_message(self, message: str, connection: Connection):
        await connection.send_message(message)

    async def broadcast(self, message: str):
        for connection in self.active_connection:
            await connection.send_message(message)

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

    threshold = 9
    if ranking_scores[len(texts) - 1] > threshold:
        return texts[len(texts) - 1]
    return DEFAULT_RESPONSE


manager = ConnectionManager()

@app.get("/")
async def get_root():
    return{"message": "welcome to the chatbot server!"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id:str):
    connection = Connection(websocket)
    await manager.connect(connection)
    
    try:
        while True:
            packet_data = await websocket.receive_text()
            packet_data = json.loads(packet_data)
            message = packet_data["params"]["value"]
            if packet_data["type"] == "message:send":
                # save message
                record = Message()
                record.session = connection.session
                record.message = message
                record.is_bot = False

                record.save()

                ans = cache.get(message)
                if ans is None:
                    # no cahce
                    ans = rank_document(message)
                    cache.set(message, ans)
    
                # save answer
                record = Message()
                record.session = connection.session
                record.message = ans
                record.is_bot = True

                record.save()
                
                resp = {"type": "room:message", "params": {"payload": {"message": ans}}}
                await manager.send_personal_message(json.dumps(resp), connection)
    
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
