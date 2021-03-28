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

ANSWER_SCORE_THRESHOLD = 0.8


class ModelInput(BaseModel):
    contexts: List[str]
    question: str


def span_to_answer(tokenizer, text: str, start: int, end: int):
    """
    When decoding from token probabilities, this method maps token indexes to actual word in the initial context.

    Args:
        text (:obj:`str`): The actual context to extract the answer from.
        start (:obj:`int`): The answer starting token index.
        end (:obj:`int`): The answer end token index.

    Returns:
        Dictionary like :obj:`{'answer': str, 'start': int, 'end': int}`
    """
    words = []
    token_idx = char_start_idx = char_end_idx = chars_idx = 0

    for i, word in enumerate(text.split(" ")):
        token = tokenizer.tokenize(word)

        # Append words if they are in the span
        if start <= token_idx <= end:
            if token_idx == start:
                char_start_idx = chars_idx

            if token_idx == end:
                char_end_idx = chars_idx + len(word)

            words += [word]

        # Stop if we went over the end of the answer
        if token_idx > end:
            break

        # Append the subtokenization length to the running index
        token_idx += len(token)
        chars_idx += len(word) + 1

    # Join text with spaces
    return {
        "answer": " ".join(words),
        "start": max(0, char_start_idx),
        "end": min(len(text), char_end_idx),
    }


def run_qa_inference(context, question):
    inputs = qa_tokenizer.encode_plus(
        question, context, add_special_tokens=True, return_tensors="pt"
    )
    input_ids = inputs["input_ids"].tolist()[0]
    # print("input_ids: ", input_ids)
    text_tokens = qa_tokenizer.convert_ids_to_tokens(input_ids)
    print("text_tokens: ", text_tokens)
    print("qa_tokenizer.convert_tokens_to_string(text_tokens): ", qa_tokenizer.convert_tokens_to_string(text_tokens))
    print("join text tokens: ", " ".join(text_tokens).replace(" ##", "").strip())
    

    # print("len(context.split()): ", len(context.split(" ")))
    # print("len(input_ids): ", len(input_ids))
    # print("len(text_tokens): ", len(text_tokens))

    # @see https://stackoverflow.com/questions/64901831/huggingface-transformer-model-returns-string-instead-of-logits
    answer_start_preds, answer_end_preds = qa_model(**inputs).values()

    # Get the most likely beginning and end of answer with the argmax of the predictions
    answer_start = torch.argmax(answer_start_preds)
    answer_end = torch.argmax(answer_end_preds) + 1

    # print("ids to tokens: ", qa_tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    answer = qa_tokenizer.convert_tokens_to_string(
        qa_tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end])
    )
    # print("qa_tokenizer.words_to_chars(input_ids[answer_start:answer_end]): ", qa_tokenizer.words_to_chars(input_ids[answer_start:answer_end]))
    # print("input_ids[answer_start]: ", input_ids[answer_start])
    # print("input_ids[answer_end]: ", input_ids[answer_end])
    # print("span_to_answer: ", span_to_answer(qa_tokenizer, context, answer_start, answer_end))

    return {
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
            filter(
                lambda x: x["score"] > ANSWER_SCORE_THRESHOLD,
                sorted(
                    map(
                        functools.partial(
                            run_qa_inference, question=model_input.question
                        ),
                        model_input.contexts,
                    ),
                    key=lambda x: x["score"],
                    reverse=True,
                ),
            )
        )
    }
