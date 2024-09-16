from annotated_types.test_cases import cases

from config import get_model,get_api_key
from .mlogging import logger

model  = get_model()
first_model = model["first_model"]
second_model = model["second_model"]
api_keys = get_api_key()

class ChatManager:
    def __init__(self):
        self.has_question = False
        self.data = []
    def clear(self):
        self.data = []
        self.has_question = False
    def add(self,data):
        if self.has_question:
            raise ValueError("已经有问题了")
        self.data.append(data)

    def ask(self):
        if not self.data:
            raise ValueError("没有问题,请先添加问题在请求回答")
        run(self.data)
    def get_answer(self):
        if not self.has_question:
            logger.info(f"获取回答,对话:{self.data}")
            return self.data[-1]
        else:
            raise ValueError("请先请求回答")

def run(data):
    if first_model == "chatglm":
        from .apis import run
        run(api_keys,second_model,data)
    else:
        print("未找到对应模型")

if __name__ == "__main__":
    data = ["你好呀，你是谁？","我是小助手，你可以问我问题哦","1+1等于多少？"]
    run(data)

