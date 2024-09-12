import yaml
# private_config.yaml为私有配置文件，不会上传到git仓库

data = {}
data["config"] = yaml.safe_load(open("config/config.yaml"))
data["pricate_config"] = yaml.safe_load(open("config/private_config.yaml"))
first_model = data["config"]["model"]["first_model"]

def get_model():
    return data["config"]["model"]

def get_api_key():
    return data["pricate_config"]["keys"][first_model]

if __name__ == "__main__":
    print(get_model())
    print(get_api_key())
