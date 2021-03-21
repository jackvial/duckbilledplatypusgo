import os
import json
import torch
from typing import List
from fastapi import (
    FastAPI,
    Request,
    Depends,
    HTTPException,
)
from pydantic import BaseModel
import functools
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

app = FastAPI()

# @see https://huggingface.co/transformers/v2.8.0/usage.html
# There are currently no docs for new versions but it's much the same.
qa_tokenizer = AutoTokenizer.from_pretrained(
    "/models/distilbert-base-uncased-distilled-squad"
)
qa_model = AutoModelForQuestionAnswering.from_pretrained(
    "/models/distilbert-base-uncased-distilled-squad"
)


class ModelInput(BaseModel):
    contexts: List[str]
    question: str


def run_qa_inference(context, question):
    inputs = qa_tokenizer.encode_plus(
        question, context, add_special_tokens=True, return_tensors="pt"
    )
    input_ids = inputs["input_ids"].tolist()[0]
    text_tokens = qa_tokenizer.convert_ids_to_tokens(input_ids)

    # @see https://stackoverflow.com/questions/64901831/huggingface-transformer-model-returns-string-instead-of-logits
    answer_start_preds, answer_end_preds = qa_model(**inputs).values()

    # Get the most likely beginning and end of answer with the argmax of the predictions
    answer_start = torch.argmax(answer_start_preds)
    answer_end = torch.argmax(answer_end_preds) + 1
    answer = qa_tokenizer.convert_tokens_to_string(
        qa_tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end])
    )

    return {
        "inputs": inputs,
        "answer": answer,
        "score": torch.sigmoid(torch.max(answer_start_preds)).item(),
        "context": context,
        "answer_start": answer_start.item(),
        "answer_end": answer_end.item(),
    }


@app.post("/predict")
async def predict(model_input: ModelInput):
    return {
        "results": list(
            map(
                functools.partial(run_qa_inference, question=model_input.question),
                model_input.contexts,
            )
        )
    }
