import os.path
import re
from typing import List, Union

from .aor_config import config
from .prompt import *
from util.dataset import get_gsm8k
from util.api import ChatManager
import pandas as pd
from .aor_config import config



from util.mlogging import logger

class Judege_data_element:
    def __init__(self):
        self.index = 0
        self.question = ""
        self.model_answer = ""
        self.judge_answer = ""
        self.sample_num = 0
        self.top_score = 0
        self.top2_score = 0
        self.quit_type = ""

class Judege_data:
    def __init__(self):
        self.index = []
        self.question = []
        self.model_answer = []
        self.judge_answer = []
        self.sample_num = []
        self.top_score = []
        self.top2_score = []
        self.quit_type = []
    def add_data(self,element:Judege_data_element):
        self.index.append(element.index)
        self.question.append(element.question)
        self.model_answer.append(element.model_answer)
        self.judge_answer.append(element.judge_answer)
        self.sample_num.append(element.sample_num)
        self.top_score.append(element.top_score)
        self.top2_score.append(element.top2_score)
        self.quit_type.append(element.quit_type)
        self.save_data_to_csv()

    def save_data_to_csv(self):
        data_path = "data"
        columns = ["index", "question", "model_answer", "judge_answer", "sample_num", "top_score", "top2_score","quit_type"]


        data = list(
            zip(self.index, self.question, self.model_answer, self.judge_answer, self.sample_num, self.top_score,
                self.top2_score,self.quit_type))


        df = pd.DataFrame(data, columns=columns)


        df.to_csv(os.path.join(data_path, "judge_data.csv"), index=False)

class AOR_data:
    def __init__(self):
        self.all_data:List[Aor_data_element] = []
        self.chunks = {}
        self.chunks_score = {}
        self.k = config["top_k"]
    def add_new_data(self, new_data:str,question:str):



        aor_data_element = Aor_data_element(new_data,question)
        if aor_data_element.failed:
            return False

        self.all_data.append(aor_data_element)
        self.save_data()
        return True
    def group_data_by_num(self):
        if not self.all_data:
            raise ValueError("No data found,you should initailize the data first")
        self.chunks = {}
        for i in self.all_data:
            if i.num not in self.chunks:
                self.chunks[i.num] = []
            self.chunks[i.num].append(i)
        return self.chunks

    def sort_chunks(self):
        chunks_top_k = {}
        if not self.chunks:
            raise ValueError("sort chunks error: no chunks found")
        for key,value in self.chunks.items():
            value.sort(key=lambda x:x.local_score,reverse=True)
            if len(value) < self.k:
                chunks_top_k[key] = value
                for i in range(self.k - len(value)):
                    chunks_top_k[key].append(value[-1])
            else:
                chunks_top_k[key] = value[:self.k]
        self.chunks_score = {}
        return chunks_top_k

    def add_chunk_score(self,score:Union[int,float],key:str):
        if key not in self.chunks_score:
            self.chunks_score[key] = 0
        self.chunks_score[key] += float(score)/self.k




    def save_data(self):
        data_path = "data"
        columns = ["question","answer","num","local_score","global_score"]
        data = [i.to_list() for i in self.all_data]
        df = pd.DataFrame(data,columns=columns)
        df.to_csv(os.path.join(data_path,"all_data.csv"),index=False)











class Aor_data_element:
    def __init__(self, answer:str,question:str):
        self.question = question
        self.answer = answer
        self.num = self.parse_string(answer)
        self.failed = False
        self.local_score = -1
        self.global_score = -1


    def parse_string(self,string:str):
        pattern = re.compile(r'(-?\d+\.?\d*)')


        num = pattern.findall(string)
        if not num:
            logger.error(f"Error: no number found in {string}")
            self.failed = True
            return  None
        return float(num[-1])

    def parse_local_score(self,string:str):
        self.local_score = self.parse_string(string)

    def parse_global_score(self,string:str):
        self.global_score = self.parse_string(string)




    def to_list(self):
        return [self.question,self.answer,self.num,self.local_score,self.global_score]
