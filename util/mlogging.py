import logging

# 创建logger对象
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 设置最低日志级别为INFO

# 创建一个控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建一个文件处理器，保存日志到本地文件
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# 创建日志输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 将格式应用到处理器
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

