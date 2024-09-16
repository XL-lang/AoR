import typing
import pandas as pd
from .prompt import *
from util.dataset import get_gsm8k
from util.api import ChatManager
from .aor_data import AOR_data

class AOR:
    def __init__(self, config):
        self.initial_sample = config["initial_sample"]
        self.max_sample = config["max_sample"]
        self.chat_manager = ChatManager()
        self.question,self.answer = self.get_benchmark()
        self.question: pd.Series
        self.answer: pd.Series
        self.database = AOR_data()


    def run(self):
        for question in self.question.values:
            self.local_sample(question)
            break

    def local_sample(self, question: str):
        for i in range(self.initial_sample):
            self.chat_manager.add(question + answer_number_last)
            self.chat_manager.ask()
            answer = self.chat_manager.get_answer()
            self.database.add_new_data(answer)
            self.chat_manager.clear()

    def get_benchmark(self):
        return get_gsm8k()



