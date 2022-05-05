import json
import os

import requests
import transformers
import yaml

from typing import List
from src.dense_retriever import DenseRetriever
from src.utils import create_text_from_summary_and_dialogue

_terminal_characters = ["\n", "User:"]
_path = os.path.dirname(__file__)
_config = yaml.safe_load(open(os.path.join(_path, "../config.yaml")))
_server_url = f"https://{_config['connection']['host']}:{_config['connection']['port']}/predictions/bot"
_tokenizer = transformers.AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
_retriever = DenseRetriever("msmarco-distilbert-base-v3")

_knowledge = yaml.safe_load(open(os.path.join(_path, "../knowledge.yaml")))
for index, sentence in enumerate(_knowledge["items"]):
    _retriever.add_text_and_index(sentence, str(index))
_chatbot_name = _knowledge["chatbot"]["name"]


def predict_answer(prompt: str) -> str:
    # payload = {"data": prompt, "num_beams": 3}
    payload = {"data": prompt}
    r = requests.post(_server_url, json=payload, verify=False)
    answer = json.loads(r.content.decode("utf-8"))
    return _tokenizer.decode(answer)


def create_dialogue_from_bot_and_user_lines(bot_lines, user_lines, max_history=-3):
    dialogue = ""
    for bot_line, user_line in zip(bot_lines[max_history:], user_lines[max_history:]):
        dialogue += f"{_chatbot_name}: {bot_line}\n"
        dialogue += f"User: {user_line}\n"

    return dialogue


def generate_reply(summary: str, bot_lines: List[str], user_lines: List[str]) -> str:
    dialogue = create_dialogue_from_bot_and_user_lines(bot_lines, user_lines)
    dialogue += f"{_chatbot_name}: "
    answer = ""
    print()
    print(create_text_from_summary_and_dialogue(summary, dialogue + answer))
    print()

    while all(item not in answer for item in _terminal_characters):
        text = create_text_from_summary_and_dialogue(summary, dialogue + answer)
        answer += predict_answer(text)[len(text) :]

    end = min(
        [answer.find(item) for item in _terminal_characters if answer.find(item) > 0]
    )
    answer = answer[:end].strip()

    return answer


def get_relevant_summary(query: str, prologue: str = "") -> str:
    summary = "\n".join(_knowledge["permanent"]) + "\n"
    summary += prologue + "\n"
    best_indices = _retriever.get_indices_and_scores_from_text(query, topn=3)
    for index, _ in best_indices:
        summary += _knowledge["items"][int(index)] + "\n"

    summary = summary.replace(".\n", ". ")
    summary = summary.replace("\n", ". ")
    return summary
