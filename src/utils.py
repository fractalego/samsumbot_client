import re

from nltk import pos_tag
from nltk import word_tokenize


def create_text_from_summary_and_dialogue(summary, dialogue):
    text = f"""
A partial summary of the conversation is:
{summary}

With the dialogue being:
{dialogue}
    """.strip()

    return text.replace("\r\n", "\n")


def tokenize_data(data, tokenizer, max_length=110):
    _limit = 1024
    tokenized_data = []
    total_skipped = 0
    for item in data:
        text = create_text_from_summary_and_dialogue(item["summary"], item["dialogue"])
        tokens = tokenizer.encode(
            text, return_tensors="pt", truncation=True, max_length=max_length
        )
        if tokens.shape[1] > _limit:
            tokens = tokens[:, :_limit]
        tokenized_data.append(tokens)

    print(f"Skipped {total_skipped} out of {len(data)}")
    return tokenized_data


def is_question(text):
    text = text.strip()
    if not text:
        return False

    if text[-1] == "?":
        return True

    text = re.sub("^Are", "are", text)
    text = re.sub("^Am", "am", text)

    word_and_pos_list = pos_tag(word_tokenize(text))
    first_tag = word_and_pos_list[0][1]
    for item in word_and_pos_list:
        if item[1] not in ["CC", ".", "RB"]:
            first_tag = item[1]
            break

    if first_tag in ["VBZ", "VBD", "VBP", "MD", "WRB", "WP", "WDT"]:
        return True

    return False


def query_refers_to_prior_dialogue(text):
    text = text.strip()
    if not text:
        return False

    text = re.sub("^Are", "are", text)
    text = re.sub("^Am", "am", text)

    if "which one" in text.lower():
        return True

    word_and_pos_list = pos_tag(word_tokenize(text))
    for item in word_and_pos_list:
        if item[0].lower() in ["yours", "mine", "its", "hers", "his", "theirs"]:
            return True

        if item[1] in ["PRP", "PRP$"] and item[0].lower() not in ["you", "your"]:
            return True

        if item[1] in ["RB"] and item[0].lower() in ["there"]:
            return True

    for item in word_and_pos_list:
        if item[1] not in ["CC", "RB", "WRB", "WP", "WDT", "IN"]:
            return False

    return True
