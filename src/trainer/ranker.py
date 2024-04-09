import tqdm

import torch.nn as nn
from pandas import DataFrame
import numpy as np
from sklearn.model_selection import KFold
from transformers import AutoTokenizer
from torch.utils.data import DataLoader

from src.model import DocumentRanker
from src.config import TrainerConfig
from src.dataset import DocumentDataset
from src.model_utils import collate_fn
from src.optimizer import optimizer_scheduler


class RankerTrainer:
    def __init__(self, model: DocumentRanker, config: TrainerConfig, df: DataFrame, tokenizer: AutoTokenizer) -> None:
        self.model = model
        self.config = config
        self.df = df
        self.tokenizer = tokenizer
    
    def train(self):
        loss_fn = nn.BCEWithLogitsLoss() # define loss function
        # TODO: configurable
        kfold = KFold(n_splits=5, shuffle=True, random_state=42)

        if self.config.device == "gpu":
            self.model.cuda()

        for fold, (train_index, test_index) in enumerate(kfold.split(self.df, self.df.label)):
            if fold != 0:
                break
            train_df = self.df
            val_df = self.df.iloc[test_index].reset_index(drop=True)
            train_dataset = DocumentDataset(train_df, self.tokenizer, 384)
            valid_dataset = DocumentDataset(val_df, self.tokenizer, 384)

            pad_token_id = self.tokenizer.pad_token_id
            train_loader = DataLoader(train_dataset, batch_size=4, collate_fn=lambda batch: collate_fn(batch, pad_token_id),
                              num_workers=2, shuffle=True, pin_memory=True, drop_last=True)
            valid_loader = DataLoader(valid_dataset, batch_size=32, collate_fn=lambda batch: collate_fn(batch, pad_token_id),
                                    num_workers=2, shuffle=False, pin_memory=True)

            num_train_steps = len(train_loader) * self.config.epochs // self.config.accumulation_step
            optimizer, scheduler = optimizer_scheduler(self.model, num_train_steps)
        
            for epoch in tqdm(range(self.config.epochs)):
                self.model.train()
                bar = tqdm(enumerate(train_loader), total=len(train_loader), leave=False)
                for step, data in bar:
                    ids = data["ids"].cuda()
                   
                    masks = data["masks"].cuda()
                    target = data["target"].cuda()
                    
                    preds = self.model(ids, masks)
                   
                    loss = loss_fn(preds.view(-1), target.view(-1))
                    loss /= self.config.accumulation_step
                    loss.backward()
                    if (step + 1) % self.config.accumulation_step == 0:
                        optimizer.step()
                        optimizer.zero_grad()
                        scheduler.step()
                    bar.set_postfix(loss=loss.item())
                self.model.eval()
        