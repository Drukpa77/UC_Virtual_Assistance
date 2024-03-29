class TrainerConfig:
    def __init__(self) -> None:
        self.device = "gpu"
        self.epochs = 2
        self.accumulation_step = 8
        self.train_batch_size = 4
        self.valid_batch_size = 32

    def load_config(self) -> None:
        pass