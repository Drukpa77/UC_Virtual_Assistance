import torch
import numpy as np
from typing import Dict, List

def collate_fn(batch: List[Dict[str, torch.Tensor]], pad_token_id: int) -> Dict[str, torch.Tensor]:
    ids = [torch.cat([x["ids1"], x["ids2"]]) for x in batch]
    targets = [x["target"] for x in batch]
    max_len = np.max([len(x) for x in ids])
    masks = []
    for i in range(len(ids)):
        if len(ids[i]) < max_len:
            ids[i] = torch.cat((ids[i], torch.tensor([pad_token_id,]*(max_len - len(ids[i])), dtype=torch.long)))
        masks.append(ids[i] != pad_token_id)
    outputs = {
        "ids": torch.vstack(ids),
        "masks": torch.vstack(masks),
        "target": torch.vstack(targets).view(-1)
    }
    return outputs