class TrainerConfig:
    def __init__(self) -> None:
        self.device = "cpu"
        self.epochs = 2
        self.accumulation_step = 8
        self.train_batch_size = 4
        self.valid_batch_size = 32
        self.learning_rate = 3e-5
        self.cache_dir = "./hf_cache"
        self.nltk_dir = "./nltk_cache"

    def load_config(self) -> None:
        pass