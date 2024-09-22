import typing
import pandas as pd
from typing_extensions import Union

from util import logger
from .prompt import *
from util.dataset import get_gsm8k
from util.api import ChatManager
from .aor_data import AOR_data,Aor_data_element,Judege_data,Judege_data_element
from .aor_config import config

class AOR:
    def __init__(self):
        self.initial_sample = config["initial_sample"]
        self.max_sample = config["max_sample"]
        self.chat_manager = ChatManager()
        self.question,self.answer = self.get_benchmark()
        self.question: pd.Series
        self.answer: pd.Series
        self.database = None
        self.judge_data = Judege_data()
        self.judge_data_element:Judege_data_element = None


    def run(self):
        max_count = config["question_number"]
        if max_count == -1:
            max_count = len(self.question)
        count = 0
        for index,question in enumerate(self.question.values):
            count += 1
            if count > max_count:
                break
            self.database = AOR_data()
            self.judge_data_element:Judege_data_element = Judege_data_element()
            self.judge_data_element.index = index
            self.judge_data_element.question = question
            self.judge_data_element.judge_answer = self.answer[index]
            self.local_sample(question)
            self.local_evaluation()
            self.global_evaluation()
            flag = True
            turn = 0
            while flag:
                turn += 1
                flag = not self.dynamic_sample(turn)

            self.judge_data.add_data(self.judge_data_element)


    def local_sample(self, question: str):
        for i in range(self.initial_sample):
            flag = False
            while not flag:
                self.chat_manager.add(question + answer_number_last +cot_prompt)
                self.chat_manager.ask()
                answer = self.chat_manager.get_answer()
                flag = self.database.add_new_data(answer,question)
                self.chat_manager.clear()
    def local_evaluation(self):
        chunks = self.database.group_data_by_num()
        for key, value in chunks.items():
            self.chat_manager.clear()
            local_evaluation_prompt = f"Question: {value[0].question}\n{local_evaluation}"
            self.chat_manager.add(local_evaluation_prompt)
            self.chat_manager.ask()
            for element in value:
                element: Aor_data_element
                flag = True
                while  flag:
                    self.chat_manager.add(prompt_before_answer+element.answer)
                    self.chat_manager.ask()
                    answer = self.chat_manager.get_answer()
                    element.parse_local_score(answer)
                    flag = element.failed
                    if element.failed:
                        self.chat_manager.clean_last_conversation()
                        element.failed = False
        self.database.save_data()

    def global_evaluation(self):
        chunks_top_k:dict = self.database.sort_chunks()
        for i in range(0,self.database.k):
            question = self.database.all_data[0].question
            final_global_evaluation = question_prompt+question+global_evaluation
            self.chat_manager.add(final_global_evaluation)
            self.chat_manager.ask()
            for key,value in chunks_top_k.items():
                element:Aor_data_element = value[i]
                flag = True
                res:Union[int,float] = 0
                while flag:
                    self.chat_manager.add(prompt_before_answer+element.answer)
                    self.chat_manager.ask()
                    answer = self.chat_manager.get_answer()
                    element.parse_global_score(answer)
                    res = element.global_score
                    flag = element.failed
                    if element.failed:
                        self.chat_manager.clean_last_conversation()
                        element.failed = False
                self.database.add_chunk_score(res,key)
        self.database.save_data()
        logger.info(f"global evaluation finished,{self.database.chunks_score}")

    def dynamic_sample(self,turn:int):
        temp = []
        for key,value in self.database.chunks_score.items():
            temp.append((key,value))
        temp.sort(key=lambda x:x[1],reverse=True)
        self.judge_data_element.model_answer = temp[0][0]
        self.judge_data_element.top_score = temp[0][1]
        if len(temp) > 1:
            self.judge_data_element.top2_score = temp[1][1]
        else:
            self.judge_data_element.top2_score = 0
        self.judge_data_element.sample_num = len(self.database.all_data)

        # return condition
        if len(temp)<=1:
            self.judge_data_element.quit_type = "one answer only"
            return True
        if len(self.database.all_data) >= self.max_sample:
            self.judge_data_element.quit_type = "max sample"
            return True
        if temp[0][1] - temp[1][1] >= config["theta"]:
            self.judge_data_element.quit_type = "theta"
            return True
        logger.info(f"turn {turn}, dynamic sample")
        for i in range(0,config["batch_size"]):
            question = self.database.all_data[0].question
            self.chat_manager.clear()
            self.chat_manager.add(question)
            self.chat_manager.ask()
            answer = self.chat_manager.get_answer()
            self.database.add_new_data(answer,question)
        self.local_evaluation()
        self.global_evaluation()
        return False






    def get_benchmark(self):
        return get_gsm8k()






