from transformers import AdamW, get_linear_schedule_with_warmup

def optimizer_scheduler(model, num_train_steps: int, learning_rate: float):
    param_optimizer = list(model.named_parameters())
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_parameters = [
            {
                "params": [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
                "weight_decay": 0.001,
            },
            {
                "params": [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
                "weight_decay": 0.0,
            },
        ]

    opt = AdamW(optimizer_parameters, lr=learning_rate)
    sch = get_linear_schedule_with_warmup(
        opt,
        num_warmup_steps=int(0.05*num_train_steps),
        num_training_steps=num_train_steps,
        last_epoch=-1,
    )
    return opt, sch