from zhipuai import ZhipuAI


def run(api_keys,second_model,data):
    client = ZhipuAI(api_key=api_keys)  # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model=second_model,  # 请填写您要调用的模型名称
        messages=fomat_data(data),
    )
    data.append(response.choices[0].message.content)
    return data
def fomat_data(data):
    messages = []
    for i in range(len(data)):
        if i % 2 == 0:
            messages.append({"role": "user", "content": data[i]})
        else:
            messages.append({"role": "assistant", "content": data[i]})
    return messages
def unformat_data(messages):
    data = []
    for i in range(len(messages)):
        data.append(messages[i]["content"])
    return data