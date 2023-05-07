# This file is a placeholder.
# One needs to separate the connection to GPTJ part to the chatbot logic.
# A refactoring is needed.

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


class Connector:
    _terminal_characters = ["\n", "User:"]
    _path = os.path.dirname(__file__)
    _config = yaml.safe_load(open(os.path.join(_path, "../config.yaml")))
    _server_url = f"https://{_config['connection']['host']}:{_config['connection']['port']}/predictions/bot"
    _retriever = DenseRetriever("msmarco-distilbert-base-v3")
    _toxic_detector = ToxicityDetector("original")
    _language_detector = LanguageDetector()
    _knowledge = yaml.safe_load(open(os.path.join(_path, "../knowledge.yaml")))
    _chatbot_name = _knowledge["chatbot"]["name"]

    def __init__(self):
        for index, sentence in enumerate(self._knowledge["permanent"]):
            self._retriever.add_text_and_index(sentence, "PERM_" + str(index))

        for index, sentence in enumerate(self._knowledge["items"]):
            self._retriever.add_text_and_index(sentence, "ITEM_" + str(index))

    def predict_answer(self, prompt: str) -> str:
        payload = {"data": prompt, "num_beams": 1, "num_tokens": 8}
        answer = requests.post(self._server_url, json=payload, verify=False)
        if not answer.text:
            return "\n"
        print(answer.text)
        return answer.text

    def create_dialogue_from_bot_and_user_lines(
        self, bot_lines, user_lines, max_history=3
    ):
        dialogue = ""
        for bot_line, user_line in zip(
            bot_lines[-max_history:], user_lines[-max_history:]
        ):
            dialogue += f"{self._chatbot_name}: {bot_line}\n"
            dialogue += f"User: {user_line}\n"

        return dialogue

    def get_reply_from_connection(self, summary: str, dialogue: str):
        answer = ""
        while all(item not in answer for item in self._terminal_characters):
            text = create_text_from_summary_and_dialogue(summary, dialogue + answer)
            answer += self.predict_answer(text)

        end = min(
            [
                answer.find(item)
                for item in self._terminal_characters
                if answer.find(item) > 0
            ]
        )
        answer = answer[:end].strip()
        return answer

    def generate_reply(
        self, prologue, bot_lines: List[str], user_lines: List[str]
    ) -> str:
        summary = self.get_relevant_summary(user_lines, prologue)

        print(summary)

        if self._toxic_detector.is_toxic(user_lines[-1]):
            return self._knowledge["profanity"][0]

        if not self._language_detector.is_english(user_lines[-1]):
            return self._knowledge["non-english"][0]

        dialogue = self.create_dialogue_from_bot_and_user_lines(bot_lines, user_lines)
        dialogue += f"{self._chatbot_name}: "
        answer = self.get_reply_from_connection(summary, dialogue)
        if answer != bot_lines[-1]:
            if self._toxic_detector.is_toxic(answer):
                return self._knowledge["profanity"][0]

            return answer

        dialogue = f"User: {user_lines[-1]}\n"
        dialogue += f"{self._chatbot_name}: "

        answer = self.get_reply_from_connection(summary, dialogue)
        if self._toxic_detector.is_toxic(answer):
            return self._knowledge["profanity"]

        return answer

    def get_relevant_summary(
        self, user_lines: List[str], prologue: str = "", retrieval_threshold=0.128
    ) -> str:
        query = user_lines[-1]
        summary = "\n".join(self._knowledge["permanent"]) + "\n"
        summary += prologue + "\n"
        best_indices = self._retriever.get_indices_and_scores_from_text(query, topn=3)
        print(best_indices)
        if (
            is_question(query)
            and all(item[1] < retrieval_threshold for item in best_indices)
            and not query_refers_to_prior_dialogue(query)
        ):
            summary += f"When asked '{query}', the user replies '{self._knowledge['default'][0]}'.\n"
            return summary

        index_list = []
        for index, score in best_indices:
            if score < retrieval_threshold:
                continue

            if "PERM_" in index:
                continue

            index = int(index.replace("ITEM_", ""))
            index_list.append(index)

        for utterance_index in range(2, min(len(user_lines) + 1, 4)):
            best_indices = self._retriever.get_indices_and_scores_from_text(
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
            summary += self._knowledge["items"][index] + "\n"

        if not index_list:
            summary += f"{self._chatbot_name} wants to move the conversation to a different topic.\n"

        summary = summary.replace(".\n", ". ")
        summary = summary.replace("\n", ". ")
        return summary
