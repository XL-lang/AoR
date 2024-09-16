import pandas as pd
import re


def get_gsm8k():
    """
    Get the GSM-8K dataset.
    """
    # %%
    splits = {'train': 'main/train-00000-of-00001.parquet', 'test': 'main/test-00000-of-00001.parquet'}
    df = pd.read_parquet("hf://datasets/openai/gsm8k/" + splits["train"])
    questions = df["question"]
    answer = df["answer"]
    number_re = re.compile(r'####.(-?\d+)')
    res = []
    for string in answer.values:
        string_re = number_re.findall(string)
        if string_re:
            number = int(string_re[0])
            res.append(number)
        else:
            raise ValueError(f"No number found, string: {string}")
    answer = pd.Series(res)
    return questions, answer
