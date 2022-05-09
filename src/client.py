import json
import os

import requests
import transformers
import yaml

from typing import List
from src.dense_retriever import DenseRetriever
from src.language_detector import LanguageDetector
from src.toxicity_detector import ToxicityDetector
from src.utils import (
    create_text_from_summary_and_dialogue,
    is_question,
    query_refers_to_prior_dialogue,
)

_terminal_characters = ["\n", "User:"]
_path = os.path.dirname(__file__)
_config = yaml.safe_load(open(os.path.join(_path, "../config.yaml")))
_server_url = f"https://{_config['connection']['host']}:{_config['connection']['port']}/predictions/bot"
_tokenizer = transformers.AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
_retriever = DenseRetriever("msmarco-distilbert-base-v3")
_toxic_detector = ToxicityDetector("original")
_language_detector = LanguageDetector()

_knowledge = yaml.safe_load(open(os.path.join(_path, "../knowledge.yaml")))
for index, sentence in enumerate(_knowledge["permanent"]):
    _retriever.add_text_and_index(sentence, "PERM_" + str(index))

for index, sentence in enumerate(_knowledge["items"]):
    _retriever.add_text_and_index(sentence, "ITEM_" + str(index))
_chatbot_name = _knowledge["chatbot"]["name"]


def predict_answer(prompt: str) -> str:
    payload = {"data": prompt, "num_beams": 1}
    r = requests.post(_server_url, json=payload, verify=False)
    answer = json.loads(r.content.decode("utf-8"))
    return _tokenizer.decode(answer)


def create_dialogue_from_bot_and_user_lines(bot_lines, user_lines, max_history=3):
    dialogue = ""
    for bot_line, user_line in zip(bot_lines[-max_history:], user_lines[-max_history:]):
        dialogue += f"{_chatbot_name}: {bot_line}\n"
        dialogue += f"User: {user_line}\n"

    return dialogue


def get_reply_from_connection(summary: str, dialogue: str):
    answer = ""
    while all(item not in answer for item in _terminal_characters):
        text = create_text_from_summary_and_dialogue(summary, dialogue + answer)
        answer += predict_answer(text)[len(text) :]

    end = min(
        [answer.find(item) for item in _terminal_characters if answer.find(item) > 0]
    )
    answer = answer[:end].strip()
    return answer


def generate_reply(summary: str, bot_lines: List[str], user_lines: List[str]) -> str:
    if _toxic_detector.is_toxic(user_lines[-1]):
        return _knowledge["profanity"][0]

    if not _language_detector.is_english(user_lines[-1]):
        return _knowledge["non-english"][0]

    dialogue = create_dialogue_from_bot_and_user_lines(bot_lines, user_lines)
    dialogue += f"{_chatbot_name}: "
    answer = ""
    print()
    print(create_text_from_summary_and_dialogue(summary, dialogue + answer))
    print()

    answer = get_reply_from_connection(summary, dialogue)
    print(answer)
    print(bot_lines[-1])
    if answer != bot_lines[-1]:
        if _toxic_detector.is_toxic(answer):
            return _knowledge["profanity"][0]

        return answer

    dialogue = f"User: {user_lines[-1]}\n"
    print("New dialogue:")
    print(dialogue)
    dialogue += f"{_chatbot_name}: "

    answer = get_reply_from_connection(summary, dialogue)
    if _toxic_detector.is_toxic(answer):
        return _knowledge["profanity"]

    return answer


def get_relevant_summary(
    user_lines: str, prologue: str = "", retrieval_threshold=0.134
) -> str:
    query = user_lines[-1]
    summary = "\n".join(_knowledge["permanent"]) + "\n"
    summary += prologue + "\n"
    best_indices = _retriever.get_indices_and_scores_from_text(query, topn=3)
    print(best_indices)

    if (
        is_question(query)
        and all(item[1] < retrieval_threshold for item in best_indices)
        and not query_refers_to_prior_dialogue(query)
    ):
        summary += (
            f"When asked '{query}', the user replies '{_knowledge['default'][0]}'.\n"
        )
        return summary

    index_list = []
    for index, score in best_indices:
        if score < retrieval_threshold:
            continue

        if "PERM_" in index:
            summary += f"{_chatbot_name} wants to move the conversation to a different topic.\n"
            continue

        index = int(index.replace("ITEM_", ""))
        index_list.append(index)

    for utterance_index in range(2, min(len(user_lines) + 1, 4)):
        best_indices = _retriever.get_indices_and_scores_from_text(
            user_lines[-utterance_index], topn=3
        )
        for index, score in best_indices:
            if score < retrieval_threshold:
                continue

            if "PERM_" in index:
                continue

            index = int(index.replace("ITEM_", ""))
            index_list.append(index)

    for index in index_list:
        summary += _knowledge["items"][index] + "\n"

    summary = summary.replace(".\n", ". ")
    summary = summary.replace("\n", ". ")
    return summary
