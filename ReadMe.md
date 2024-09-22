# 项目简介
本项目旨在复刻[Aggregation of Reasoning : AHierarchical Framework for Enhancing Answer Selection in Large Language Models](https://arxiv.org/abs/2405.12939)
目前能够完成从初始采样到动态采样，最后得到结果的整个流程。

# 项目结构
略

# 环境配置
````bash
conda env create -f environments.yml
````
在/config文件夹中创建一个private_config.yaml文件，内容如下
````yaml
keys:
  "chatglm": "your private key"
````
如果需要其他api支持可以在util/api.py中添加相应的api支持

对于aor模型，在/model/aor_config.py中添加相应的配置


# 使用方法
运行main.py即可
在/data文件夹中存放中间数据以及结果
app.log为日志文件
all_data为当前问题的所有数据
judge_data为最终的结果
