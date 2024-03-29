import tqdm

from src.model import DocumentRanker
from src.config import TrainerConfig

class RankerTrainer:
    def __init__(self, model: DocumentRanker, config: TrainerConfig) -> None:
        self.model = model
        self.config = config
    
    def train(self):
        if self.config.device == "gpu":
            self.model.cuda()
        for epoch in tqdm(range(self.config.epochs)):
            self.model.train()
        