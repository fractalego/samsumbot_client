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
