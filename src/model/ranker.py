import torch.nn as nn
from transformers import AutoModel, AutoConfig
from src.config import TrainerConfig
import pandas as pd
from torch.utils.data import DataLoader
import torch
from src.model_utils import collate_fn
from src.dataset import DocumentDataset
from tqdm import tqdm

class DocumentRanker(nn.Module):
    def __init__(self, model_name: str, config: TrainerConfig, tokenizer):
        super(DocumentRanker, self).__init__()
        self.model = AutoModel.from_pretrained(model_name, cache_dir=config.cache_dir)
        self.config = AutoConfig.from_pretrained(model_name, cache_dir=config.cache_dir)
        self.drop = nn.Dropout(p=0.2)
        self.max_length = 128
        self.batch_size = 4
        self.device = config.device
        self.fc = nn.Linear(768, 1).to(self.device)
        self.model.to(self.device)
        self.model.eval()
        self.pad_token_id = tokenizer.pad_token_id

    def forward(self, ids, masks):
        out = self.model(input_ids=ids,
                           attention_mask=masks,
                           output_hidden_states=False).last_hidden_state
        out = out[:,0]
        outputs = self.fc(out)
        return outputs
    
    def predict(self, question: str, texts: str, tokenizer):
        tmp = pd.DataFrame()
        pad_token_id = tokenizer.pad_token_id
        tmp["answer"] = [" ".join(x.split()) for x in texts]
        tmp["question"] = question
        valid_dataset = DocumentDataset(tmp, tokenizer, self.max_length, test=True)
        valid_loader = DataLoader(valid_dataset, batch_size=self.batch_size, collate_fn=lambda batch: collate_fn(batch, self.pad_token_id),
                                  num_workers=0, shuffle=False, pin_memory=True)
        preds = []
    
        with torch.no_grad():
            bar = enumerate(valid_loader)
            for step, data in tqdm(bar):
                ids = data["ids"].to(self.device)
                masks = data["masks"].to(self.device)
                preds.append(torch.sigmoid(self(ids, masks)).view(-1))
            preds = torch.cat(preds)
        """
        with torch.no_grad():
            # Wrap the DataLoader directly with tqdm for progress tracking
            for step, data in tqdm(enumerate(valid_loader), total=len(valid_loader)):
                ids = data["ids"].to(self.device)
                masks = data["masks"].to(self.device)
        
                # Perform inference
                preds.append(torch.sigmoid(self(ids, masks)).view(-1))
        preds = torch.cat(preds)
        """
        return preds.cpu().numpy()