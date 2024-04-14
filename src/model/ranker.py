import torch.nn as nn
from transformers import AutoModel, AutoConfig
from src.config import TrainerConfig

class DocumentRanker(nn.Module):
    def __init__(self, model_name: str, config: TrainerConfig):
        super(DocumentRanker, self).__init__()
        self.model = AutoModel.from_pretrained(model_name, cache_dir=config.cache_dir)
        self.config = AutoConfig.from_pretrained(model_name, cache_dir=config.cache_dir)
        self.drop = nn.Dropout(p=0.2)
        self.fc = nn.Linear(768, 1)

    def forward(self, ids, masks):
        out = self.model(input_ids=ids,
                           attention_mask=masks,
                           output_hidden_states=False).last_hidden_state
        out = out[:,0]
        outputs = self.fc(out)
        return outputs
    
    def predict(self):
        pass