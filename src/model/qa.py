from transformers import AutoModelForQuestionAnswering, pipeline
from typing import Union

class QAModel:
    def __init__(self, model_name: str, threshold: float):
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        self.nlp = pipeline('question-answering', model=self.model, tokenizer=model_name)
        self.threshold = threshold

    def predict(self, question, texts, ranking_scores) -> Union[None, str]:
        answers = []
        best_score = 0
        answer = ""
        for text, score in zip(texts, ranking_scores):
            res = self.nlp(question=question, context=text)
            if res["score"] > self.threshold:
                answers.append(text)
            res["score"] = res["score"] * score
            if res["score"] > best_score:
                answer = text
                best_score = res["score"]
        if len(answers) == 0:
            return None
        return answer
