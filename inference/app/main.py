import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from typing import List
from fastapi import (
    FastAPI,
    Request,
    Depends,
    HTTPException,
)
from pydantic import BaseModel

app = FastAPI()

# @see https://huggingface.co/transformers/v2.8.0/usage.html
qa_tokenizer = AutoTokenizer.from_pretrained("/models/distilbert-base-uncased-distilled-squad")
# print("qa_tokenizer: ", qa_tokenizer)
qa_model = AutoModelForQuestionAnswering.from_pretrained("/models/distilbert-base-uncased-distilled-squad")
# print("qa_model: ", qa_model)


class ModelInput(BaseModel):
    text: str


# @app.post("/predict")
# async def predict(model_input: ModelInput):
#     res = {
#         "model_input": model_input,
#         "label": "POSITIVE",
#         "score": 0.51,
#     }
#     return res
 
@app.get("/predict")
async def predict():
    text = r"""
    🤗 Transformers (formerly known as pytorch-transformers and pytorch-pretrained-bert) provides general-purpose
    architectures (BERT, GPT-2, RoBERTa, XLM, DistilBert, XLNet…) for Natural Language Understanding (NLU) and Natural
    Language Generation (NLG) with over 32+ pretrained models in 100+ languages and deep interoperability between
    TensorFlow 2.0 and PyTorch.
    """

    questions = [
        "How many pretrained models are available in Transformers?",
        "What does Transformers provide?",
        "Transformers provides interoperability between which frameworks?",
    ]

    answers = []
    answer_starts = []
    answer_ends = []
    for question in questions:
        inputs = qa_tokenizer.encode_plus(question, text, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]

        text_tokens = qa_tokenizer.convert_ids_to_tokens(input_ids)
        # https://stackoverflow.com/questions/64901831/huggingface-transformer-model-returns-string-instead-of-logits
        answer_start_scores, answer_end_scores = qa_model(**inputs).values()
        # print("answer_start_scores: ", answer_start_scores)
        # print("answer_end_scores: ", answer_end_scores)

        answer_start = torch.argmax(
            answer_start_scores
        )  # Get the most likely beginning of answer with the argmax of the score
        print("answer_start: ", answer_start)
        answer_starts.append(answer_start.item())
        answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
        answer_ends.append(answer_end.item())

        answer = qa_tokenizer.convert_tokens_to_string(qa_tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

        # print(f"Question: {question}")
        # print(f"Answer: {answer}\n")
        answers.append(answer)
    
    
    res = {
        "questions": questions,
        "answers": answers,
        "answer_starts": answer_starts,
        "answer_ends": answer_ends,
    }
    return res
