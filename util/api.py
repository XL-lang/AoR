from annotated_types.test_cases import cases

from config import get_model,get_api_key


model  = get_model()
first_model = model["first_model"]
second_model = model["second_model"]
api_keys = get_api_key()

def run(data):
    if first_model == "chatglm":
        from apis import run
        run(api_keys,second_model,data)
    else:
        print("未找到对应模型")

if __name__ == "__main__":
    data = ["你好呀，你是谁？","我是小助手，你可以问我问题哦","1+1等于多少？"]
    run(data)

