import json
import os

import requests
import transformers
import yaml

from src.dense_retriever import DenseRetriever
from src.utils import create_text_from_summary_and_dialogue

_path = os.path.dirname(__file__)
_config = yaml.safe_load(open(os.path.join(_path, "./config.yaml")))
_server_url = f"https://{_config['connection']['host']}:{_config['connection']['port']}/predictions/bot"
_tokenizer = transformers.AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
_retriever = DenseRetriever("msmarco-distilbert-base-v3")

_knowledge = yaml.safe_load(open(os.path.join(_path, "./knowledge.yaml")))
for index, sentence in enumerate(_knowledge["items"]):
    _retriever.add_text_and_index(sentence, str(index))


def predict_answer(prompt: str) -> str:
    payload = {"data": prompt}
    r = requests.post(_server_url, json=payload, verify=False)
    answer = json.loads(r.content.decode("utf-8"))
    return _tokenizer.decode(answer)


def generate_reply(summary: str, dialogue: str, query: str) -> str:
    dialogue += "\nAlberto: " + query + "\nJohn: "
    answer = ""

    terminal_characters = [".", "!", "?", "\n"]

    while all(item not in answer for item in terminal_characters):
        text = create_text_from_summary_and_dialogue(summary, dialogue + answer)
        answer += predict_answer(text)[len(text) :]

    end = min(
        [answer.find(item) for item in terminal_characters if answer.find(item) > 0]
    )
    answer = answer[:end].strip()

    return answer


def get_relevant_summary(query: str, prologue: str = "") -> str:
    summary = prologue + "\n"
    summary += _knowledge["permanent"] + "\n"
    best_indices = _retriever.get_indices_and_scores_from_text(query)
    for index in best_indices:
        summary += _knowledge["items"][int(index)] + "\n"

    return summary
