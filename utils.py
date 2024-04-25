import yaml

def GetBotToken(TypeOfData:str):
    with open('config.yaml', 'r') as file:
        data = yaml.safe_load(file)

    return data[TypeOfData]

