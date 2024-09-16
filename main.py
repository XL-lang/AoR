from model.aor.aor_model import AOR
if __name__ == "__main__":
    config = {
        "initial_sample": 20,
        "max_sample": 100
    }
    aor = AOR(config)
    aor.run()
    print(aor.database.all_data)