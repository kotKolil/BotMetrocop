import yaml

def GetBotToken():
    with open('config.yaml', 'r') as file:
        data = yaml.safe_load(file)

    return data["BotToken"]

