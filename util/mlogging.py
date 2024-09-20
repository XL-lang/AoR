import logging

# 创建logger对象
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 设置最低日志级别为INFO

# 创建一个控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建一个文件处理器，保存日志到本地文件，并使用utf-8编码
file_handler = logging.FileHandler('data/app.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 创建日志输出格式，使用%(filename)s来显示实际调用日志的文件名
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

# 将格式应用到处理器
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


