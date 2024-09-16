import re
from typing import List

from .aor_config import config
from .prompt import *
from util.dataset import get_gsm8k
from util.api import ChatManager
import pandas as pd
class AOR_data:
    def __init__(self, config=config):
        self.all_data = []
    def add_new_data(self, new_data:str):
        aor_data_element = Aor_data_element(new_data)
        self.all_data.append(aor_data_element)






class Aor_data_element:
    def __init__(self, answer:str):
        self.answer = answer
        self.num = self.parse_answer()
        self.local_score = -1
        self.global_score = -1

    def parse_answer(self):
        pattern = re.compile(r'(-?\d+)')
        num = pattern.findall(self.answer)
        if not num:
            raise ValueError(f"No score found in the answer, answer: {self.answer}")
        return num[-1]
