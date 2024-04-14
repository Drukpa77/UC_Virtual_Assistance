from torch.utils.data import Dataset
import torch

class DocumentDataset(Dataset):
    def __init__(self, df, tokenizer, max_length, test = False):
        self.df = df
        self.max_length = max_length
        self.tokenizer = tokenizer
        self.test = test
        self.content1 = tokenizer.batch_encode_plus(list(df.question.apply(lambda x: x.replace("_"," ")).values), max_length=max_length, truncation=True)["input_ids"]
        self.content2 = tokenizer.batch_encode_plus(list(df.answer.apply(lambda x: x.replace("_"," ")).values), max_length=max_length, truncation=True)["input_ids"]
        if not test:
            self.targets = self.df.label

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        return {
            'ids1': torch.tensor(self.content1[index], dtype=torch.long),
            'ids2': torch.tensor(self.content2[index][1:], dtype=torch.long),
            #'target': torch.tensor(self.targets[index], dtype=torch.float)
            'target': torch.tensor(0) if self.test else torch.tensor(self.targets[index], dtype=torch.float)
        }